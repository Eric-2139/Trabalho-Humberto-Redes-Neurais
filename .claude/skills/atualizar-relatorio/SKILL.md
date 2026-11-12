---
name: atualizar-relatorio
description: Cria ou atualiza relatorio.ipynb (relatório detalhado para o professor, markdown + código que carrega as tabelas) a partir dos CSVs de outputs/ e das conclusões do notebook principal executado. Use na fase R, ou depois de uma nova execução completa que mude os resultados.
disable-model-invocation: true
---

# /atualizar-relatorio

## Pré-condições (verifique e pare se faltar algo)
- `outputs/resultados_eurosat.csv` existe e é mais recente que `trabalho_eurosat.ipynb`. Caso contrário, peça para rodar `/executar-notebook completo` (a execução local é a oficial).

## Passos
1. Leia `.claude/rules/relatorio.md`: estrutura obrigatória e regras.
2. Leia os CSVs e os markdowns de interpretação do notebook executado (A5, A6, B1, B4), que são as conclusões já revisadas.
3. Monte ou atualize `relatorio.ipynb` com **NotebookEdit**, na ordem das 7 seções da regra: markdown para o texto e células de código só para carregar/exibir as tabelas dos CSVs.
   - A tabela comparativa sai do CSV: modelo | accuracy | F1-macro | tempo de treino (s) | parâmetros totais | parâmetros treináveis.
   - Números com 3 casas para métricas, segundos inteiros para tempo e separador de milhar `.` para parâmetros.
4. Confira cada número do relatório contra o CSV, um a um, e liste as divergências encontradas.
5. Rode o agente `revisor-rubrica` sobre o relatório (critério "Clareza e conclusão do relatório", 10%).
6. Mostre ao aluno: o que mudou, a tabela final e os pontos que ele precisa preencher (link do Colab). **Pare** para aprovação.
