# Dados

As planilhas do ERP ALVO **não são versionadas** neste repositório, porque são dados internos da CPTM. Coloque os arquivos abaixo em uma pasta do seu computador e informe essa pasta no parâmetro **PastaDados** do Power BI.

| Arquivo esperado | Conteúdo | Aba |
|---|---|---|
| `1. PROD__20260824_V1.xlsx` | Cadastro de materiais | Sheet1 |
| `RES43_Base_Consolidada.xlsx` | Materiais no ponto de reposição (Normal, Essencial e Estratégico) | Sheet1 |
| `3. Centro de Custo_20260824.xlsx` | Centros de custo | Centro de Custo |
| `4. RES34_20260824.xlsx` | Saldo por almoxarifado e obsolescência | Page 1 |
| `5. RES47_20260824.xlsx` | Posição do estoque | Page 1 |
| `6. RES75_20260824.xlsx` | PCAN e movimentação anual | Page 1 |
| `7. RES82_20260825.xlsx` | Movimentações de materiais (2021–2026) | Page 1 |
| `8. Movimentações Materiais_20260825.xlsx` | Etapas das requisições | Page 1 |

Os nomes dos arquivos precisam ser exatamente esses. Se a CPTM enviar novas extrações com outra data no nome, altere o nome na etapa **Fonte** da consulta correspondente no Power Query.
