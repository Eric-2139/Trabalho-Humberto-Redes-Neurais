---
paths:
  - "**/*.ipynb"
---

# Estilo do notebook principal

O professor precisa conseguir ler o notebook **sem esforço**. No trabalho anterior ele reclamou de ter que ler 90 células. Clareza também vale nota (10%).

## Estrutura
- Duas partes com cabeçalho `# PARTE A — Dados e MLP` e `# PARTE B — CNN e Transfer Learning`; seções `## A1.` … `## B4.` iguais às do PLAN.md.
- A primeira célula é o cabeçalho: título, autor, link para `relatorio.ipynb`, como executar e sumário (tabela parte → seção → conteúdo).
- Padrão de cada passo: **markdown "o que + por quê" → código → saída → markdown de interpretação** (a interpretação só quando houver algo a concluir).
- Constantes só no A1 e funções reutilizáveis só no A4. Nas demais seções, só chamadas.

## Células de código
- Curtas (idealmente ≤ 40 linhas) e com um propósito por célula.
- Comentários explicam o **porquê**, não o óbvio. Em português.
- `verbose=2` no `fit` (uma linha por época, sem barras de progresso poluindo a saída).
- Sem prints de debug. Cada saída deve ser algo que o professor queira ver.
- A última expressão da célula pode ser um DataFrame/Styler para exibir tabelas (melhor que `print`).

## Markdown
- Títulos curtos. Justificativas em bullets de 1–2 linhas, com termos técnicos em **negrito** na primeira ocorrência.
- Números que dependem da execução levam `✍️` até serem conferidos com a saída real. Nunca invente resultados.
- Tabelas markdown para decisões (decisão | escolha | por quê).

## Gráficos (matplotlib)
- Estilo global definido no A1: grade discreta, sem spines superior/direita, linhas de 2 px.
- Cores fixas: **treino = `#2a78d6` (azul)**, **validação = `#eb6834` (laranja)**, destaque = `#1baf7a`, neutro = `#898781`.
- Matrizes de confusão e heatmaps: colormap sequencial `Blues`, matriz normalizada por linha, valores com 2 casas.
- Todo gráfico tem título e rótulos de eixo em português. Legenda quando houver ≥ 2 séries. Nada de eixo duplo.
