# Classificação dos tipos de movimentação (RES82)

A RES82 registra todas as quantidades como números positivos, sem indicar se o lançamento é entrada ou saída.
Por isso, cada um dos 98 tipos de movimentação foi classificado em um **sentido** e em uma **categoria**. Somente a categoria **Consumo efetivo** entra no cálculo de consumo, giro e cobertura, conforme orientação da CPTM.

| Sentido | Efeito no estoque |
|---|---|
| Entrada | soma no saldo |
| Saída | subtrai do saldo |
| Neutro | não altera o saldo (troca de local ou compra não estocável) |
| Somente valor (+/-) | altera apenas o valor (reajustes e regularizações de custo) |

## Resumo por categoria

| Categoria | Tipos |
|---|---|
| Remessa / empréstimo / retorno | 28 |
| Entrada por compra | 11 |
| Descarte / venda / doação | 11 |
| Regularização de valor | 8 |
| Transferência externa | 8 |
| Devolução a fornecedor | 7 |
| Devolução de requisição | 5 |
| Transferência interna | 5 |
| Compra direta (fundo fixo, não estocável) | 5 |
| Consumo efetivo | 4 |
| Ajuste de inventário | 3 |
| Capitalização / outras entradas | 3 |

## Pontos a validar com a CPTM

- `E0000252 – TRANF. TR P/ LOCAL OFICIAL` tratado como **neutro** (a entrada já é registrada na Entrada por OF). Com essa regra, os saldos negativos na reconstrução caem de 680 para 120 materiais.
- Remessas para ViaMobilidade, TIC Trens e STM tratadas como **transferência externa** (não são consumo da CPTM).
- Fundo fixo GOF, GFA e GOS tratados como **compra direta não estocável** (códigos 5.02).

## Tabela completa

| Código | Descrição | Sentido | Categoria |
|---|---|---|---|
| E0000245 | ENTRADA POR OF | Entrada | Entrada por compra |
| E0000248 | DEVOLUÇÃO MATS DIVERSOS - ADM | Entrada | Devolução de requisição |
| E0000249 | SAÍDA POR REQUISIÇÃO ADMINISTRAÇÃO | Saída | Consumo efetivo |
| E0000250 | ENTRADA POR AJUSTE DE INVENTÁRIO | Entrada | Ajuste de inventário |
| E0000251 | SAÍDA POR AJUSTE DE INVENTÁRIO | Saída | Ajuste de inventário |
| E0000252 | TRANF. TR P/ LOCAL OFICIAL | Neutro | Transferência interna |
| E0000256 | SAÍDA DE AMOSTRAS DESTRUÍDAS | Saída | Descarte / venda / doação |
| E0000503 | SAÍDA POR REQUISIÇÃO OPERAÇÃO | Saída | Consumo efetivo |
| E0000504 | SAÍDA POR REQUISIÇÃO MANUTENÇÃO | Saída | Consumo efetivo |
| E0000505 | DEVOLUÇÃO MATS DIVERSOS - OPERAC | Entrada | Devolução de requisição |
| E0000506 | DEVOLUÇÃO MATS DIVERSOS - MANUT | Entrada | Devolução de requisição |
| E0000523 | ENTRADA POR REMESSA (DEMONSTRAÇÃO) | Entrada | Remessa / empréstimo / retorno |
| E0000834 | ESTORNO - TRANSF DE TR EM DUPL - OFICIAL | Neutro | Transferência interna |
| E0000846 | ENTRADA POR TRANSFERÊNCIA DE INSERVÍVEIS | Entrada | Descarte / venda / doação |
| E0000914 | SAÍDA POR TRANSFERÊNCIA DE INSERVÍVEIS | Saída | Descarte / venda / doação |
| E0001020 | ESTORNO DE LAUDO | Neutro | Transferência interna |
| E0001170 | ENTRADA POR REMESSA (AMOSTRA) | Entrada | Remessa / empréstimo / retorno |
| E0001182 | ENTRADA AMOSTRA COM CÁLCULO DIFAL | Entrada | Remessa / empréstimo / retorno |
| E0001195 | ENTRADA POR DEMONSTRAÇÃO - OUTRO ESTADO | Entrada | Remessa / empréstimo / retorno |
| E0001217 | SAÍDA POR REQUISIÇÃO ENGENHARIA | Saída | Consumo efetivo |
| E0001218 | DEVOLUÇÃO MATS DIVERSOS - ENGENHARIA | Entrada | Devolução de requisição |
| E0001224 | ENTRADA POR OF - FORMULÁRIOS | Entrada | Entrada por compra |
| E0001247 | VENDA SUCATA/INSERVÍVEIS - LEILÃO | Saída | Descarte / venda / doação |
| E0001248 | DEVOLUÇÃO PARA FORNECEDOR | Saída | Devolução a fornecedor |
| E0001249 | RETORNO DE PROTÓTIPO | Entrada | Remessa / empréstimo / retorno |
| E0001250 | REMESSA P/ INDUSTRIALIZAÇÃO | Saída | Remessa / empréstimo / retorno |
| E0001251 | SAÍDA POR DOAÇÃO | Saída | Descarte / venda / doação |
| E0001252 | RETORNO DE LOCAÇÃO/EMPRÉSTIMO | Entrada | Remessa / empréstimo / retorno |
| E0001261 | DEVOLUÇÃO P/ FORNECEDOR PRODUTO - ST | Saída | Devolução a fornecedor |
| E0001267 | REMESSA EM GARANTIA - PRODUTOS ESTOQUE | Saída | Remessa / empréstimo / retorno |
| E0001268 | RETORNO DE REMESSA EM GARANTIA - ESTOQUE | Entrada | Remessa / empréstimo / retorno |
| E0001275 | REGULARIZAÇÃO DE SALDO DE CUSTO MÉDIO | Somente valor (+) | Regularização de valor |
| E0001278 | REGULARIZAÇÃO C. MÉDIO INDUSTRIALIZAÇÃO | Somente valor (+) | Regularização de valor |
| E0001280 | ENTRADA POR OF INDUSTRIALIZAÇÃO | Entrada | Entrada por compra |
| E0001302 | ENTRADA DE REMESSA PRODUTO TRANSITÓRIO | Entrada | Remessa / empréstimo / retorno |
| E0001303 | SAÍDA PARA TESTE PRODUTO TRANSITÓRIO | Saída | Remessa / empréstimo / retorno |
| E0001307 | DEVOLUÇÃO DE VENDA EM LEILÃO | Entrada | Descarte / venda / doação |
| E0001352 | EMPRESTIMO - ITENS ESTOQUE | Saída | Remessa / empréstimo / retorno |
| E0001355 | SAÍDA POR DESCARTE | Saída | Descarte / venda / doação |
| E0001365 | ENTRADA DE SOBRESSALENTES | Entrada | Entrada por compra |
| E0001368 | ENTRADA REAJUSTE CAPA | Somente valor (+) | Regularização de valor |
| E0001371 | ENTRADA  APENAS DE REAJUSTE | Somente valor (+) | Regularização de valor |
| E0001413 | REMESSA P/ CONSERTO - BENS PATRIM. ESTOQ | Saída | Remessa / empréstimo / retorno |
| E0001434 | BAIXA MAT. REPROV. S/INTEGRAÇÃO-BX FORNE | Saída | Devolução a fornecedor |
| E0001447 | AMOSTRA OU MAT N RETIR -REPROV.TR.SUCATA | Saída | Descarte / venda / doação |
| E0001448 | BAIXA MATERIAIS - AMOSTRA / DEMONSTRAÇÃO | Saída | Descarte / venda / doação |
| E0001470 | REMESSA PARA TESTE/ANALISE - C/ RETORNO | Saída | Remessa / empréstimo / retorno |
| E0001471 | RETORNO DE REMESSA - TESTE/ANALISE | Entrada | Remessa / empréstimo / retorno |
| E0001514 | FUNDO FIXO - GOF | Neutro | Compra direta (fundo fixo, não estocável) |
| E0001519 | FUNDO FIXO - GOS | Neutro | Compra direta (fundo fixo, não estocável) |
| E0001520 | FUNDO FIXO - GFA | Neutro | Compra direta (fundo fixo, não estocável) |
| E0001528 | FUNDO FIXO - GOF (SUBSTITUIÇÃO TRIBUT.) | Neutro | Compra direta (fundo fixo, não estocável) |
| E0001529 | FUNDO FIXO - GOS (SUBSTITUIÇÃO TRIBUT.) | Neutro | Compra direta (fundo fixo, não estocável) |
| E0001561 | DEVOLUÇÃO FORMULÁRIOS - NF SERVIÇO | Saída | Devolução a fornecedor |
| E0001562 | DESCARTE SUCATA - DECLARAÇÃO | Saída | Descarte / venda / doação |
| E0001564 | FUNDO FIXO DFMA - KIT -ESTOQUE | Entrada | Entrada por compra |
| E0001638 | ENTRADA REMESSA PARA TESTE - SEM RETORNO | Entrada | Remessa / empréstimo / retorno |
| E0001639 | REMESSA EM GARANTIA - TRIBUTADA | Saída | Remessa / empréstimo / retorno |
| E0001663 | TRANSF. AMOSTRA P/ ESTOQUE OFICIAL | Neutro | Transferência interna |
| E0001664 | RETORNO DE EMPRÉSTIMO | Entrada | Remessa / empréstimo / retorno |
| E0001675 | FUNDO FIXO - DEVOLUÇÃO DFMA - MAT. ESTOQ | Saída | Devolução a fornecedor |
| E0001687 | TRANSF. MAT.NÃO RETIR. P/ ESTOQ. OFICIAL | Neutro | Transferência interna |
| E0001752 | FUNDO FIXO - DFMA (MATERIAL DE ESTOQUE) | Entrada | Entrada por compra |
| E0001753 | FUNDO FIXO - DFMA (MAT. ESTOQUE - S.T.) | Entrada | Entrada por compra |
| E0001795 | SOBRESSALENTES CONTRATO - ESTOQ. TRANSIT | Entrada | Entrada por compra |
| E0001798 | RETORNO DE EMPRÉSTIMO- S/ INTEGR. FISCAL | Entrada | Remessa / empréstimo / retorno |
| E0001804 | BAIXA DE AMOSTRA - ESTOQUE TRANSITÓRIO | Saída | Descarte / venda / doação |
| E0001829 | ENTRADA NOTA RECUSADA (ESTOQUE) | Entrada | Remessa / empréstimo / retorno |
| E0001840 | DEVOLUÇÃO FORNECEDOR-ICMS DIF. NF COMPRA | Saída | Devolução a fornecedor |
| E0001847 | REGULARIZAÇÃO ENTRADA INDEVIDA | Saída | Ajuste de inventário |
| E0001852 | DEVOLUÇÃO FORNECEDOR SEM FISCAL | Saída | Devolução a fornecedor |
| E0001853 | ENTRADA POR ESMPRESTIMO | Entrada | Remessa / empréstimo / retorno |
| E0001870 | SAÍDA TRANSITÓRIO - EMPRÉSTIMO | Saída | Remessa / empréstimo / retorno |
| E0001874 | REMESSA DEVOLUÇÃO DE EMPRÉSTIMOS | Saída | Remessa / empréstimo / retorno |
| E0001898 | SAÍDA REGULARIZAÇÃO DE CUSTO MÉDIO | Somente valor (-) | Regularização de valor |
| E0001907 | COMPLEMENTO VALOR-DEV. EMPREST. A MENOR | Somente valor (+) | Regularização de valor |
| E0001914 | ENTRADA COMODATO/EMPR - SEM MOV. ESTOQUE | Neutro | Remessa / empréstimo / retorno |
| E0001916 | REMESSA MATERIAIS VIA MOBILIDADE | Saída | Transferência externa |
| E0001917 | REGULARIZAÇÃO CUSTO MÉDIO ENTRADA INSERV | Somente valor (+) | Regularização de valor |
| E0001918 | REGULARIZAÇÃO DE VALOR - DEV. INSERV. | Somente valor (+) | Regularização de valor |
| E0001935 | DEVOLUÇÃO DE PROTÓTIPO | Entrada | Remessa / empréstimo / retorno |
| E0001952 | FUNDO FIXO - DOLM (MAT. ESTOQ S/RM) | Entrada | Entrada por compra |
| E0001953 | FUNDO FIXO - DOLM (ESTOQUE - ST S/RM ) | Entrada | Entrada por compra |
| E0001991 | DEVOLUÇÃO INSERVIVEL | Entrada | Devolução de requisição |
| E0002009 | REMESSA MATERIAIS TIC TRENS | Saída | Transferência externa |
| E0002017 | FUNDO FIXO - GOA (NÃO PASS. COMPR.) | Entrada | Entrada por compra |
| E0002021 | CAPITALIZAÇÃO  SOBRESSALENTES SERIE 8500 | Entrada | Capitalização / outras entradas |
| E0002022 | CAPITALIZAÇÃO  SOBRESSALENTES SERIE 9500 | Entrada | Capitalização / outras entradas |
| E0002023 | CAPITALIZAÇÃO  SOBRESSALENTES SERIE 2500 | Entrada | Capitalização / outras entradas |
| E0002026 | SAÍDA DE MATERIAL STM - SÉRIE 2500 | Saída | Transferência externa |
| E0002027 | SAÍDA DE MATERIAL STM - SÉRIE 8500 | Saída | Transferência externa |
| E0002028 | SAÍDA DE MATERIAL STM - SÉRIE 9500 | Saída | Transferência externa |
| E0002031 | REMESSA MATERIAIS TIC TRENS - SEM INTEGR | Saída | Transferência externa |
| E0002032 | RETORNO DE MATERIAL - VIA MOBILIDADE | Entrada | Transferência externa |
| E0002034 | Dev. de Material Recusado -TIC TRENS | Entrada | Transferência externa |
| E0002273 | RETORNO TRILHOS ENV.P/ INDUSTRIALIZAÇÃO | Entrada | Remessa / empréstimo / retorno |
| E0002279 | ENTRADA POR RETORNO -  INDUSTRIALIZAÇÃO | Entrada | Remessa / empréstimo / retorno |
| E0002353 | RETORNO DE MATERIA PRIMA ENV. P/ INDUSTR | Entrada | Remessa / empréstimo / retorno |

A mesma tabela está em `classificacao_movimentacoes.csv` (separador `;`).
