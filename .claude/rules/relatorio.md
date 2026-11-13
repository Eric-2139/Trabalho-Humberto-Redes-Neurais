---
paths:
  - "relatorio.ipynb"
---

# Relatório (`relatorio.ipynb`)

Leitor: o **professor**, que quer as conclusões e a análise sem abrir o notebook principal.
Decisão dos alunos (2026-11-09): relatório **separado e detalhado**, que **carrega as tabelas de resultados** exportadas pelo notebook principal.

## Estrutura (ordem do roteiro da apresentação, decidida em 2026-11-13)
0. Cabeçalho: título, alunos (Eric Costa Ciciliotti e Yuri Martinelli), professor, disciplina, link do Colab, referência ao `trabalho_eurosat.ipynb`, resumo e roteiro; depois, o carregamento dos CSVs e das figuras.
1. **Apresentação do dataset**: qual dataset e por quê (origem real: Zenodo); classes e quantidades; principais desafios.
2. **Produto 1: MLP**: 2.1 preparação dos dados (subconjunto, split, pré-processamento, normalização) · 2.2 arquitetura e decisões (ativação, perda, otimizador) · 2.3 métricas e o que revelam (com a explicação de "macro" e a matriz de confusão) · 2.4 diagnóstico de overfitting/underfitting pelas curvas · 2.5 regularização e data augmentation, com o efeito observado e as **limitações da MLP**.
3. **Produto 2: CNN e Transfer Learning**: 3.1 arquitetura da CNN e comparação com a MLP · 3.2 feature extraction e fine-tuning · 3.3 tabela comparativa final (accuracy, F1, tempo de treino, parâmetros totais e treináveis).
4. **Conclusão**: modelo recomendado e por quê (desempenho × custo em CPU × tamanho do dataset), principal dificuldade e aprendizado, limitações do estudo.

Os itens do "Entregável" do enunciado (descrição do dataset, decisões, métricas finais, limitações da MLP, tabela comparativa, recomendação) continuam todos presentes, distribuídos nessa ordem.

## Regras
- Markdown para o texto; **células de código só para carregar e exibir** as tabelas (dos CSVs de `outputs/`) e as figuras (lidas do `trabalho_eurosat.ipynb` executado pela função `figura(id_da_célula)`). Nada de treino, de recálculo de métricas nem de gráfico redesenhado no relatório.
- Cada figura tem uma legenda numerada ("Figura N") com a seção de origem e o que ela sustenta na tabela vizinha. Interpretações citam a figura quando dependem dela.
- Detalhado, mas organizado: seções com títulos claros, tabelas em vez de parágrafos sempre que possível.
- Todo número vem dos CSVs exportados pelo notebook principal ou de uma saída citada dele. Tempos vêm da **execução completa local** (execução oficial).
- Números citados no texto precisam bater com as tabelas carregadas.
- Nada que não esteja sustentado por uma saída do notebook principal.
- Se houver divergência entre relatório e notebook, o notebook é a fonte de verdade: corrija o relatório.
