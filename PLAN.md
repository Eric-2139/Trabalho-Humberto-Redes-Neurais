# PLAN — Trabalho de Redes Neurais: EuroSAT RGB (MLP × CNN × Transfer Learning)

> Documento vivo. É a visão geral do que será feito, em que ordem e com que critério de "pronto".
> Atualizado ao fim de cada fase: status, decisões novas e entrada no log.
> Requisitos e rubrica oficiais: [docs/enunciado.md](docs/enunciado.md).

**Status atual:** Parte A ✅ · Parte B ✅ · X ✅ (local) · **R (relatório) 👀 aguardando aprovação dos alunos**

---

## 1. Objetivo

Comparar três abordagens de classificação de imagens no **EuroSAT RGB** (10 classes de uso do solo, imagens de satélite 64×64), sob o mesmo protocolo e em **CPU**:

1. **MLP** (imagem achatada em vetor) → baseline + diagnóstico de overfitting + regularização
2. **CNN própria** (do zero)
3. **Transfer Learning** com MobileNetV2 (etapa 1: feature extraction · etapa 2: fine-tuning)

E concluir **qual abordagem vale mais a pena** considerando desempenho, custo computacional e tamanho do dataset.

## 2. Entregáveis

| Arquivo | Conteúdo | Para quem |
|---|---|---|
| `trabalho_eurosat.ipynb` | Implementação completa: Parte A (dados + MLP) e Parte B (CNN + TL + comparação) | Professor (detalhes) / Colab |
| `relatorio.ipynb` | Relatório **detalhado**, separado: dataset, decisões, métricas finais, limitações da MLP, tabela comparativa, recomendação. Markdown + células de código que **carregam as tabelas de resultados** exportadas pelo notebook principal (`outputs/*.csv`) | Professor (leitura principal) |
| Link do Colab | Notebook principal no Colab (runtime CPU) | Envio |

## 3. Decisões já tomadas

| Decisão | Escolha | Justificativa |
|---|---|---|
| Dataset | EuroSAT RGB (Zenodo 7711810; espelho HF `torchgeo/eurosat`) | 10 classes, classes visualmente parecidas, leve desbalanceamento, imagens pequenas → viável em CPU |
| Subconjunto | 5.000 treino / 1.000 validação / 2.000 teste, **estratificado**, seed 42 | Limite sugerido pelo enunciado; teste maior reduz o ruído das métricas |
| Framework | **Keras 3** (`import keras`) com backend TensorFlow | API de alto nível (`fit`/`predict`), análoga ao sklearn; TF é o motor |
| Hardware | CPU forçada (`CUDA_VISIBLE_DEVICES=-1`) | O enunciado compara custo em CPU |
| Resolução | 64×64 nativa para MLP/CNN; `Resizing(96)` **dentro** do modelo de TL | Todos recebem o mesmo array; 96 é o menor tamanho com pesos ImageNet |
| Pré-processamento | Dentro do modelo (`Rescaling`, `Flatten`, augmentation) | Equivale ao `Pipeline` do sklearn: sem divergência entre treino e teste |
| Métrica principal | **F1-macro** (+ accuracy, precision, recall, matriz de confusão) | 10 classes com desbalanceamento leve; cada classe pesa igual |
| Seleção de modelo | Sempre pela **validação**; teste só para reportar | Mesmo protocolo do TCC |
| Relatório | Notebook separado `relatorio.ipynb`, **detalhado**, com células de código que carregam as tabelas de resultados do notebook principal | O professor reclamou de ter que ler ~90 células no trabalho anterior; decidido pelos alunos mesmo o enunciado citando "no início do próprio notebook" |
| Execução oficial | **Local** (AMD Ryzen 7 7435HS, 16 threads, CPU) | Todos os números, tempos, textos ✍️ e o relatório vêm da execução completa local |
| Cabeçalho | Alunos: Eric Costa Ciciliotti e Yuri Martinelli · Professor: Humberto Tozetti · Disciplina: Desenvolvimento de Aplicação para Reconhecimento e Interpretação de Imagens | — |
| Orçamento de épocas | `MAX_EPOCHS = 40` (MLP/CNN) · `TL_EPOCHS = 15` por etapa do TL | 40 dá espaço para o overfitting da MLP aparecer nas curvas; a MobileNetV2 converge rápido e cada época custa muito mais em CPU |
| Batch size | `BATCH_SIZE = 64` para todos os modelos | ~79 atualizações por época com 5.000 imagens; bom equilíbrio velocidade × estabilidade em CPU |
| Early stopping | `PATIENCE = 8` (MLP/CNN) · `TL_PATIENCE = 4` (TL) | ~20–25% do orçamento: tolera oscilações da `val_loss` sem desperdiçar épocas |
| Taxas de aprendizado | Adam `LR = 1e-3` (padrão) · `LR_FINE_TUNE = 1e-5` | Padrão do Adam para treino do zero e para a cabeça do TL; lr 100× menor no fine-tuning para não destruir os pesos do ImageNet |
| ES no baseline | MLP baseline (A5) **sem** early stopping (40 épocas inteiras); todos os demais modelos **com** ES | O baseline é o "antes" do diagnóstico: mostra o overfitting completo nas curvas. ES é uma das técnicas de regularização do A6. A MLP que vai para a comparação final é a melhor pela validação |
| Conjuntos avaliados | `evaluate_model` mede **validação e teste** de cada modelo; matriz de confusão e relatório por classe saem do teste | Todas as escolhas usam só métricas de validação; o teste é apenas reportado |
| Data augmentation | `RandomFlip("horizontal")` + `RandomFlip("vertical")` + `RandomRotation(0.25, fill_mode="reflect")` (±90°), sementes SEED, SEED+1, SEED+2 | Cenas de satélite não têm orientação fixa; reflect evita bordas pretas. Flips separados e sementes distintas: a camada única "horizontal_and_vertical" só gerava 2 das 4 orientações e sementes iguais correlacionavam flip e rotação (conferido empiricamente na A4) |
| Arquitetura da MLP | `Rescaling(1/255)` → `Flatten` → `Dense(256, relu)` → `Dense(128, relu)` → `Dense(10, softmax)` (~3,18 M parâmetros) | 2 camadas ocultas (o enunciado pede 1–2); capacidade suficiente para o overfitting aparecer e o A6 ter o que corrigir; ~1–2 min em CPU |
| Ativação das ocultas | **ReLU** | Não satura para valores positivos, é barata e é a mesma da CNN (comparação limpa); padrão do `MLPClassifier` |
| Função de saída | **softmax** com 10 neurônios, em **todos** os modelos (MLP, CNN, TL) | Converte as saídas em probabilidades que somam 1; par natural da entropia cruzada (`sparse_categorical_crossentropy`). Decidido pelos alunos em 2026-11-10 |
| Variantes do A6 | baseline (A5) · **MLP + ES** · **MLP + ES + dropout** · **MLP + ES + L2** · **MLP + ES + augmentation**; todas com `construir_mlp` (mesma arquitetura e mesmos pesos iniciais) | A variante só-ES isola o ganho de escolher a melhor época; as outras medem o efeito adicional de cada técnica isolada. Dropout e L2 separados em 2026-11-11 (antes eram uma variante combinada) porque um diagnóstico mostrou efeitos opostos: só dropout F1 val 0,339, só L2 0,503, combinados 0,184. Escolha da MLP para a B4 por `val_f1_macro` |
| Intensidade da regularização | `DROPOUT_MLP = 0.3` (após cada oculta) · `L2_MLP = 1e-4` (kernels das ocultas) | Regularização leve, porque o baseline tem underfitting; valores fortes tenderiam a piorar o ajuste |
| Arquitetura da CNN | `Rescaling(1/255)` → 3 blocos [`Conv2D(3×3, same, relu)` → `MaxPool(2×2)`] com 32 → 64 → 128 filtros → `GlobalAveragePooling2D` → `Dense(128, relu)` → `Dense(10, softmax)` (~111 mil parâmetros, ~29× menos que a MLP) | 3 camadas conv (o enunciado pede 2–4); três reduções 64→32→16→8 dão campo de visão para estradas, rios e talhões; GAP evita o Flatten gigante |
| Augmentation na CNN | Duas variantes, **CNN + ES** e **CNN + ES + augmentation**, escolha da CNN para a B4 por `val_f1_macro` | Mesmo processo de seleção da MLP: nenhum modelo leva vantagem por ter mais opções; a comparação não mistura arquitetura com augmentation |
| Cabeça do TL (B2) | MobileNetV2 congelada → `GlobalAveragePooling2D` → `Dense(10, softmax)` (12.810 parâmetros treináveis) | É literalmente "treinar apenas a camada final" do enunciado; equivale a usar a base como extrator fixo de features + regressão logística. Decidido pelos alunos em 2026-11-12 |
| Augmentation no TL (B2) | Duas variantes, **TL + ES** e **TL + ES + augmentation**, escolha da etapa 1 por `val_f1_macro` | Mesmo processo de seleção da MLP e da CNN. Decidido pelos alunos em 2026-11-12 |
| Fine-tuning (B3) | As **duas** variantes da B2 passam pelo fine-tuning (TL-FT + ES e TL-FT + ES + augmentation), cada uma partindo dos seus pesos da etapa 1; descongela as convoluções a partir de `block_14_expand` (29 camadas; **BatchNorm continuam congeladas**: 1.510.720 parâmetros da base + 12.810 da cabeça = 1.523.530 treináveis); TL final = maior `val_f1_macro` entre `MELHOR_TL_FE` e as duas FT | Testa a hipótese da B2 (augmentation só ajuda quando a base se adapta) e dá um regularizador ao fine-tuning, que treina ~120× mais parâmetros que a etapa 1. Mesmo processo de seleção dos outros modelos. Decidido pelos alunos em 2026-11-12 |
| Tabela final (B4) | Tabela principal com `MELHOR_MLP`, `MELHOR_CNN` e `MELHOR_TL`; anexo compacto com as 11 variantes; CSV com as 11 linhas e a coluna que marca as 3 da comparação | Atende o enunciado sem esconder o processo de seleção (feito só pela validação). Decidido pelos alunos em 2026-11-12 |
| Recomendação (B4) | **TL-FE** (MobileNetV2 congelada + Dense(10)); CNN como alternativa só se a inferência for o gargalo; MLP descartada | +15 pts de F1 sobre a CNN com custo de treino na mesma ordem e 12.810 parâmetros treinados; fine-tuning empatou com custo ~40% maior. Decidido pelos alunos em 2026-11-12 |
| CSVs no Colab (R) | `relatorio.ipynb` entregue **já executado** localmente (tabelas visíveis sem rodar); se reexecutado sem `outputs/`, uma célula explica como anexar os CSVs | Simples e sem link externo. Decidido pelos alunos em 2026-11-12 |
| Resumo no cabeçalho (R) | Bloco curto no cabeçalho do `trabalho_eurosat.ipynb`: tabela final dos 3 modelos + recomendação em uma frase + link para o relatório | Atende a leitura literal do enunciado ("no início do próprio notebook") sem duplicar o relatório. Decidido pelos alunos em 2026-11-12 |

## 4. Pontos em aberto

- [x] ~~Local do relatório~~ → `relatorio.ipynb` separado e detalhado (decidido em 2026-11-09).
- [x] ~~Nomes no cabeçalho~~ → ver §3.
- [x] ~~Execução oficial dos números~~ → local (decidido em 2026-11-09).
- [ ] Link do Colab (gerado na fase E): preencher o ✍️ no cabeçalho do `relatorio.ipynb`.
- [ ] **E (revisão da R):** o `trabalho_eurosat.ipynb` da raiz está **sem saídas**; o anexo e o Colab devem usar a versão executada (`outputs/trabalho_eurosat_executado.ipynb`, já com os textos finais sincronizados) ou uma reexecução no Colab. O link relativo `relatorio.ipynb` no cabeçalho do notebook principal não abre no Colab: trocar pelo link compartilhado do relatório. O `relatorio.ipynb` vai executado (decisão da R).
- [x] ~~Fase R/E: como o `relatorio.ipynb` acessa os CSVs quando aberto no Colab~~ → entregue já executado (§3) (anexar `outputs/`, Drive ou URL). Decidir na fase R. A B4 grava `resultados_eurosat.csv`, `f1_por_classe_eurosat.csv` (longo: modelo, abordagem, classe, conjunto, f1) e `execucao_eurosat.csv` (modo, split, assinatura, versões, escolhidos): o relatório deve conferir `modo == completo` e a assinatura `25d314761ce3`.
- [x] **R (revisão da B4):** → resumo curto no cabeçalho (§3). O enunciado pede o relatório "no início do próprio notebook"; considerar um bloco curto no cabeçalho do `trabalho_eurosat.ipynb` com a tabela final resumida e a recomendação, mantendo o `relatorio.ipynb` como leitura detalhada.

**Pendências herdadas da revisão do A2:**
- [x] ~~**A3:** `assert` de hashes disjuntos~~ → feito na célula do split.

**Pendências herdadas da revisão do A3:**
- [x] ~~**B2:** o `keras.Input` do modelo de TL **não** recebe `dtype="uint8"` (padrão float32); senão o `Resizing` arredonda a interpolação. Alternativa equivalente: `Rescaling` antes do `Resizing`.~~ → feito (Input float32).
- [ ] **E (parte local feita na X):** conferir no Colab que a assinatura do split é `25d314761ce3` (mesma da execução local); conferir os números da A3 (0,06 pp; 61,4/12,3/24,6 MB) na execução oficial; conferir o ✍️ da estimativa de tempo do TL.
- [x] ~~**A5:** hipótese do A2~~ → feito: agrícolas parcial, Highway × River confirmada, maiores confusões seguem a cor média.
- [x] ~~**B1:** a CNN reduz as confusões de cor?~~ → sim (≤ ~0,08); sobram Highway → River (0,319) e PermanentCrop → HerbaceousVegetation (0,258).
- [x] **B4/relatório:** limitação a citar: o MD5 só pega duplicatas exatas; recortes vizinhos da mesma região podem cair em conjuntos diferentes (correlação espacial), deixando as métricas um pouco otimistas. → **feito na discussão da B4 (limitações)**

**Pendências herdadas da revisão do A5 (para o A6):**
- [x] ~~Desenho do A6~~ → decidido com os alunos (4 variantes isoladas).
- [x] ~~Variante só com ES~~ → incluída.
- [x] ~~Comparar por F1, não pela loss (penalidade L2)~~ → dito no markdown.
- [x] ~~Curva de treino com dropout/augmentation~~ → explicado na A4 (accuracy de treino pode ficar **abaixo** da de validação).
- [x] **X:** duas execuções completas locais deram métricas idênticas (val_loss mínima 1,4657 na época 26 nas duas); só o tempo variou (81,6 s × 88,5 s). Reconferir os números do A5 na execução oficial. → **feito na execução oficial (2026-11-12 17:41): val_loss mínima 1,4657 na época 26, números do A5 conferidos**

**Pendências herdadas da revisão do A6:**
- [x] ~~**B1:** augmentation na CNN~~ → CNN e CNN + aug, escolha pela validação. **B2:** decidir o mesmo para o TL.
- [x] **B4/relatório:** a tabela final usa a variável `MELHOR_MLP` (não um nome fixo) e o relatório diz qual MLP entrou; `RESULTS` tem 5 linhas de MLP. As confusões "de cor" da B1/B4 devem ser comparadas com `MATRIZES[MELHOR_MLP]` (ou dizer que a referência é o baseline). → **feito: a B4 usa `FINALISTAS` com as variáveis de seleção; o relatório (R) diz qual variante entrou**
- [x] **B4:** tempos de treino são ruidosos (o baseline mediu 81,6 · 88,5 · 100,2 s em três execuções). Comparar custo por ordem de grandeza e por épocas, não por diferenças pequenas de segundos. → **feito: B4 compara por ordem de grandeza, épocas e tempo por época**
- [x] **X:** conferir que `MELHOR_MLP` continua "MLP + ES + augmentation" (empate com L2: 0,507 × 0,503) e os números citados na A6. → **feito: MLP + ES + augmentation (0,5066 × L2 0,5027); números da A6 conferidos**

**Pendências herdadas da revisão da B1:**
- [x] ~~**B2 (decisão dos alunos):** augmentation no TL~~ → TL e TL + aug, escolha pela validação (2026-11-12).
- [x] **B4:** `RESULTS` terá ~9 linhas (5 MLP, 2 CNN, TL etapa 1, TL etapa 2). A tabela final seleciona explicitamente `[MELHOR_MLP, MELHOR_CNN, <TL escolhido>]` e o CSV marca quais linhas entram na comparação. Números "no orçamento de 40 épocas" (MLP e CNN com augmentation não convergiram: pesos das épocas 39 e 35). → **feito: 11 linhas; tabela final por `FINALISTAS`; CSV com `na_comparacao_final`**
- [x] **B4:** custo por época: MLP ~2,3–2,7 s, CNN ~5,9–6,3 s (execução local). → **feito: coluna "tempo por época" na tabela final**

**Pendências herdadas da B2 (decisões e revisão de 2026-11-12):**
- [x] ~~Decisões da B2~~ → cabeça `GAP → Dense(10)`, variantes TL-FE + ES e TL-FE + ES + aug, execução completa autorizada (ver §3).
- [x] ~~Lembretes do protocolo da B2~~ → `keras.Input` float32, `Resizing(96)` + `Rescaling` [−1, 1], `trainable=False` + `training=False`, `TL_EPOCHS`/`TL_PATIENCE`, etapa 1 avaliada sozinha, parâmetros totais e treináveis, nomes `"TL-FE ..."`.
- [x] **B3:** restaurar `modelos_tl[MELHOR_TL_FE].set_weights(PESOS_TL_FE)` antes de descongelar (a célula fica reexecutável e a etapa 1 nunca é sobrescrita); nome novo no `RESULTS` (`"TL-FT ..."`); `evaluate_model(modelo, nome_ft, [treinos_tl[MELHOR_TL_FE], treino_ft])`. → **feito na B3**
- [x] **B3:** **achado de 2026-11-12:** no Keras 3.15, o `fit` de um modelo funcional sobrescreve o `base(x, training=False)` (a `operation_fn` injeta o `training` externo); com as BN descongeladas, as `moving_mean`/`moving_variance` mudavam no teste. Correção: as BatchNorm da região descongelada ficam com `trainable=False` (prática padrão), e um assert prova que as estatísticas não mudam. A B2 não foi afetada (base inteira com `trainable=False`); os textos dela foram corrigidos. → **feito na B3 (BN congeladas + demonstração)**
- [x] **B3:** a B2 mostrou overfitting leve da cabeça (treino 0,986 × val 0,918) e nenhum ganho do augmentation (0,916 × 0,900, empate). Discutir se o fine-tuning amplia o overfitting. → **feito na B3**
- [x] **B4/relatório:** custo do TL-FE é ponta a ponta (a base recalcula as features a cada época, ~13,6 s/época). Com cache das features, o treino seria ~15 s (estimativa, não medida). O custo do pré-treino no ImageNet não entra na conta. Inferência: TL ~2,2 ms/imagem × CNN ~0,34 × MLP ~0,10. → **feito na discussão da B4 (cache de features e pré-treino)**
- [x] **X:** duas execuções completas da B2 (2026-11-12) deram métricas idênticas (TL-FE + ES: F1 val 0,916 · teste 0,902), mas tempos diferentes: CNN + aug 239 → 204 s, TL-FE + aug 208 → 224 s, inferência do TL 2,2 → 2,4 ms. Os textos da B2 usam faixas. Na execução oficial, conferir o "~250 s × ~110 s" da B1 (cc31e3a1) e as faixas da B2. → **feito: textos da B1–B4 usam faixas que contêm os tempos da execução oficial**
- [x] **B4 (revisão da B3):** `RESULTS` tem **11 linhas** (5 MLP, 2 CNN, 2 TL-FE, 2 TL-FT). A tabela final usa `MELHOR_MLP`, `MELHOR_CNN` e **`MELHOR_TL`** (não `MELHOR_TL_FE`/`MELHOR_TL_FT`); treináveis = 12.810 se for etapa 1, 1.523.530 se for fine-tuning. Em empate exato, `idxmax` fica com a etapa 1 (primeira da lista). No fine-tuning, `tabelas_comparacao` mostra tempo por época = média das duas etapas; para custo, citar a etapa 2 sozinha a partir de `treinos_ft`. → **feito na B4 (`MELHOR_TL`; empate decidido por 0,0004 na validação)**
- [x] **B4/relatório (resultado da B3):** fine-tuning **empatou** com a etapa 1 (F1 val 0,916 × 0,916; FT + aug 0,912), `MELHOR_TL` = TL-FE + ES. FT sem aug só aprofunda o overfitting (val_loss sobe desde a 1ª época); com aug, +1,2 pt (ruído, direção da hipótese da B2). Custo do FT: etapa 2 78–98 s (~15–16 s/época), total 284–303 s (~40% a mais), 1.523.530 treináveis. Erros inalterados. Limitação a citar: pares Highway ↔ River e PermanentCrop → HerbaceousVegetation parecem ambíguos em 64×64 RGB (mais resolução ou bandas do EuroSAT multiespectral ficariam fora do escopo). → **feito na B4 (discussão e anexo)**
- [x] **X:** 3ª execução completa (2026-11-12): métricas idênticas da A5 à B2; tempos variaram de novo (CNN + aug 206 s, TL-FE ~206 s). Conferir faixas de tempo na execução oficial. → **feito: faixas conferidas na execução oficial**
- Medições: pesos `mobilenet_v2_1.0_96_no_top` (9 MB, cache em `~/.keras`); base com **2.257.984 parâmetros**, 154 camadas, `block_14_expand` no índice 125; saída 3×3×1280.

## 5. Protocolo experimental (vale para todos os modelos)

1. Split **uma única vez**, estratificado, seed fixa, com checagem de duplicatas (MD5) antes do split.
2. Mesmos `X_train / X_val / X_test` (`uint8`, 64×64×3) para todos os modelos.
3. Mesma perda (`sparse_categorical_crossentropy`), mesmo otimizador (Adam), mesmo batch e o mesmo critério de parada (early stopping em `val_loss`, restaurando a melhor época), **exceto o baseline da MLP**, que roda sem ES para servir de "antes" no diagnóstico (a MLP comparada na B4 tem ES). Orçamento: 40 épocas/paciência 8 para MLP e CNN; 15 épocas por etapa/paciência 4 no TL (parte de pesos treinados), justificado no A1.
4. Mesmas funções `train_model` / `evaluate_model`; a tabela final sai de `RESULTS`.
5. Medidos para cada modelo: accuracy, precision/recall/F1 (macro), F1 por classe, matriz de confusão, tempo de treino, tempo de inferência, parâmetros totais e treináveis.
6. **Modo smoke** (`SMOKE_TEST=1`): mesmo código com poucos dados e 1–2 épocas, para validar o notebook em ~2 min antes da execução completa.

## 6. Workflow por fase

Ciclo de cada fase: **escopo combinado → células escritas → smoke test → revisão (agentes) → explicação ao aluno → aprovação → ✅ + log**.
Nenhuma fase começa sem aprovação da anterior.

| # | Fase | O que entra | Critério de pronto | Rubrica | Status |
|---|---|---|---|---|---|
| 0 | Harness e ambiente | uv + `.venv`, CLAUDE.md, PLAN.md, rules, agents, skills, hook | ambiente importa TF/Keras; hook valida notebook | — | ✅ |
| A1 | Setup | imports, constantes, seed, CPU forçada, modo smoke, estilo dos gráficos, info de hardware | roda sem erro; constantes num só lugar | — | ✅ |
| A2 | Dataset + EDA | download idempotente, inventário, duplicatas, dimensões, histograma de classes, grade de exemplos, imagem média por classe | todos os itens de "Exploração" do enunciado presentes e comentados | 5% | ✅ |
| A3 | Subconjunto + split + pré-processamento | split estratificado 5k/1k/2k, tabela de proporções, carga em memória, explicação de resize/normalização/flatten | justificativa do subconjunto escrita; sem vazamento | 5% | ✅ |
| A4 | Funções utilitárias | `make_augmentation`, `train_model`, `plot_history`, `evaluate_model`, `top_confusions` | reutilizáveis por todos os modelos | (base) | ✅ |
| A5 | MLP baseline + métricas | arquitetura justificada, treino de 40 épocas sem regularização, curvas, métricas + matriz de confusão + interpretação | ativação/perda/otimizador justificados; interpretação além da accuracy | 15% + 15% | ✅ |
| A6 | Diagnóstico + regularização | diagnóstico pelas curvas; MLP com dropout+L2+ES; MLP + augmentation; tabela antes × depois; limitações da MLP | técnica aplicada e comparada pela validação | 10% | ✅ |
| B1 | CNN própria | 3 blocos conv+pool, GAP, densas; mesmo protocolo; comparação com a MLP; "por que a CNN ganhou" | 2–4 camadas conv; discussão baseada nos resultados | 10% | ✅ |
| B2 | TL — feature extraction | MobileNetV2 congelada, `Rescaling` para [−1, 1], `training=False`, só a cabeça treina | base congelada comprovada (parâmetros treináveis) | 15% | ✅ |
| B3 | TL — fine-tuning | descongela a partir de `block_14_expand`, lr 1e-5, recompila, curvas das 2 etapas | lr baixa; etapas encadeadas no gráfico | (15%) | ✅ |
| B4 | Comparação final | tabela (acc, F1, tempo, parâmetros), gráfico desempenho × custo, F1 por classe, discussão + recomendação | tabela com os 4 itens exigidos + discussão de custo | 10% + 10% | ✅ |
| X | Execução completa | roda o notebook inteiro **localmente** (execução oficial, CPU); confere textos ✍️ com as saídas; depois valida no Colab | sem erros; textos batem com os números | — | ✅ |
| R | Relatório | `relatorio.ipynb` detalhado: markdown + código que carrega as tabelas de `outputs/*.csv` | todos os itens do "Entregável"; números idênticos aos do notebook | 10% | 👀 |
| E | Entrega | upload no Colab, execução em CPU, link compartilhado, `.ipynb` anexado | link funcionando | — | ⬜ |

Legenda: ⬜ a fazer · 🔄 em andamento · 👀 aguardando aprovação · ✅ concluída

### Tempo estimado de execução (CPU)
| Etapa | Local (16 threads) | Colab CPU (2 vCPUs) |
|---|---|---|
| Smoke test (notebook inteiro) | ~2–3 min | ~5 min |
| MLPs (3 variações) | ~2 min | ~5 min |
| CNN | ~5 min | ~10–15 min |
| TL etapa 1 + etapa 2 | ~10 min | ~20–30 min |

## 7. Mapa rubrica → onde é atendida

| Critério (peso) | Seções |
|---|---|
| Preparação e justificativa dos dados (5%) | A2, A3 |
| Implementação correta da MLP (15%) | A5 |
| Uso e interpretação das métricas (15%) | A4 (`evaluate_model`), A5, B4 |
| Diagnóstico overfitting/desbalanceamento + correção (10%) | A5 (desbalanceamento), A6 |
| CNN própria (10%) | B1 |
| Transfer Learning — feature extraction (15%) | B2 (+ B3) |
| Comparação justa (10%) | §5 deste plano, A4, B4 |
| Análise comparativa (10%) | B4 |
| Clareza e conclusão do relatório (10%) | R |

## 8. Log

| Data | Fase | Registro |
|---|---|---|
| 2026-11-09 | 0 | Dataset (EuroSAT RGB), estrutura em duas partes e relatório separado definidos. Ambiente uv criado (Python 3.12, TF 2.21, Keras 3.15). Harness do Claude Code configurado. Rascunho completo descartado: construção será fase por fase. |
| 2026-11-09 | A1 | Notebook criado com cabeçalho e setup (imports, CPU forçada, constantes, estilo, ambiente). Decididos: 40 épocas/paciência 8 (MLP/CNN), 15 por etapa/paciência 4 (TL), batch 64, Adam 1e-3 / FT 1e-5. Revisão: CSV separado no smoke, texto "mesmo orçamento" corrigido. Decididos também: relatório separado e detalhado (com código que carrega as tabelas), execução oficial local, nomes no cabeçalho. Smoke ok. Aprovada. |
| 2026-11-09 | A2 | Dataset + EDA: leitura direta do zip (extrair levava ~4,5 min no Windows × ~6–12 s do zip), inventário, distribuição (razão 1,5), dimensões (todas 64×64 RGB), MD5 (0 duplicatas), grade de exemplos, imagem média + RGB médio, hipótese de confusões, síntese. Revisão: pares "parecidos" coerentes e tratados como hipótese, download à prova de interrupção, sanidade do zip. Adicionado parágrafo "descritivo × ajustado" sobre vazamento (pedido dos alunos) e regra correspondente em protocolo-ml.md. Aprovada. |
| 2026-11-09 | A3 | Split estratificado 5.000/1.000/2.000 em duas etapas (seed 42), assert de MD5 disjunto, `del X_todas`, assinatura do split `25d314761ce3`. Proporções: desvio máx. 0,06 pp. Pré-processamento explicado (tabela por modelo) e demonstrado com as camadas reais (cast float32 como no `keras.Input`). Revisão: motivo do subconjunto quantificado, erro-padrão no pior caso, alerta de ~5 pp para métricas por classe. Aprovada. |
| 2026-11-09 | A4 | Funções: `make_augmentation` (flip H, flip V e rotação ±90° reflect, sementes distintas), `train_model` (epochs/patience obrigatórios, ES opcional), `plot_history` (pesos usados por etapa, épocas descartadas), `evaluate_model` (val + teste, F1 por classe e matrizes nos dois, inferência = mediana de 3 após aquecimento, aceita lista de etapas), `plot_confusion_matrix`, `top_confusions`. Decididos: baseline MLP sem ES; avaliação val + teste; augmentation flips + rotação. Revisão: bug do augmentation (camada única H+V gerava 2 orientações; sementes iguais correlacionavam flip e rotação) confirmado empiricamente e corrigido; perda/otimizador justificados. Testadas com modelo descartável. Aprovada. |
| 2026-11-10 | A5 | MLP 256→128 ReLU + softmax (3.180.170 parâmetros), 40 épocas sem ES (~1,5 min). F1-macro 0,482 (val) · 0,511 (teste). Previsto overfitting; observado **underfitting predominante** (treino ~56%), overfitting moderado após ~30 épocas (vão médio 4,3 → 8,8 pp), validação instável. Erros seguem a cor média (cinzas urbanos; SeaLake/Forest → Pasture; Highway como destino); hipótese do A2 parcial. Desbalanceamento: Pasture prevista 137× para 74 (val) → sem class_weight. Revisão: diagnóstico calibrado com médias por janela, decisão de desbalanceamento só com validação, pares da hipótese em tabela textual. Duas execuções completas com métricas idênticas. Aprovada em 2026-11-11. |
| 2026-11-11 | A6 | Variantes isoladas com `construir_mlp` (mesmos pesos iniciais): ES, ES + dropout 0,3, ES + L2 1e-4, ES + augmentation. Dropout e L2 separados após diagnóstico (combinados colapsavam: F1 val 0,184). F1-macro val: baseline 0,482 · ES 0,479 · dropout 0,339 · L2 0,503 · augmentation 0,507. Só o dropout teve efeito claro (negativo); ES, L2 e augmentation dentro do ruído; no teste nenhum ganho se repete (baseline 0,511). `MELHOR_MLP` = MLP + ES + augmentation (escolha só entre variantes com ES). Limitações da MLP em tabela. Revisão: interpretação calibrada ao ruído, contradição A4 corrigida, seleção restrita. Três execuções completas com métricas idênticas. Aprovada. |
| 2026-11-12 | B1 | CNN 3 blocos (32→64→128) + GAP + Dense(128) + softmax (111.050 parâmetros, ~29× menos que a MLP). Variantes CNN + ES (F1 val 0,668, início de overfitting após a época 12) e CNN + ES + augmentation (F1 val 0,767 · teste 0,758, escolhida). Comparação 2×2 arquitetura × augmentation: arquitetura +19/+26 pts; augmentation +3 (MLP) e +10 (CNN). Confusões de cor caem para ≤ ~0,08; restam Highway → River (0,319; recall de Highway 0,286) e PermanentCrop → HerbaceousVegetation (0,258). Custo ~6 s/época (MLP ~2,5). Revisão: overfitting calibrado ("início"), efeito do augmentation explicado pelo regime, leitura completa dos pares, top_confusions e recall em texto. Aprovada. |
| 2026-11-12 | B2 | MobileNetV2 (ImageNet, 96×96) congelada + GAP + Dense(10, softmax): 2.270.794 parâmetros, 12.810 treináveis. Decididos pelos alunos: cabeça só com a camada final; variantes TL-FE + ES e TL-FE + ES + aug. Congelamento provado (0 treináveis na base, pesos e estatísticas da BN idênticos antes/depois; cabeça inicial igual nas variantes). F1-macro val: TL-FE + ES 0,916 (escolhida, teste 0,902) · + aug 0,900 (empate no ruído; augmentation sem efeito numa cabeça linear sobre features fixas, ao contrário dos +10 na CNN). +15 pts sobre a CNN, +41 sobre a MLP. Highway → River 0,319 → 0,103; PermanentCrop → HerbaceousVegetation 0,258 → 0,134. Leve overfitting da cabeça (treino 0,986). Custo: treino ~200–225 s (~13,5–15 s/época), inferência ~2,2–2,4 ms/imagem (~6–8× a CNN). Revisão: texto do training=False corrigido (no Keras 3, trainable=False já põe a BN em inferência), PESOS_TL_FE guardados para a B3, precision/recall na tabela, ressalva do custo sem cache de features. Duas execuções completas com métricas idênticas. Aprovada. |
| 2026-11-12 | B3 | Fine-tuning das duas variantes da B2 (decisão dos alunos), cada uma a partir dos seus pesos da etapa 1 (conferido por `predict`). **Achado:** no Keras 3.15 o `fit` de um modelo funcional sobrescreve o `base(x, training=False)`; BatchNorm descongeladas mudavam as estatísticas. Correção: BN congeladas também na região descongelada, demonstração com modelo de brinquedo no início da B3, regra e textos da B2 corrigidos. Descongeladas 10 convoluções a partir de `block_14_expand` (1.510.720 parâmetros, ~67% da base; 1.523.530 treináveis). lr 1e-5. F1-macro val: FE 0,916 · FT 0,916 · FT + aug 0,912 → **empate**; `MELHOR_TL` = TL-FE + ES. FT sem aug só aprofunda o overfitting (val_loss sobe desde a 1ª época); com aug +1,2 pt (ruído, direção da hipótese da B2). Custo do FT ~40% maior (284–303 s). Erros inalterados. Revisão: comparação de erros pela mesma variante, trava contra fine-tuning duplo, descrição exata do descongelamento, `tabelas_comparacao` no A4, legenda da `plot_history`. Execução completa: métricas da A5 à B2 idênticas. Aprovada. |
| 2026-11-12 | B4 | Decididos pelos alunos: tabela com os 3 escolhidos + anexo das 11 variantes; recomendação TL-FE. Seção "por que é justa" com todas as diferenças assumidas (orçamento/paciência do TL, lr do FT, 96×96, pré-treino, MLP/CNN sem convergir em 40 épocas, desempate). Tabela final (formato BR), gráfico desempenho × custo de treino e de inferência, heatmap de F1 por classe, anexo, 3 CSVs (resultados, F1 por classe em formato longo, metadados da execução), discussão como última célula. F1 teste: MLP 0,498 · CNN 0,758 · TL 0,902; TL e CNN com o mesmo tempo de treino (~200 s), inferência TL ~8× a CNN. TL ≥ CNN ≥ MLP nas 10 classes; mesmas 5 classes difíceis nos três. Estimativa de tempo do A3 conferida (~10 min de TL). Revisão: diferenças de protocolo completas, colunas de convergência e s/época, legenda, variáveis fora de células de exibição, metadados. Enxugar a repetição de custo na B2/B3: oferecido, não pedido (não feito). Aprovada. |
| 2026-11-12 | X | Execução oficial local (17:41, AMD Ryzen 7 7435HS, TF 2.21 / Keras 3.15): 53 células, 0 erros, métricas idênticas às execuções anteriores, assinatura do split `25d314761ce3`, escolhidos MLP + ES + aug / CNN + ES + aug / TL-FE + ES. Conferência das 83 células markdown por agente: métricas todas batem; 8 correções (River → Highway não caiu na B2; tempos do FT 280/310 s; arredondamentos da B4; faixas de tempo da MLP/CNN). Markdown sincronizado no executado sem reexecutar (código idêntico conferido). Validação no Colab movida para a fase E. Aprovada. |
