# Dicionário de Indicadores

Fórmula, fonte e página de cada indicador do painel. É a mesma tabela exibida na página **Metodologia** do Power BI.

| Nº | Indicador | Fórmula / regra | Fonte | Página |
|---|---|---|---|---|
| 1 | Estoque em quantidade | Soma do saldo atual dos materiais | RES34 – Saldo Atual | Visão de Estoque |
| 2 | Estoque em valor (R$) | Soma do valor total em estoque | RES34 – Valor Total | Visão de Estoque |
| 3 | Materiais com saldo | Nº de materiais distintos com saldo maior que zero | RES34 | Visão de Estoque |
| 4 | Curva ABC | Materiais ordenados por valor em estoque: A até 80% do valor acumulado, B até 95%, C o restante | RES34 (tabela CurvaABC) | Visão de Estoque |
| 5 | Estoque médio 12 meses (R$) | Média de 13 posições mensais (ago/25 a ago/26). Cada posição = saldo de 24/08/2026 menos as movimentações líquidas posteriores à data | RES47 + RES82 | Visão de Estoque / Indicadores |
| 6 | Giro de estoque 12 meses | Consumo efetivo dos últimos 12 meses (R$) ÷ estoque médio 12 meses (R$) | RES82 + RES47 | Visão de Estoque / Indicadores |
| 7 | Consumo efetivo | Saídas por requisição de manutenção, operação, administração e engenharia. Não inclui transferências, devoluções, ajustes, remessas, vendas e descartes | RES82 – Tipo Lancto. | Indicadores / Consumo |
| 8 | Consumo médio mensal | Consumo efetivo dos últimos 12 meses ÷ 12 | RES82 | Indicadores |
| 9 | Cobertura (meses) | Por material: saldo atual ÷ consumo médio mensal. No total: valor em estoque ÷ consumo médio mensal em R$ | RES47 + RES82 | Indicadores |
| 10 | Ruptura | Saldo igual a zero e consumo nos últimos 12 meses | RES47 + RES82 | Indicadores |
| 11 | Risco de ruptura | Tem consumo e a cobertura está abaixo do limite escolhido (padrão: 3 meses) | RES47 + RES82 + parâmetro | Indicadores |
| 12 | Excesso de estoque | Tem consumo e a cobertura está acima do limite escolhido (padrão: 24 meses) | RES47 + RES82 + parâmetro | Indicadores |
| 13 | Sem consumo 12 meses | Tem saldo, mas nenhum consumo nos últimos 12 meses. Não significa que o material é obsoleto | RES47 + RES82 | Indicadores |
| 14 | Tempo sem consumo | Meses entre o último consumo e 24/08/2026, agrupados em faixas (12, 24, 36, 60 meses ou mais) | RES47 – Último Consumo | Indicadores |
| 15 | PCA anual | PCA mensal (coluna K, 'fatia') × 12 | RES43 | Consumo e Aderência |
| 16 | Aderência ao PCA | Consumo efetivo 12 meses ÷ PCA anual. Aderente: 80% a 120%; acima: mais de 120%; abaixo: menos de 80% | RES43 + RES82 | Consumo e Aderência |
| 17 | Material crítico | Tipo de consumo Essencial ou Estratégico (classificação da CPTM). A Curva ABC mede valor, não criticidade | RES47 / RES75 | Filtro de todas as páginas |
| 18 | Tipo de consumo | Tipo de consumo da RES47; quando não existe, o da RES75 | RES47 / RES75 | Filtro de todas as páginas |
| 19 | Giro por material | Consumo efetivo 12 meses (quantidade) ÷ estoque médio do material, sendo estoque médio = (estoque inicial + estoque final) ÷ 2 | RES47 + RES82 | Giro e Rotatividade |
| 20 | Classificação por rotatividade | Alta: giro ≥ 4; Média: giro de 1 a 4; Baixa: giro < 1; Sem giro: tem saldo e não teve consumo em 12 meses | RES47 + RES82 | Giro e Rotatividade |
| 21 | Tempo médio de permanência (dias) | 365 ÷ giro. Indica, em média, quantos dias o material fica no estoque | RES47 + RES82 | Giro e Rotatividade |
| 22 | Sazonalidade | Consumo efetivo médio de cada mês do ano (2021 a 2025). Índice = mês ÷ média dos meses | RES82 | Giro e Rotatividade |
| 23 | Variação do consumo | (Consumo dos últimos 12 meses − consumo dos 12 meses anteriores) ÷ consumo dos 12 meses anteriores | RES82 | Evolução por Material |
| 24 | Cobertura com pedidos (meses) | (Saldo + OFs a entregar + quantidade contratada) ÷ consumo médio mensal | RES43 | Reposição |
| 25 | Etapa do processo de compra | Etapa mais avançada do material: OF a entregar, em contratação, SC provisória, RM aberta ou sem processo iniciado | RES43 | Reposição |
| 26 | Estoque obsoleto | Valor e quantidade de materiais com status Obsoleto e a destinação indicada (leilão, doação, reuso, reciclagem, logística reversa, aterro) | RES34 | Obsolescência |
