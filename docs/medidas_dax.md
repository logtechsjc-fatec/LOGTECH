# Medidas DAX

Todas as medidas do modelo `LOGTECH_CPTM`, agrupadas pela pasta de exibição (uma pasta para cada página do painel).
O código é o mesmo do arquivo `powerbi/LOGTECH_CPTM.SemanticModel/definition/tables/Medidas.tmdl`.

Total: **123 medidas**.

## Índice

- [Visão de Estoque](#visão-de-estoque) – 8 medidas
- [Indicadores Logísticos](#indicadores-logísticos) – 23 medidas
- [Giro e Rotatividade](#giro-e-rotatividade) – 15 medidas
- [Consumo e Aderência](#consumo-e-aderência) – 19 medidas
- [Evolução por Material](#evolução-por-material) – 17 medidas
- [Reposição](#reposição) – 20 medidas
- [Obsolescência](#obsolescência) – 8 medidas
- [Metodologia](#metodologia) – 13 medidas

## Visão de Estoque

### Estoque Total

Formato: `#,0`

```dax
Estoque Total =
    SUM(RES34_20260824[Saldo Atual])
```

### Quantidade Total de Itens

Formato: `0`

```dax
Quantidade Total de Itens =
    COUNT(Fato_Planejamento[Saldo])
```

### Valor Estoque

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
Valor Estoque =
    SUM(RES34_20260824[Valor Total])
```

### Materiais em Estoque

Formato: `#,0`

```dax
Materiais em Estoque =
    CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Saldo Atual] > 0 )
```

### % Valor ABC

Formato: `0.0%`

```dax
% Valor ABC =
    DIVIDE ( [Valor Estoque], CALCULATE ( [Valor Estoque], ALL ( PROD__20260824[Classe ABC] ) ) )
```

### % Itens ABC

Formato: `0.0%`

```dax
% Itens ABC =
    DIVIDE ( [Materiais em Estoque], CALCULATE ( [Materiais em Estoque], ALL ( PROD__20260824[Classe ABC] ) ) )
```

### % Valor na Classe A

Formato: `0.0%`

```dax
% Valor na Classe A =
    CALCULATE ( [% Valor ABC], PROD__20260824[Classe ABC] = "A" )
```

### Itens na Classe A

Formato: `#,0`

```dax
Itens na Classe A =
    CALCULATE ( [Materiais em Estoque], PROD__20260824[Classe ABC] = "A" )
```


## Indicadores Logísticos

### Data Base Estoque

Formato: `Short Date`

```dax
Data Base Estoque =
    DATE ( 2026, 8, 24 )
```

### Saldo Qtd (RES47)

Formato: `#,0.##`

```dax
Saldo Qtd (RES47) =
    SUM ( RES47_20260824[Quantidade] )
```

### Valor Estoque (RES47)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Valor Estoque (RES47) =
    SUM ( RES47_20260824[Valor Total] )
```

### Materiais (RES47)

Formato: `#,0`

```dax
Materiais (RES47) =
    DISTINCTCOUNT ( RES47_20260824[Código Reduzido] )
```

### Consumo 12m (Qtd)

Formato: `#,0.##`

```dax
Consumo 12m (Qtd) =
    VAR ref = [Data Base Estoque]
    RETURN
        CALCULATE (
            SUM ( RES82_20260825[Qtde.] ),
            'Tipo de Movimentação'[Categoria] = "Consumo efetivo",
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -12 ),
            RES82_20260825[Entrada] <= ref
        )
```

### Consumo 12m (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Consumo 12m (R$) =
    VAR ref = [Data Base Estoque]
    RETURN
        CALCULATE (
            SUM ( RES82_20260825[Valor Total] ),
            'Tipo de Movimentação'[Categoria] = "Consumo efetivo",
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -12 ),
            RES82_20260825[Entrada] <= ref
        )
```

### Consumo Médio Mensal 12m

Formato: `#,0.##`

```dax
Consumo Médio Mensal 12m =
    DIVIDE ( [Consumo 12m (Qtd)], 12 )
```

### Cobertura Material (meses)

Formato: `#,0.0`

```dax
Cobertura Material (meses) =
    DIVIDE ( [Saldo Qtd (RES47)], [Consumo Médio Mensal 12m] )
```

### Cobertura Estoque (meses)

Formato: `#,0.0`

```dax
Cobertura Estoque (meses) =
    DIVIDE ( [Valor Estoque (RES47)], DIVIDE ( [Consumo 12m (R$)], 12 ) )
```

### Estoque Médio 12m (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Estoque Médio 12m (R$) =
    VAR ref = [Data Base Estoque]
    VAR atual = [Valor Estoque (RES47)]
    RETURN
        AVERAGEX (
            GENERATESERIES ( 0, 12, 1 ),
            VAR d = IF ( [Value] = 12, ref, EOMONTH ( ref, [Value] - 12 ) )
            RETURN
                atual
                    - CALCULATE (
                        SUM ( RES82_20260825[Valor Líquido] ),
                        REMOVEFILTERS ( dCalendario ),
                        RES82_20260825[Entrada] > d,
                        RES82_20260825[Entrada] <= ref
                    )
        )
```

### Giro de Estoque

Formato: `#,0.00`

```dax
Giro de Estoque =
    DIVIDE ( [Consumo 12m (R$)], [Estoque Médio 12m (R$)] )
```

### Estoque Fim do Mês (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Estoque Fim do Mês (R$) =
    VAR ref = [Data Base Estoque]
    VAR fimMes = MAX ( dCalendario[Date] )
    VAR iniMes = MIN ( dCalendario[Date] )
    VAR d = MIN ( fimMes, ref )
    RETURN
        IF (
            fimMes >= EOMONTH ( ref, -12 ) && iniMes <= ref,
            [Valor Estoque (RES47)]
                - CALCULATE (
                    SUM ( RES82_20260825[Valor Líquido] ),
                    REMOVEFILTERS ( dCalendario ),
                    RES82_20260825[Entrada] > d,
                    RES82_20260825[Entrada] <= ref
                )
        )
```

### Limite Risco (meses)

Formato: `0`

```dax
Limite Risco (meses) =
    SELECTEDVALUE ( 'Parâmetro Risco'[Risco (meses)], 3 )
```

### Limite Excesso (meses)

Formato: `0`

```dax
Limite Excesso (meses) =
    SELECTEDVALUE ( 'Parâmetro Excesso'[Excesso (meses)], 24 )
```

### Status Estoque

```dax
Status Estoque =
    VAR s = COALESCE ( [Saldo Qtd (RES47)], 0 )
    VAR c = COALESCE ( [Consumo Médio Mensal 12m], 0 )
    VAR cob = DIVIDE ( s, c )
    RETURN
        SWITCH (
            TRUE (),
            c > 0 && s <= 0, "Ruptura",
            c > 0 && cob < [Limite Risco (meses)], "Risco de ruptura",
            c > 0 && cob > [Limite Excesso (meses)], "Excesso",
            c > 0, "Adequado",
            s > 0, "Sem consumo 12m",
            BLANK ()
        )
```

### Prioridade

Formato: `0`

```dax
Prioridade =
    SWITCH ( [Status Estoque], "Ruptura", 1, "Risco de ruptura", 2, "Excesso", 3, "Sem consumo 12m", 4, "Adequado", 5 )
```

### Cor Status

```dax
Cor Status =
    SWITCH ( [Status Estoque], "Ruptura", "#C8102E", "Risco de ruptura", "#E07B00", "Adequado", "#2E8B57", "Excesso", "#1F5FBF", "Sem consumo 12m", "#7A869A" )
```

### Cor Status Barra

```dax
Cor Status Barra =
    SWITCH ( SELECTEDVALUE ( dStatus[Status] ), "Ruptura", "#C8102E", "Risco de ruptura", "#E07B00", "Adequado", "#2E8B57", "Excesso", "#1F5FBF", "Sem consumo 12m", "#7A869A" )
```

### Materiais no Status

Formato: `#,0`

```dax
Materiais no Status =
    VAR st = SELECTEDVALUE ( dStatus[Status] )
    RETURN
        IF (
            NOT ISBLANK ( st ),
            COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), [Status Estoque] = st ) )
        )
```

### Materiais em Ruptura

Formato: `#,0`

```dax
Materiais em Ruptura =
    CALCULATE ( [Materiais no Status], dStatus[Status] = "Ruptura" )
```

### Materiais em Risco de Ruptura

Formato: `#,0`

```dax
Materiais em Risco de Ruptura =
    CALCULATE ( [Materiais no Status], dStatus[Status] = "Risco de ruptura" )
```

### Materiais em Excesso

Formato: `#,0`

```dax
Materiais em Excesso =
    CALCULATE ( [Materiais no Status], dStatus[Status] = "Excesso" )
```

### Materiais sem Consumo 12m

Formato: `#,0`

```dax
Materiais sem Consumo 12m =
    CALCULATE ( [Materiais no Status], dStatus[Status] = "Sem consumo 12m" )
```


## Giro e Rotatividade

### Estoque Inicial 12m (Qtd)

Formato: `#,0.##`

```dax
Estoque Inicial 12m (Qtd) =
    VAR ref = [Data Base Estoque]
    VAR movLiquido =
        CALCULATE (
            SUM ( RES82_20260825[Qtd Líquida] ),
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -12 ),
            RES82_20260825[Entrada] <= ref
        )
    RETURN MAX ( 0, COALESCE ( [Saldo Qtd (RES47)], 0 ) - COALESCE ( movLiquido, 0 ) )
```

### Estoque Médio Material (Qtd)

Formato: `#,0.##`

```dax
Estoque Médio Material (Qtd) =
    ( [Estoque Inicial 12m (Qtd)] + COALESCE ( [Saldo Qtd (RES47)], 0 ) ) / 2
```

### Giro Material 12m

Formato: `#,0.00`

```dax
Giro Material 12m =
    DIVIDE ( [Consumo 12m (Qtd)], [Estoque Médio Material (Qtd)] )
```

### Permanência Material (dias)

Formato: `#,0`

```dax
Permanência Material (dias) =
    DIVIDE ( 365, [Giro Material 12m] )
```

### Tempo Médio de Permanência (dias)

Formato: `#,0`

```dax
Tempo Médio de Permanência (dias) =
    DIVIDE ( 365, [Giro de Estoque] )
```

### Classe Rotatividade

```dax
Classe Rotatividade =
    VAR c = COALESCE ( [Consumo 12m (Qtd)], 0 )
    VAR s = COALESCE ( [Saldo Qtd (RES47)], 0 )
    VAR g = [Giro Material 12m]
    RETURN
        SWITCH (
            TRUE (),
            c > 0 && ( ISBLANK ( g ) || g >= 4 ), "Alta (giro ≥ 4)",
            c > 0 && g >= 1, "Média (giro de 1 a 4)",
            c > 0, "Baixa (giro < 1)",
            s > 0, "Sem giro (sem consumo)",
            BLANK ()
        )
```

### Materiais na Rotatividade

Formato: `#,0`

```dax
Materiais na Rotatividade =
    VAR r = SELECTEDVALUE ( dRotatividade[Rotatividade] )
    RETURN
        IF (
            NOT ISBLANK ( r ),
            COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), [Classe Rotatividade] = r ) )
        )
```

### Materiais Alta Rotatividade

Formato: `#,0`

```dax
Materiais Alta Rotatividade =
    CALCULATE ( [Materiais na Rotatividade], dRotatividade[Rotatividade] = "Alta (giro ≥ 4)" )
```

### Materiais Média Rotatividade

Formato: `#,0`

```dax
Materiais Média Rotatividade =
    CALCULATE ( [Materiais na Rotatividade], dRotatividade[Rotatividade] = "Média (giro de 1 a 4)" )
```

### Materiais Baixa Rotatividade

Formato: `#,0`

```dax
Materiais Baixa Rotatividade =
    CALCULATE ( [Materiais na Rotatividade], dRotatividade[Rotatividade] = "Baixa (giro < 1)" )
```

### Materiais Sem Giro

Formato: `#,0`

```dax
Materiais Sem Giro =
    CALCULATE ( [Materiais na Rotatividade], dRotatividade[Rotatividade] = "Sem giro (sem consumo)" )
```

### Cor Rotatividade

```dax
Cor Rotatividade =
    SWITCH ( [Classe Rotatividade], "Alta (giro ≥ 4)", "#2E8B57", "Média (giro de 1 a 4)", "#1F5FBF", "Baixa (giro < 1)", "#E07B00", "Sem giro (sem consumo)", "#C8102E" )
```

### Cor Rotatividade Barra

```dax
Cor Rotatividade Barra =
    SWITCH ( SELECTEDVALUE ( dRotatividade[Rotatividade] ), "Alta (giro ≥ 4)", "#2E8B57", "Média (giro de 1 a 4)", "#1F5FBF", "Baixa (giro < 1)", "#E07B00", "Sem giro (sem consumo)", "#C8102E" )
```

### Consumo Médio por Mês do Ano (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Consumo Médio por Mês do Ano (R$) =
    CALCULATE (
        AVERAGEX ( VALUES ( dCalendario[Ano] ), [Consumo Efetivo (R$)] ),
        dCalendario[Ano] >= 2021,
        dCalendario[Ano] <= 2025
    )
```

### Índice de Sazonalidade

Formato: `0.00`

```dax
Índice de Sazonalidade =
    VAR mes = [Consumo Médio por Mês do Ano (R$)]
    VAR media = CALCULATE ( AVERAGEX ( VALUES ( dCalendario[Mês Num] ), [Consumo Médio por Mês do Ano (R$)] ), REMOVEFILTERS ( dCalendario[Mês do Ano], dCalendario[Mês Num] ) )
    RETURN DIVIDE ( mes, media )
```


## Consumo e Aderência

### Consumo Efetivo (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Consumo Efetivo (R$) =
    CALCULATE ( SUM ( RES82_20260825[Valor Total] ), 'Tipo de Movimentação'[Categoria] = "Consumo efetivo" )
```

### Entradas por Compra (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Entradas por Compra (R$) =
    CALCULATE ( SUM ( RES82_20260825[Valor Total] ), 'Tipo de Movimentação'[Categoria] = "Entrada por compra" )
```

### Entradas por Compra 12m (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Entradas por Compra 12m (R$) =
    VAR ref = [Data Base Estoque]
    RETURN
        CALCULATE (
            SUM ( RES82_20260825[Valor Total] ),
            'Tipo de Movimentação'[Categoria] = "Entrada por compra",
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -12 ),
            RES82_20260825[Entrada] <= ref
        )
```

### Saídas 12m (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Saídas 12m (R$) =
    VAR ref = [Data Base Estoque]
    RETURN
        CALCULATE (
            SUM ( RES82_20260825[Valor Total] ),
            'Tipo de Movimentação'[Sentido] = "Saída",
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -12 ),
            RES82_20260825[Entrada] <= ref
        )
```

### Posição do Estoque (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Posição do Estoque (R$) =
    VAR ref = [Data Base Estoque]
    VAR fimMes = MAX ( dCalendario[Date] )
    VAR iniMes = MIN ( dCalendario[Date] )
    VAR d = MIN ( fimMes, ref )
    RETURN
        IF (
            iniMes <= ref && fimMes >= DATE ( 2021, 1, 31 ),
            [Valor Estoque (RES47)]
                - CALCULATE (
                    SUM ( RES82_20260825[Valor Líquido] ),
                    REMOVEFILTERS ( dCalendario ),
                    RES82_20260825[Entrada] > d,
                    RES82_20260825[Entrada] <= ref
                )
        )
```

### PCA Anual (RES43)

Formato: `#,0.##`

```dax
PCA Anual (RES43) =
    [PCA Mensal] * 12
```

### Aderência PCA (%)

Formato: `0%`

```dax
Aderência PCA (%) =
    DIVIDE ( [Consumo 12m (Qtd)], [PCA Anual (RES43)] )
```

### Classe Aderência

```dax
Classe Aderência =
    VAR p = [PCA Anual (RES43)]
    VAR c = COALESCE ( [Consumo 12m (Qtd)], 0 )
    RETURN
        IF (
            NOT ISBLANK ( p ),
            SWITCH (
                TRUE (),
                p <= 0 && c > 0, "Consumo sem PCA",
                p <= 0, BLANK (),
                c = 0, "Sem consumo",
                c / p < 0.8, "Abaixo do planejado",
                c / p <= 1.2, "Aderente",
                "Acima do planejado"
            )
        )
```

### Materiais na Classe

Formato: `#,0`

```dax
Materiais na Classe =
    VAR cl = SELECTEDVALUE ( dAderencia[Classe] )
    RETURN
        IF (
            NOT ISBLANK ( cl ),
            COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), [Classe Aderência] = cl ) )
        )
```

### Materiais com PCA

Formato: `#,0`

```dax
Materiais com PCA =
    COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), [PCA Anual (RES43)] > 0 ) )
```

### Materiais Aderentes

Formato: `#,0`

```dax
Materiais Aderentes =
    CALCULATE ( [Materiais na Classe], dAderencia[Classe] = "Aderente" )
```

### Materiais Acima do PCA

Formato: `#,0`

```dax
Materiais Acima do PCA =
    CALCULATE ( [Materiais na Classe], dAderencia[Classe] = "Acima do planejado" )
```

### Materiais Abaixo do PCA

Formato: `#,0`

```dax
Materiais Abaixo do PCA =
    CALCULATE ( [Materiais na Classe], dAderencia[Classe] = "Abaixo do planejado" )
```

### Materiais com PCA sem Consumo

Formato: `#,0`

```dax
Materiais com PCA sem Consumo =
    CALCULATE ( [Materiais na Classe], dAderencia[Classe] = "Sem consumo" )
```

### % Materiais Aderentes

Formato: `0.0%`

```dax
% Materiais Aderentes =
    DIVIDE ( [Materiais Aderentes], [Materiais com PCA] )
```

### Cor Aderência

```dax
Cor Aderência =
    SWITCH ( [Classe Aderência], "Acima do planejado", "#C8102E", "Aderente", "#2E8B57", "Abaixo do planejado", "#1F5FBF", "Sem consumo", "#7A869A", "Consumo sem PCA", "#E07B00" )
```

### Cor Aderência Barra

```dax
Cor Aderência Barra =
    SWITCH ( SELECTEDVALUE ( dAderencia[Classe] ), "Acima do planejado", "#C8102E", "Aderente", "#2E8B57", "Abaixo do planejado", "#1F5FBF", "Sem consumo", "#7A869A", "Consumo sem PCA", "#E07B00" )
```

### Cor Categoria Saída

```dax
Cor Categoria Saída =
    IF ( SELECTEDVALUE ( 'Tipo de Movimentação'[Categoria] ) = "Consumo efetivo", "#C8102E", "#8FA3C4" )
```

### Consumo 12m (materiais com PCA)

Formato: `#,0.##`

```dax
Consumo 12m (materiais com PCA) =
    IF ( NOT ISBLANK ( [PCA Anual (RES43)] ), COALESCE ( [Consumo 12m (Qtd)], 0 ) )
```


## Evolução por Material

### Material Selecionado

```dax
Material Selecionado =
    HASONEVALUE ( PROD__20260824[Alternativo] )
```

### Entradas (Qtd)

Formato: `#,0.##`

```dax
Entradas (Qtd) =
    CALCULATE ( SUM ( RES82_20260825[Qtde.] ), 'Tipo de Movimentação'[Sentido] = "Entrada" )
```

### Saídas (Qtd)

Formato: `#,0.##`

```dax
Saídas (Qtd) =
    CALCULATE ( SUM ( RES82_20260825[Qtde.] ), 'Tipo de Movimentação'[Sentido] = "Saída" )
```

### Consumo Efetivo (Qtd)

Formato: `#,0.##`

```dax
Consumo Efetivo (Qtd) =
    CALCULATE ( SUM ( RES82_20260825[Qtde.] ), 'Tipo de Movimentação'[Categoria] = "Consumo efetivo" )
```

### Entradas - Item (Qtd)

Formato: `#,0.##`

```dax
Entradas - Item (Qtd) =
    IF ( [Material Selecionado], [Entradas (Qtd)] )
```

### Saídas - Item (Qtd)

Formato: `#,0.##`

```dax
Saídas - Item (Qtd) =
    IF ( [Material Selecionado], [Saídas (Qtd)] )
```

### Consumo Efetivo - Item (Qtd)

Formato: `#,0.##`

```dax
Consumo Efetivo - Item (Qtd) =
    IF ( [Material Selecionado], [Consumo Efetivo (Qtd)] )
```

### Posição do Estoque - Item (Qtd)

Formato: `#,0.##`

```dax
Posição do Estoque - Item (Qtd) =
    VAR ref = [Data Base Estoque]
    VAR fimMes = MAX ( dCalendario[Date] )
    VAR iniMes = MIN ( dCalendario[Date] )
    VAR d = MIN ( fimMes, ref )
    RETURN
        IF (
            [Material Selecionado] && iniMes <= ref && fimMes >= DATE ( 2021, 1, 31 ),
            COALESCE ( [Saldo Qtd (RES47)], 0 )
                - COALESCE (
                    CALCULATE (
                        SUM ( RES82_20260825[Qtd Líquida] ),
                        REMOVEFILTERS ( dCalendario ),
                        RES82_20260825[Entrada] > d,
                        RES82_20260825[Entrada] <= ref
                    ),
                    0
                )
        )
```

### Consumo 12m Anterior (Qtd)

Formato: `#,0.##`

```dax
Consumo 12m Anterior (Qtd) =
    VAR ref = [Data Base Estoque]
    RETURN
        CALCULATE (
            SUM ( RES82_20260825[Qtde.] ),
            'Tipo de Movimentação'[Categoria] = "Consumo efetivo",
            REMOVEFILTERS ( dCalendario ),
            RES82_20260825[Entrada] > EDATE ( ref, -24 ),
            RES82_20260825[Entrada] <= EDATE ( ref, -12 )
        )
```

### Variação Consumo 12m (%)

Formato: `+0.0%;-0.0%;0.0%`

```dax
Variação Consumo 12m (%) =
    DIVIDE ( [Consumo 12m (Qtd)] - [Consumo 12m Anterior (Qtd)], [Consumo 12m Anterior (Qtd)] )
```

### Saldo Atual - Item

Formato: `#,0.##`

```dax
Saldo Atual - Item =
    IF ( [Material Selecionado], COALESCE ( [Saldo Qtd (RES47)], 0 ) )
```

### Valor em Estoque - Item

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Valor em Estoque - Item =
    IF ( [Material Selecionado], COALESCE ( [Valor Estoque (RES47)], 0 ) )
```

### Consumo 12m - Item

Formato: `#,0.##`

```dax
Consumo 12m - Item =
    IF ( [Material Selecionado], COALESCE ( [Consumo 12m (Qtd)], 0 ) )
```

### Consumo 12m Anterior - Item

Formato: `#,0.##`

```dax
Consumo 12m Anterior - Item =
    IF ( [Material Selecionado], COALESCE ( [Consumo 12m Anterior (Qtd)], 0 ) )
```

### Variação Consumo - Item

Formato: `+0.0%;-0.0%;0.0%`

```dax
Variação Consumo - Item =
    IF ( [Material Selecionado], COALESCE ( [Variação Consumo 12m (%)], 0 ) )
```

### Cobertura - Item (meses)

Formato: `#,0.0`

```dax
Cobertura - Item (meses) =
    IF ( [Material Selecionado], COALESCE ( [Cobertura Material (meses)], 0 ) )
```

### Situação - Item

```dax
Situação - Item =
    IF ( [Material Selecionado], COALESCE ( [Status Estoque], "-" ), "Selecione um material" )
```


## Reposição

### Consumo Médio Mensal

```dax
Consumo Médio Mensal =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Consumo Médio Mensal] ) ) )
```

### PCA Mensal

```dax
PCA Mensal =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[PCA Mensal (fatia)] ) ) )
```

### RMs Abertas

Formato: `0`

```dax
RMs Abertas =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[RMs Aberta] ) ) )
```

### Quantidade Necessária p/ Compra

```dax
Quantidade Necessária p/ Compra =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Quantidade Necessária p/ Compra] ) ) )
```

### Valor Total Compra

```dax
Valor Total Compra =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Previsão $] ) ) )
```

### Contratações em Andamento

Formato: `0`

```dax
Contratações em Andamento =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Qtd. Contratada] ) ) )
```

### OFs a Entregar

Formato: `0`

```dax
OFs a Entregar =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[OFs a Entregar] ) ) )
```

### SCs Provisórias

Formato: `0`

```dax
SCs Provisórias =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[SCs Provisórias] ) ) )
```

### Saldo Total (para Cobertura)

```dax
Saldo Total (para Cobertura) =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Saldo] ) ) )
```

### Consumo Total (para Cobertura)

```dax
Consumo Total (para Cobertura) =
    SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Consumo Médio Mensal] ) ) )
```

### Cobertura (meses)

```dax
Cobertura (meses) =
    DIVIDE ( [Saldo Total (para Cobertura)], [Consumo Total (para Cobertura)] )
```

### Cobertura por Material

```dax
Cobertura por Material =
    DIVIDE ( 
        CALCULATE ( MAX ( RES43_20260824[Saldo] ) ), 
        CALCULATE ( MAX ( RES43_20260824[Consumo Médio Mensal] ) ) 
    )
```

### Materiais no Ponto de Reposição

Formato: `#,0`

```dax
Materiais no Ponto de Reposição =
    DISTINCTCOUNT ( RES43_20260824[CPTM] )
```

### Materiais Prioritários

Formato: `#,0`

```dax
Materiais Prioritários =
    CALCULATE ( DISTINCTCOUNT ( RES43_20260824[CPTM] ), RES43_20260824[Prior.] = "Sim" )
```

### Materiais na Etapa

Formato: `#,0`

```dax
Materiais na Etapa =
    SWITCH (
        SELECTEDVALUE ( dEtapa[Ordem] ),
        1, COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Quantidade Necessária p/ Compra] ) ) > 0 ) ),
        2, COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[RMs Aberta] ) ) > 0 ) ),
        3, COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[SCs Provisórias] ) ) > 0 ) ),
        4, COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Qtd. Contratada] ) ) > 0 ) ),
        5, COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[OFs a Entregar] ) ) > 0 ) )
    )
```

### Etapa do Processo

```dax
Etapa do Processo =
    VAR rm = CALCULATE ( MAX ( RES43_20260824[RMs Aberta] ) )
    VAR sc = CALCULATE ( MAX ( RES43_20260824[SCs Provisórias] ) )
    VAR ct = CALCULATE ( MAX ( RES43_20260824[Qtd. Contratada] ) )
    VAR ofe = CALCULATE ( MAX ( RES43_20260824[OFs a Entregar] ) )
    VAR nec = CALCULATE ( MAX ( RES43_20260824[Quantidade Necessária p/ Compra] ) )
    RETURN
        SWITCH (
            TRUE (),
            ofe > 0, "OF a entregar",
            ct > 0, "Em contratação",
            sc > 0, "SC provisória",
            rm > 0, "RM aberta",
            nec > 0, "Sem processo iniciado",
            BLANK ()
        )
```

### Materiais sem Processo Iniciado

Formato: `#,0`

```dax
Materiais sem Processo Iniciado =
    COUNTROWS ( FILTER ( VALUES ( RES43_20260824[CPTM] ), [Etapa do Processo] = "Sem processo iniciado" ) )
```

### Cobertura com Pedidos (meses)

Formato: `#,0.0`

```dax
Cobertura com Pedidos (meses) =
    VAR saldo = SUMX ( VALUES ( RES43_20260824[CPTM] ), CALCULATE ( MAX ( RES43_20260824[Saldo] ) ) )
    VAR pedidos = [OFs a Entregar] + [Contratações em Andamento]
    RETURN DIVIDE ( saldo + pedidos, [Consumo Médio Mensal] )
```

### Materiais em Ruptura no Ponto de Reposição

Formato: `#,0`

```dax
Materiais em Ruptura no Ponto de Reposição =
    COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), NOT ISBLANK ( CALCULATE ( COUNTROWS ( RES43_20260824 ) ) ) && [Status Estoque] = "Ruptura" ) )
```

### Cor Etapa

```dax
Cor Etapa =
    SWITCH ( [Etapa do Processo], "Sem processo iniciado", "#C8102E", "RM aberta", "#E07B00", "SC provisória", "#8FA3C4", "Em contratação", "#1F5FBF", "OF a entregar", "#2E8B57" )
```


## Obsolescência

### Valor Estoque Obsoleto

```dax
Valor Estoque Obsoleto =
    CALCULATE ( SUM ( RES34_20260824[Valor Total] ), RES34_20260824[Status] = "Obsoleto" )
```

### Saldo Estoque Obsoleto

```dax
Saldo Estoque Obsoleto =
    CALCULATE ( SUM ( RES34_20260824[Saldo Atual] ), RES34_20260824[Status] = "Obsoleto" )
```

### % Valor Obsoleto sobre Total

Formato: `0.00%;-0.00%;0.00%`

```dax
% Valor Obsoleto sobre Total =
    DIVIDE ( 
        [Valor Estoque Obsoleto], 
        CALCULATE ( SUM ( RES34_20260824[Valor Total] ), ALL ( RES34_20260824[Status] ) ) 
    )
```

### Qtd. Materiais Obsoletos

Formato: `0`

```dax
Qtd. Materiais Obsoletos =
    CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Estr.] ), RES34_20260824[Status] = "Obsoleto" )
```

### Obsoletos sem Destinação

Formato: `#,0`

```dax
Obsoletos sem Destinação =
    CALCULATE (
        DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ),
        RES34_20260824[Status] = "Obsoleto",
        ISBLANK ( RES34_20260824[Leilão] ), ISBLANK ( RES34_20260824[Doação] ), ISBLANK ( RES34_20260824[Reuso] ),
        ISBLANK ( RES34_20260824[Reciclagem] ), ISBLANK ( RES34_20260824[Log. Reversa] ), ISBLANK ( RES34_20260824[Aterro] )
    )
```

### Materiais por Destinação Indicada

Formato: `#,0`

```dax
Materiais por Destinação Indicada =
    SWITCH (
        SELECTEDVALUE ( dDestino[Destinação] ),
        "Leilão", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Leilão] = "X" ),
        "Doação", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Doação] = "X" ),
        "Reuso", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Reuso] = "X" ),
        "Reciclagem", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Reciclagem] = "X" ),
        "Log. Reversa", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Log. Reversa] = "X" ),
        "Aterro", CALCULATE ( DISTINCTCOUNT ( RES34_20260824[Cód. Red.] ), RES34_20260824[Aterro] = "X" )
    )
```

### Obsoletos com Destinação

Formato: `#,0`

```dax
Obsoletos com Destinação =
    [Qtd. Materiais Obsoletos] - [Obsoletos sem Destinação]
```

### Valor Obsoleto sem Destinação

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Valor Obsoleto sem Destinação =
    CALCULATE (
        SUM ( RES34_20260824[Valor Total] ),
        RES34_20260824[Status] = "Obsoleto",
        ISBLANK ( RES34_20260824[Leilão] ), ISBLANK ( RES34_20260824[Doação] ), ISBLANK ( RES34_20260824[Reuso] ),
        ISBLANK ( RES34_20260824[Reciclagem] ), ISBLANK ( RES34_20260824[Log. Reversa] ), ISBLANK ( RES34_20260824[Aterro] )
    )
```


## Metodologia

### Teste RES34 sem PROD

Formato: `#,0`

```dax
Teste RES34 sem PROD =
    COUNTROWS ( FILTER ( RES34_20260824, ISBLANK ( RELATED ( PROD__20260824[Alternativo] ) ) ) ) + 0
```

### Teste RES82 sem PROD

Formato: `#,0`

```dax
Teste RES82 sem PROD =
    COUNTROWS ( FILTER ( RES82_20260825, ISBLANK ( RELATED ( PROD__20260824[Estruturado] ) ) ) ) + 0
```

### Teste RES82 sem Classificação

Formato: `#,0`

```dax
Teste RES82 sem Classificação =
    COUNTROWS ( FILTER ( RES82_20260825, ISBLANK ( RELATED ( 'Tipo de Movimentação'[Categoria] ) ) ) ) + 0
```

### Teste RES47 sem RES34

Formato: `#,0`

```dax
Teste RES47 sem RES34 =
    COUNTROWS ( FILTER ( VALUES ( PROD__20260824[Alternativo] ), NOT ISBLANK ( [Materiais (RES47)] ) && ISBLANK ( CALCULATE ( COUNTROWS ( RES34_20260824 ) ) ) ) ) + 0
```

### Teste Diferença RES47 RES34

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Teste Diferença RES47 RES34 =
    [Valor Estoque (RES47)] - [Valor Estoque]
```

### Consumo 2025 RES82 (Qtd)

Formato: `#,0`

```dax
Consumo 2025 RES82 (Qtd) =
    CALCULATE ( SUM ( RES82_20260825[Qtde.] ), 'Tipo de Movimentação'[Categoria] = "Consumo efetivo", REMOVEFILTERS ( dCalendario ), dCalendario[Ano] = 2025 )
```

### Consumo 2025 RES75 (Qtd)

Formato: `#,0`

```dax
Consumo 2025 RES75 (Qtd) =
    SUM ( RES75_20260824[Consumo 2025] )
```

### Teste Consumo RES82 RES75

Formato: `0.0%`

```dax
Teste Consumo RES82 RES75 =
    DIVIDE ( [Consumo 2025 RES82 (Qtd)], [Consumo 2025 RES75 (Qtd)] )
```

### Teste Saldo Negativo

Formato: `#,0`

```dax
Teste Saldo Negativo =
    VAR ref = [Data Base Estoque]
    VAR ini = EOMONTH ( ref, -12 )
    RETURN
        COUNTROWS (
            FILTER (
                VALUES ( PROD__20260824[Alternativo] ),
                COALESCE ( [Saldo Qtd (RES47)], 0 )
                    - CALCULATE (
                        SUM ( RES82_20260825[Qtd Líquida] ),
                        REMOVEFILTERS ( dCalendario ),
                        RES82_20260825[Entrada] > ini,
                        RES82_20260825[Entrada] <= ref
                    ) < -0.001
            )
        ) + 0
```

### Teste RMs Base 8

Formato: `0.0%`

```dax
Teste RMs Base 8 =
    VAR total = COUNTROWS ( 'Movimentações Materiais_20260825' )
    VAR achadas = COUNTROWS ( FILTER ( 'Movimentações Materiais_20260825', CALCULATE ( COUNTROWS ( RES82_20260825 ) ) > 0 ) )
    RETURN DIVIDE ( achadas, total )
```

### Resultado do Teste

```dax
Resultado do Teste =
    SWITCH (
        SELECTEDVALUE ( 'Testes de Consistência'[Nº] ),
        1, FORMAT ( [Teste RES34 sem PROD], "#,0" ),
        2, FORMAT ( [Teste RES82 sem PROD], "#,0" ) & " linhas",
        3, FORMAT ( [Teste RES82 sem Classificação], "#,0" ),
        4, FORMAT ( [Teste RES47 sem RES34], "#,0" ) & " materiais",
        5, FORMAT ( [Teste Diferença RES47 RES34], "R$ #,0" ),
        6, FORMAT ( [Teste Consumo RES82 RES75], "0.0%" ),
        7, FORMAT ( [Teste Saldo Negativo], "#,0" ) & " materiais",
        8, FORMAT ( [Teste RMs Base 8], "0.0%" )
    )
```

### Lançamentos RES82

Formato: `#,0`

```dax
Lançamentos RES82 =
    COUNTROWS ( RES82_20260825 )
```

### Valor Lançado RES82 (R$)

Formato: `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`

```dax
Valor Lançado RES82 (R$) =
    SUM ( RES82_20260825[Valor Total] )
```
