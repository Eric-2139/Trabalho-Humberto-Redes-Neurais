---
paths:
  - "relatorio.ipynb"
---

# Relatório (`relatorio.ipynb`)

Leitor: o **professor**, que quer as conclusões e a análise sem abrir o notebook principal.
Decisão dos alunos (2026-11-09): relatório **separado e detalhado**, que **carrega as tabelas de resultados** exportadas pelo notebook principal.

## Conteúdo obrigatório (seção "Entregável" do enunciado)
1. Cabeçalho: título, alunos (Eric Costa Ciciliotti e Yuri Martinelli), professor, disciplina, link do Colab e referência ao `trabalho_eurosat.ipynb`.
2. **Descrição do dataset**: origem, classes, quantidade, subconjunto usado e por quê, dificuldades.
3. **Decisões tomadas**: tabela decisão | escolha | justificativa (split, pré-processamento, arquiteturas, regularização, métricas, CPU).
4. **Métricas finais**: accuracy, precision, recall e F1-macro no teste, por modelo.
5. **Limitações da MLP** para este problema (flatten, ausência de invariância a translação, parâmetros), com evidência numérica.
6. **Tabela comparativa** MLP × CNN × TL: accuracy, F1, tempo de treino e nº de parâmetros (totais e treináveis).
7. **Conclusão e recomendação**: qual modelo e por quê (desempenho × custo em CPU × tamanho do dataset), mais as limitações do estudo.

## Regras
- Markdown para o texto; **células de código só para carregar e exibir** as tabelas (e eventualmente gráficos) a partir dos CSVs de `outputs/`. Nada de treino nem de recálculo de métricas no relatório.
- Detalhado, mas organizado: seções com títulos claros, tabelas em vez de parágrafos sempre que possível.
- Todo número vem dos CSVs exportados pelo notebook principal ou de uma saída citada dele. Tempos vêm da **execução completa local** (execução oficial).
- Números citados no texto precisam bater com as tabelas carregadas.
- Nada que não esteja sustentado por uma saída do notebook principal.
- Se houver divergência entre relatório e notebook, o notebook é a fonte de verdade: corrija o relatório.
