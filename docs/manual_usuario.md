# Manual do usuário

## Como abrir o painel

1. Copie as planilhas do ERP ALVO para uma pasta do computador (veja `dados/README.md`).
2. Abra `powerbi/LOGTECH_CPTM.pbip` no **Power BI Desktop**.
3. Em **Página Inicial → Transformar dados → Editar parâmetros**, informe a pasta das planilhas no parâmetro **PastaDados** (terminando com `\`).
4. Clique em **Atualizar**.

## Navegação e filtros

- Os **botões no topo** levam a cada página. A página atual fica em vermelho.
- O filtro **Tipo de Consumo** (Essencial, Normal, Estratégico) vale para todas as páginas ao mesmo tempo. Sem seleção, o painel mostra todos os materiais.
- O filtro de **ano** também é sincronizado entre as páginas que o possuem.
- Clicar em uma barra ou linha de qualquer gráfico filtra os outros visuais da página. Clique de novo para limpar.
- Cada página tem um **layout para celular** (Exibir → Layout móvel, ou no aplicativo Power BI Mobile).

## Páginas

| Página | Para que serve | Como usar |
|---|---|---|
| 1. Visão de Estoque | Panorama do estoque: valor, quantidade, Curva ABC, armazéns e top 10 | Clique em um armazém para ver só aquele almoxarifado |
| 2. Indicadores Logísticos | Ruptura, risco, cobertura, giro, excesso e sem consumo | Escolha os limites de risco e de excesso (em meses) nos seletores; a tabela de priorização mostra o que repor primeiro |
| 3. Giro e Rotatividade | Giro por material, tempo de permanência, rotatividade, sazonalidade e ABC × criticidade | Passe o mouse no gráfico de sazonalidade para ver o índice do mês |
| 4. Consumo e Aderência | Histórico de compras e consumo, evolução do estoque e PCA × consumo | Use o filtro de ano para focar em um período |
| 5. Evolução por Material | Histórico completo de um material | **Digite o código ou o nome** no campo de busca e escolha o material; sem seleção a página fica vazia de propósito |
| 6. Reposição | Materiais no ponto de reposição e etapa do processo de compra | Filtre por prioridade; a cor da coluna "Etapa do processo" mostra o gargalo |
| 7. Obsolescência | Materiais obsoletos, valor por almoxarifado e destinação | Use a busca de almoxarifado |
| 8. Metodologia | Fórmulas, fontes, classificação das movimentações e testes | Consulte para explicar qualquer número do painel |

## Regras que o usuário deve conhecer

- **Data de referência:** 24/08/2026 (data da posição da RES47). Os indicadores de "12 meses" usam de 25/08/2025 a 24/08/2026.
- **Consumo efetivo:** apenas saídas por requisição (manutenção, operação, administração e engenharia).
- **Material sem consumo não é obsoleto:** pode ser sobressalente estratégico.
- **Curva ABC não é criticidade:** criticidade = tipo de consumo Essencial ou Estratégico.
