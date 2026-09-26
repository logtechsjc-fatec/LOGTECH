# Consultas Power Query (linguagem M)

Código de importação e tratamento de cada base do ERP ALVO. Todas as consultas leem os arquivos da pasta definida no parâmetro **PastaDados** (veja `dados/README.md`).

## Centro de Custo_20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "3. Centro de Custo_20260824.xlsx"), null, true),
    #"Centro de Custo_Sheet" = Fonte{[Item="Centro de Custo",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Centro de Custo_Sheet", [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Código", Int64.Type}, {"Nome", type text}, {"Sigla", type text}, {"Tipo", type text}, {"Inicial", type datetime}, {"Final", type datetime}, {"Linha", type text}})
in
    #"Tipo Alterado"
```

## Fato_Planejamento

```powerquery
let
    Fonte = RES43_20260824,
    #"Duplicatas Removidas" = Table.Distinct(Fonte, {"CPTM"})
in
    #"Duplicatas Removidas"
```

## Movimentações Materiais_20260825

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "8. Movimentações Materiais_20260825.xlsx"), null, true),
    #"Page 1_Sheet" = Fonte{[Item="Page 1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Page 1_Sheet", [PromoteAllScalars=true]),
    #"Texto Limpo" = Table.TransformColumns(#"Cabeçalhos Promovidos", List.Transform(Table.ColumnNames(#"Cabeçalhos Promovidos"), each {_, (x) => if x is text then (if Text.Trim(Text.Clean(x)) = "" then null else Text.Trim(Text.Clean(x))) else x})),
    #"Tipo Texto" = Table.TransformColumnTypes(#"Texto Limpo",{{"Número", type text}, {"Descrição", type text}, {"Local de Armazenagem", type text}, {"Centro de Controle", type text}, {"Funcionário Entregou", type text}, {"Funcionário", type text}, {"Funcionário Separação", type text}, {"Funcionário Retirou", type text}, {"Equipamento", type text}, {"Sucata", type text}}),
    #"Tipo Data" = Table.TransformColumnTypes(#"Tipo Texto",{{"Data Aprovação", type datetime}, {"Data Entrega", type datetime}, {"Data Conferência", type datetime}, {"Data Separação", type datetime}, {"Data Fim Separação", type datetime}, {"Data Início Separação", type datetime}, {"Data", type datetime}}, "pt-BR")
in
    #"Tipo Data"
```

## PROD__20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "1. PROD__20260824_V1.xlsx"), null, true),
    Sheet1_Sheet = Fonte{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Alternativo", Int64.Type}, {"Nome", type text}, {"Observação", type text}, {"Código do Desenho", type text}, {"Estruturado", type text}, {"Grupo", type text}, {"Reduzido", Int64.Type}, {"Alternativo 1", type text}, {"Código de Barras", Int64.Type}, {"Nome Alternativo 1", type text}, {"Nome Alternativo 2", type text}, {"Nome Alternativo 3", type any}, {"Tipo do Produto", type text}, {"Tipo da Mídia", type text}, {"Classificação Fiscal", type text}, {"Baixa Estoque Composição", type text}, {"Tipo Produto Fiscal (SPED)", type text}, {"Gênero do Serviço", type text}, {"Comprimento Entra no Cálculdo do Espaço", type text}, {"Largura Entra no Cálculo do Espaço", type text}, {"Altura Entra no Cálculo do Espaço", type text}, {"Entra na Pesquisa Aplicação Externa", type text}, {"Visualiza na Página Principal em Aplicações Externas", type text}, {"Aparece Destacado em Aplicações Externas", type text}, {"Status", type text}, {"Utilização do Produto", type text}, {"Norma Aplicação", type text}, {"Tipo de Consumo", type text}, {"Classe BEC", Int64.Type}, {"Ação", type text}, {"Custo Pesquisa", type number}, {"Crítico", type text}, {"Prazo de Validade", Int64.Type}, {"Área Localizada", type text}, {"Tipo da Estrutura", type text}, {"Iluminação", type text}, {"Tipo Iluminação", type text}, {"Responsável Energia Elétrica", type text}, {"Junção", type text}, {"Exclui IPI do Crédito do PIS/COFINS", type text}, {"Múltipla Aprovação Cotação Compra", type text}, {"Base Lote Controle Esterilização", type text}, {"Exclui Frete/Seguro do Crédito do PIS/COFINS", type text}, {"Solicita Cartão Kanban", type text}, {"Utiliza Atendimento Pedido de Venda", type text}, {"Calcula Quantidade Composição", type text}, {"Incluir o Valor da Composição no Item", type text}, {"Natureza de Rendimento R-4000", type any}, {"Auto Retenção", type text}, {"Tipo de Ligação", type text}, {"Segmento Rocha", type text}, {"Gerar Ordem de Produção pelo Pedido Venda", type text}, {"Finaliza OP automaticamente ao Atingir Qtd Necessá", type text}, {"Obriga Atendimento da RM na Liberação da OP", type text}, {"Controla Grade Mix", type text}, {"Integra com Alvo CRM Top", type text}, {"Envio Pesquisa de Preço", type datetime}, {"Valor Custo Pesquisa OBS", type text}, {"Custo Pesquisa Data", type any}, {"Distruibuição Pesquisa", type text}, {"Natureza de Despesa - BEC", type text}, {"Seq Inventário", Int64.Type}, {"Prioridade", type any}, {"Cod ICMS ST", type any}, {"Classificação ABNT NBR 10.004", type any}, {"Descarte Leilão", type text}, {"Descarte Doação", type text}, {"Descarte Reuso", type text}, {"Descarte Reciclagem", type text}, {"Produto Controlado", type text}, {"Descarte Aterro/Tratamento", type text}, {"Previsível", type text}, {"Recupera IBS UF", type text}, {"Recupera IBS Município", type text}, {"Recupera CBS", type text}, {"Fabricação Escala Relevante", type text}, {"Desconsidera Pesagem", type text}, {"Possui Dimensão na Produção", type text}, {"Habilita Comprimento Produção", type text}, {"Habilita Largura Produção", type text}, {"Habilita Altura (Espessura) Produção", type text}}),
    #"Erros Substituídos" = Table.ReplaceErrorValues(#"Tipo Alterado", {{"Alternativo", null}, {"Grupo", null}}),
    #"Linhas Filtradas" = Table.SelectRows(#"Erros Substituídos", each [Alternativo] <> null and [Grupo] <> "Sim")
in
    #"Linhas Filtradas"
```

## RES34_20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "4. RES34_20260824.xlsx"), null, true),
    #"Page 1_Sheet" = Fonte{[Item="Page 1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Page 1_Sheet", [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Cód. Estr.", type text}, {"Cód. Red.", Int64.Type}, {"UN", type text}, {"Descrição", type text}, {"Status", type text}, {"ABNT NBR 10.004", type any}, {"Leilão", type any}, {"Doação", type any}, {"Reuso", type any}, {"Reciclagem", type any}, {"Log. Reversa", type any}, {"Aterro", type any}, {"Ult. Saída", type date}, {"Ult. Entrada", type date}, {"Local", type text}, {"Almoxarifado", type text}, {"Saldo Atual", type number}, {"Valor Unit", type number}, {"Valor Total", type number}, {"Reserva Estoque", type number}, {"Saldo Total", type number}}),
    #"Tipo Alterado com Localidade" = Table.TransformColumnTypes(#"Tipo Alterado", {{"Valor Total", type number}}, "pt-BR"),
    #"Tipo Alterado com Localidade1" = Table.TransformColumnTypes(#"Tipo Alterado com Localidade", {{"Reserva Estoque", type number}}, "pt-BR"),
    #"Tipo Alterado com Localidade2" = Table.TransformColumnTypes(#"Tipo Alterado com Localidade1", {{"Saldo Total", type number}}, "pt-BR")
in
    #"Tipo Alterado com Localidade2"
```

## RES43_20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "RES43_Base_Consolidada.xlsx"), null, true),
    Sheet1_Sheet = Fonte{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Seq.", Int64.Type}, {"CPTM", Int64.Type}, {"Cód.Estr.", type text}, {"Código BEC", type text}, {"Classe BEC", Int64.Type}, {"Descrição", type text}, {"Centro de Controle", type text}, {"Saldo", type number}, {"Consumo Médio Mensal", type number}, {"PCA Mensal (fatia)", type number}, {"Utilização (%)", type number}, {"Quantidade Necessária p/ Compra", type number}, {"Previsão $", type number}, {"Qtd. Solic.", Int64.Type}, {"Prior.", type text}, {"Qtd. Contratada", Int64.Type}, {"RMs Aberta", Int64.Type}, {"SCs Provisórias", Int64.Type}, {"OFs a Entregar", Int64.Type}, {"tipo_consumo", type text}, {"opcao_relatorio", type text}, {"insuficiente_meses", Int64.Type}, {"compra_meses", Int64.Type}, {"considera_saldo_calculo", type text}, {"arquivo_origem", type text}})
in
    #"Tipo Alterado"
```

## RES47_20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "5. RES47_20260824.xlsx"), null, true),
    #"Page 1_Sheet" = Fonte{[Item="Page 1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Page 1_Sheet", [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Código Reduzido", Int64.Type}, {"Código Estruturado", type text}, {"Descrição", type text}, {"Tipo Consumo", type text}, {"Utilização", type text}, {"Unid. Medida", type text}, {"Quantidade", type number}, {"Custo Médio", type number}, {"Valor Total", type number}, {"Última Movimentação", type date}, {"Último Consumo", type date}})
in
    #"Tipo Alterado"
```

## RES75_20260824

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "6. RES75_20260824.xlsx"), null, true),
    #"Page 1_Sheet" = Fonte{[Item="Page 1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Page 1_Sheet", [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"PCAN", type any}, {"Centro de Controle", Int64.Type}, {"Produto Estruturado", type text}, {"Código CPTM", Int64.Type}, {"Código BEC", type text}, {"Descrição", type text}, {"Unid. Medida Principal", type text}, {"Tipo Consumo", type text}, {"Utilização", type text}, {"Status", type text}, {"Espeficicação Técnica", type text}, {"Qtde PCAN", Int64.Type}, {"Qtde PCAN Reestruturação", Int64.Type}, {"Qtde Estoque", Int64.Type}, {"Dias Estoque Zerado", Int64.Type}, {"2014 MOV", type any}, {"2014 PCA", type text}, {"2015 MOV", type any}, {"2015 PCA", type text}, {"2016 MOV", type any}, {"2016 PCA", type text}, {"2017 MOV", type any}, {"2017 PCA", type text}, {"2018 MOV", type any}, {"2018 PCA", type text}, {"2019 MOV", type any}, {"2019 PCA", type text}, {"2020 MOV", type any}, {"2020 PCA", type text}, {"2021 MOV", type any}, {"2021 PCA", type text}, {"2022 MOV", type any}, {"2022 PCA", type text}, {"2023 MOV", type any}, {"2023 PCA", type text}, {"2024 MOV", type any}, {"2024 PCA", type text}, {"2025 MOV", type text}, {"2025 PCA", type text}, {"2026 MOV", type text}, {"2026 PCA", type text}}),
    #"Linhas Superiores Removidas" = Table.Skip(#"Tipo Alterado",1),
    #"Consumo 2025" = Table.AddColumn(#"Linhas Superiores Removidas", "Consumo 2025", each try Number.From([#"2025 MOV"], "pt-BR") otherwise null, type number)
in
    #"Consumo 2025"
```

## RES82_20260825

```powerquery
let
    Fonte = Excel.Workbook(File.Contents(PastaDados & "7. RES82_20260825.xlsx"), null, true),
    #"Page 1_Sheet" = Fonte{[Item="Page 1",Kind="Sheet"]}[Data],
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Page 1_Sheet", [PromoteAllScalars=true]),
    #"Tipo Texto" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Chave", type text}, {"Entidade", type text}, {"Espécie", type text}, {"Número", type text}, {"Tipo Lancto.", type text}, {"Produto", type text}, {"Tipo Produto", type text}, {"Complemento", type text}}),
    #"Tipo Data" = Table.TransformColumnTypes(#"Tipo Texto",{{"Entrada", type date}, {"Emissão", type date}}, "pt-BR"),
    #"Tipo Número" = Table.TransformColumnTypes(#"Tipo Data",{{"Qtde.", type number}, {"Valor Unit.", type number}, {"Valor Total", type number}, {"Difal ICMS", type number}, {"IPI", type number}, {"Glosa", type number}, {"Percentual", type number}, {"Valor", type number}}, "pt-BR"),
    #"Cód. Estr." = Table.AddColumn(#"Tipo Número", "Cód. Estr.", each Text.Trim(Text.BeforeDelimiter([Produto], " - ")), type text),
    #"Código Movimento" = Table.AddColumn(#"Cód. Estr.", "Código Movimento", each Text.Trim(Text.BeforeDelimiter([#"Tipo Lancto."], " - ")), type text),
    #"Número RM" = Table.AddColumn(#"Código Movimento", "Número RM", each if [Espécie] = "RM" then [Número] else null, type text)
in
    #"Número RM"
```
