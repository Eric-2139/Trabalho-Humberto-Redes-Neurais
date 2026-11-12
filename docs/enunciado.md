# Enunciado do trabalho (cópia literal, fonte de verdade para requisitos e rubrica)

## Critérios de escolha do dataset
Para caber no escopo, o dataset escolhido pelo aluno deve:

- Ser um problema de classificação de imagens.
- Ter entre 2 e ~10 classes.
- Ter um volume de imagens gerenciável em CPU. Como sugestão: usar um subconjunto de até 5.000 imagens de treino caso o dataset original seja muito grande. Para este caso, justifique o motivo e a forma de como foi criado o subconjunto.
- Ter alguma dificuldade real: classes desbalanceadas, variação de iluminação/ângulo, e/ou classes visualmente parecidas. Datasets como o "dígitos MNIST puro" devem ser evitados ou justificados.

## Escopo do Trabalho

### Exploração e preparação dos dados
- Apresentar o dataset escolhido (origem, classes, quantidade de imagens por classe).
- Análise exploratória: histograma de distribuição de classes, exemplos visuais, dimensões das imagens.
- Pré-processamento: redimensionamento padronizado, normalização, flatten das imagens para entrada da MLP.

### Construção e treinamento da MLP
- Implementar uma MLP simples com pelo menos 1-2 camadas ocultas.
- Justificar escolhas básicas: função de ativação, função de perda, otimizador.
- Treinar e plotar curvas de loss/accuracy (treino vs validação).

### Avaliação
- Calcular accuracy, precision, recall, F1-score e matriz de confusão.
- Se o dataset for desbalanceado, discutir o que essas métricas revelam além da accuracy simples.

### Diagnóstico e ajuste
- Identificar se houve overfitting ou underfitting (usando as curvas de treino/validação).
- Aplicar ao menos uma técnica de regularização (dropout, L2, early stopping) e/ou Data Augmentation, comparando o resultado antes/depois.

### CNN própria (do zero)
- Construir uma CNN simples, com 2-4 camadas convolucionais + pooling + camadas densas finais.
- Treinar com os mesmos dados e comparar accuracy/F1 com a MLP, construida nos passos 2 e 3.
- Discutir por que, caso ocorra, a CNN superou a MLP.

### Transfer Learning com modelo pré-treinado leve
- Aplicar um modelo leve compatível com CPU. Recomendo o uso do MobileNetV2, porém não há impedimento para que outro seja utilizado.
- Etapa 1 (feature extraction): congelar a base pré-treinada e treinar apenas a camada final.
- Etapa 2 (fine-tuning): descongelar as últimas camadas da base e treinar novamente com taxa de aprendizado baixa.

### Comparação final
- Tabela comparativa entre MLP, CNN própria e Transfer Learning: accuracy, F1-score, tempo de treinamento, número de parâmetros.
- Discussão a respeito de qual abordagem valeu mais a pena para esse dataset específico, considerando o resultado, o custo computacional (CPU) e o tamanho do dataset.

## Critérios de avaliação

| Critério | Peso |
|---|---|
| Preparação e justificativa dos dados | 5% |
| Implementação correta da MLP | 15% |
| Uso e interpretação correta das métricas | 15% |
| Diagnóstico de overfitting/desbalanceamento + aplicação de técnica de correção | 10% |
| Implementação correta da CNN própria | 10% |
| Implementação correta do Transfer Learning (feature extraction) | 15% |
| Comparação justa e bem executada | 10% |
| Qualidade da análise comparativa (tabela + discussão) | 10% |
| Clareza e conclusão do relatório | 10% |

## Entregável
- Notebook Colab, comentado e organizado, dividido em duas seções claras contendo todos os pontos ilustrados no escopo do trabalho.
- Relatório curto em markdown no início do próprio notebook com: descrição do dataset, decisões tomadas, métricas finais, conclusão sobre limitações da MLP para esse problema, tabela comparativa entre MLP, CNN própria e Transfer Learning, e conclusão final sobre qual modelo o aluno recomendaria para o problema apresentado.
- Envio do link compartilhado do colab e do notebook .ipynb como anexo.
