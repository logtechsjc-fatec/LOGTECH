# Testes de consistência

Os testes abaixo são calculados por medidas DAX na página **Metodologia** e se atualizam junto com as bases. Os resultados indicados são os obtidos com as bases de agosto de 2026.

| Nº | Teste | Resultado | Como ler |
|---|---|---|---|
| 1 | Linhas da RES34 sem cadastro na PROD | 0 | Todos os materiais do estoque estão no cadastro |
| 2 | Linhas da RES82 sem material na PROD | 6.083 | Compras diretas de fundo fixo (códigos 5.02), não estocáveis |
| 3 | Tipos de movimentação sem classificação | 0 | Os 98 tipos foram classificados |
| 4 | Materiais na RES47 que não estão na RES34 | 315 | Diferença entre as duas fotografias do estoque |
| 5 | Diferença de valor RES47 − RES34 | ≈ R$ 7,2 mi | A mesma diferença, em valor |
| 6 | Consumo 2025: RES82 ÷ RES75 (2025 MOV) | ≈ 100% | Confirma a classificação do consumo efetivo |
| 7 | Materiais com saldo negativo ao reconstruir ago/2025 | 120 | Menos de 1,5% dos materiais; movimentos a revisar |
| 8 | RMs da base 8 encontradas na RES82 | ≈ 93,6% | A ligação pelo número da movimentação funciona |

Os mesmos números podem ser conferidos fora do Power BI com o script `scripts/validar_indicadores.py`.
