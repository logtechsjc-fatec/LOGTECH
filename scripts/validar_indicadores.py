"""
Validação independente dos indicadores do painel LOGTECH_CPTM.

Recalcula, com pandas, os principais números do Power BI a partir das
planilhas do ERP ALVO, para conferir se o modelo está correto.

Uso:
    python scripts/validar_indicadores.py --pasta "C:/caminho/para/ERP ALVO"

Saída: um resumo no terminal e o arquivo saida/indicadores_validacao.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DATA_BASE = pd.Timestamp("2026-08-24")  # data da posição da RES47
ARQUIVOS = {
    "prod": ("1. PROD__20260824_V1.xlsx", "Sheet1"),
    "res34": ("4. RES34_20260824.xlsx", "Page 1"),
    "res43": ("RES43_Base_Consolidada.xlsx", "Sheet1"),
    "res47": ("5. RES47_20260824.xlsx", "Page 1"),
    "res75": ("6. RES75_20260824.xlsx", "Page 1"),
    "res82": ("7. RES82_20260825.xlsx", "Page 1"),
    "base8": ("8. Movimentações Materiais_20260825.xlsx", "Page 1"),
}
CLASSIFICACAO = Path(__file__).resolve().parents[1] / "docs" / "classificacao_movimentacoes.csv"


def numero(serie: pd.Series) -> pd.Series:
    """Converte números vindos do ERP (numéricos ou texto no padrão pt-BR)."""
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)
    texto = serie.astype("string").str.strip()
    tem_virgula = texto.str.contains(",", na=False)
    texto = texto.where(~tem_virgula, texto.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(texto, errors="coerce")


def data(serie: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(serie):
        return serie
    return pd.to_datetime(serie, dayfirst=True, errors="coerce")


def ler(pasta: Path, chave: str) -> pd.DataFrame:
    nome, aba = ARQUIVOS[chave]
    df = pd.read_excel(pasta / nome, sheet_name=aba, dtype=object)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def carregar(pasta: Path) -> dict[str, pd.DataFrame]:
    d = {k: ler(pasta, k) for k in ARQUIVOS}

    prod = d["prod"]
    prod["Alternativo"] = numero(prod["Alternativo"])
    prod = prod[prod["Alternativo"].notna() & (prod["Grupo"].astype("string") != "Sim")].copy()
    prod["Alternativo"] = prod["Alternativo"].astype("int64")
    d["prod"] = prod

    r34 = d["res34"]
    for c in ["Cód. Red.", "Saldo Atual", "Valor Total"]:
        r34[c] = numero(r34[c])

    r47 = d["res47"]
    for c in ["Código Reduzido", "Quantidade", "Custo Médio", "Valor Total"]:
        r47[c] = numero(r47[c])
    r47["Último Consumo"] = data(r47["Último Consumo"])

    r43 = d["res43"]
    for c in ["CPTM", "PCA Mensal (fatia)"]:
        r43[c] = numero(r43[c])

    r75 = d["res75"].iloc[1:].copy()  # a primeira linha após o cabeçalho é descartada, como no Power Query
    r75["Código CPTM"] = numero(r75["Código CPTM"])
    r75["Consumo 2025"] = numero(r75["2025 MOV"])
    d["res75"] = r75

    r82 = d["res82"]
    r82["Entrada"] = data(r82["Entrada"])
    r82["Qtde."] = numero(r82["Qtde."])
    r82["Valor Total"] = numero(r82["Valor Total"])
    r82["Cód. Estr."] = r82["Produto"].astype("string").str.split(" - ").str[0].str.strip()
    r82["Código Movimento"] = r82["Tipo Lancto."].astype("string").str.split(" - ").str[0].str.strip()
    tipos = pd.read_csv(CLASSIFICACAO, sep=";", encoding="utf-8-sig")
    r82 = r82.merge(tipos[["Código", "Sentido", "Categoria"]], left_on="Código Movimento", right_on="Código", how="left")
    sinal_qtd = r82["Sentido"].map({"Entrada": 1, "Saída": -1}).fillna(0)
    sinal_valor = r82["Sentido"].map({"Entrada": 1, "Somente valor (+)": 1, "Saída": -1, "Somente valor (-)": -1}).fillna(0)
    r82["Qtd Líquida"] = r82["Qtde."] * sinal_qtd
    r82["Valor Líquido"] = r82["Valor Total"] * sinal_valor
    d["res82"] = r82
    return d


def indicadores(d: dict[str, pd.DataFrame], risco: float = 3, excesso: float = 24) -> dict[str, float]:
    prod, r34, r47, r43, r75, r82, b8 = (d[k] for k in ["prod", "res34", "res47", "res43", "res75", "res82", "base8"])
    res: dict[str, float] = {}

    # Visão de Estoque (RES34)
    res["Estoque em quantidade (RES34)"] = r34["Saldo Atual"].sum()
    res["Estoque em valor R$ (RES34)"] = r34["Valor Total"].sum()
    res["Materiais com saldo (RES34)"] = r34.loc[r34["Saldo Atual"] > 0, "Cód. Red."].nunique()
    por_material = r34.groupby("Cód. Estr.")["Valor Total"].sum().sort_values(ascending=False)
    acumulado = por_material.cumsum() / por_material.sum()
    classe = np.select([acumulado <= 0.8, acumulado <= 0.95], ["A", "B"], "C")
    res["Itens classe A"] = int((classe == "A").sum())
    res["% do valor na classe A"] = por_material[classe == "A"].sum() / por_material.sum()

    # Janela de 12 meses e consumo efetivo (RES82)
    janela = r82[(r82["Entrada"] > DATA_BASE - pd.DateOffset(months=12)) & (r82["Entrada"] <= DATA_BASE)]
    consumo = janela[janela["Categoria"] == "Consumo efetivo"]
    res["Consumo efetivo 12m R$"] = consumo["Valor Total"].sum()
    res["Compras recebidas 12m R$"] = janela.loc[janela["Categoria"] == "Entrada por compra", "Valor Total"].sum()

    # Estoque médio = média de 13 posições mensais reconstruídas
    valor_atual = r47["Valor Total"].sum()
    datas = [DATA_BASE + pd.offsets.MonthEnd(-12 + i) for i in range(12)] + [DATA_BASE]
    ate_base = r82[r82["Entrada"] <= DATA_BASE]
    posicoes = [valor_atual - ate_base.loc[ate_base["Entrada"] > dt, "Valor Líquido"].sum() for dt in datas]
    res["Estoque médio 12m R$"] = float(np.mean(posicoes))
    res["Giro 12m"] = res["Consumo efetivo 12m R$"] / res["Estoque médio 12m R$"]
    res["Tempo médio de permanência (dias)"] = 365 / res["Giro 12m"]
    res["Cobertura do estoque (meses)"] = valor_atual / (res["Consumo efetivo 12m R$"] / 12)

    # Situação por material
    mat = prod[["Alternativo", "Estruturado"]].copy()
    mat["saldo"] = mat["Alternativo"].map(r47.groupby("Código Reduzido")["Quantidade"].sum()).fillna(0)
    mat["consumo_mes"] = mat["Estruturado"].map(consumo.groupby("Cód. Estr.")["Qtde."].sum()).fillna(0) / 12
    cobertura = mat["saldo"] / mat["consumo_mes"].replace(0, np.nan)
    tem_consumo = mat["consumo_mes"] > 0
    mat["status"] = np.select(
        [tem_consumo & (mat["saldo"] <= 0), tem_consumo & (cobertura < risco), tem_consumo & (cobertura > excesso), tem_consumo, mat["saldo"] > 0],
        ["Ruptura", "Risco de ruptura", "Excesso", "Adequado", "Sem consumo 12m"], default="",
    )
    for s in ["Ruptura", "Risco de ruptura", "Adequado", "Excesso", "Sem consumo 12m"]:
        res[f"Materiais - {s}"] = int((mat["status"] == s).sum())

    # Aderência ao PCA (RES43)
    pca = r43.groupby("CPTM")["PCA Mensal (fatia)"].max() * 12
    estruturado = pca.index.to_series().map(prod.set_index("Alternativo")["Estruturado"])
    cons_pca = pd.to_numeric(estruturado.map(consumo.groupby("Cód. Estr.")["Qtde."].sum()), errors="coerce").fillna(0)
    ader = cons_pca / pca.replace(0, np.nan)
    res["Materiais com PCA"] = int((pca > 0).sum())
    res["Materiais aderentes ao PCA (80% a 120%)"] = int(((ader >= 0.8) & (ader <= 1.2)).sum())

    # Testes de consistência
    c25 = r82[(r82["Categoria"] == "Consumo efetivo") & (r82["Entrada"].dt.year == 2025)]["Qtde."].sum()
    res["Teste: consumo 2025 RES82 / RES75"] = c25 / r75["Consumo 2025"].sum()
    res["Teste: tipos de movimentação sem classificação"] = int(r82["Categoria"].isna().sum())
    rms = set(r82.loc[r82["Espécie"] == "RM", "Número"].astype(str))
    res["Teste: RMs da base 8 encontradas na RES82"] = b8["Número"].astype(str).str.strip().isin(rms).mean()
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True, help="Pasta com as planilhas do ERP ALVO")
    ap.add_argument("--risco", type=float, default=3, help="Limite de risco de ruptura, em meses (padrão 3)")
    ap.add_argument("--excesso", type=float, default=24, help="Limite de excesso, em meses (padrão 24)")
    args = ap.parse_args()

    res = indicadores(carregar(Path(args.pasta)), args.risco, args.excesso)
    largura = max(len(k) for k in res)
    for k, v in res.items():
        print(f"{k:<{largura}}  {v:,.4f}" if isinstance(v, float) and abs(v) < 10 else f"{k:<{largura}}  {v:,.0f}")
    saida = Path("saida"); saida.mkdir(exist_ok=True)
    pd.Series(res, name="valor").to_csv(saida / "indicadores_validacao.csv", sep=";", encoding="utf-8-sig")
    print(f"\nResultado salvo em {saida / 'indicadores_validacao.csv'}")


if __name__ == "__main__":
    main()
