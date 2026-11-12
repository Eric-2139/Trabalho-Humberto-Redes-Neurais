# Protocolo de ML — regras técnicas invioláveis

Estas regras garantem a **comparação justa** (10% da nota) e a corretude das métricas (15%).

## Dados e split
- O split é feito **uma única vez** (seção A3), estratificado por classe, com `random_state=SEED`. Nenhuma outra célula reamostra os dados.
- Duplicatas exatas (MD5) são removidas **antes** do split, e um `assert` garante que nenhum hash aparece em dois conjuntos.
- Todos os modelos recebem os mesmos `X_train/X_val/X_test` em `uint8` 64×64×3. Nenhum modelo recebe dados pré-processados por fora.
- **EDA × vazamento:** análise feita antes do split (A2) é só descritiva. Estatística que vá **ajustar** algo (normalização, `class_weight`, reamostragem, escolha de features) vem **só do treino**. Ao escrever cada etapa, deixe explícito se ela é descritiva ou se ajusta/decide algo.
- **MLP para a B4:** `MELHOR_MLP` = maior `val_f1_macro` **entre as variantes com early stopping** do A6 (o baseline é só o "antes").
- **O teste é só para reportar.** Escolha de regularização, épocas, qual MLP vai para a comparação etc. usa **apenas a validação** (`val_f1_macro`).

## Pré-processamento (dentro do modelo)
- MLP/CNN: `layers.Rescaling(1/255)`. MLP: `layers.Flatten()` depois do rescaling.
- MobileNetV2: `layers.Resizing(96, 96)` + `layers.Rescaling(1/127.5, offset=-1)` → escala **[-1, 1]**. Nunca usar `/255` na MobileNetV2.
- Data augmentation só como camadas `Random*` dentro do modelo (ficam ativas apenas no `fit`). Para satélite: flips H+V e rotação. Nada de augmentation em validação ou teste.

## Treino
- Compilar sempre via `train_model`: Adam, `sparse_categorical_crossentropy`, `metrics=["accuracy"]`.
- Camada de saída de **todos** os modelos: `Dense(10, activation="softmax")` (decisão dos alunos). Ocultas da MLP e da CNN: ReLU.
- Early stopping: `monitor="val_loss"`, `restore_best_weights=True` (o Keras 3 restaura ao fim do treino mesmo sem parada antecipada). **Única exceção:** a MLP baseline do A5 (`early_stopping=False`), que é o "antes" do diagnóstico. Todos os demais modelos usam ES.
- Data augmentation: `make_augmentation()` = `RandomFlip("horizontal", seed=SEED)` + `RandomFlip("vertical", seed=SEED+1)` + `RandomRotation(0.25, fill_mode="reflect", seed=SEED+2)`. Nunca usar `"horizontal_and_vertical"` numa camada só (sorteia um valor para os dois eixos) nem a mesma semente em duas camadas `Random*` (sorteiam números iguais).
- `train_model` exige `epochs` e `patience` explícitos: MLP/CNN `MAX_EPOCHS`/`PATIENCE`; TL `TL_EPOCHS`/`TL_PATIENCE` (+ `lr=LR_FINE_TUNE` na etapa 2).
- TL: `evaluate_model(modelo, nome, [treino_etapa1, treino_etapa2])` soma tempo e épocas. Avaliar também a etapa 1 sozinha antes da etapa 2 (o ES da etapa 2 não conhece a val_loss da etapa 1); a escolha FE × FT é por `val_f1_macro`.
- `keras.utils.set_random_seed(SEED)` antes de **construir** cada modelo.
- Orçamento máximo de épocas definido nas constantes do A1 (`MAX_EPOCHS`, `TL_EPOCHS`). Não alterar por modelo sem registrar no PLAN.md.
- Tempo de treino = `time.perf_counter()` em volta do `fit`. TL com fine-tuning reporta **etapa 1 + etapa 2**.

## Transfer Learning (armadilhas)
- Etapa 1: `base.trainable = False` e chamada `base(x, training=False)`. Quem põe a BatchNorm em modo de inferência é o `trainable=False`: **no Keras 3, o `fit` de um modelo funcional sobrescreve o `training=False` passado a um submodelo** (conferido em 2026-11-12, Keras 3.15).
- Etapa 2: `base.trainable = True`, recongelar as camadas antes de `block_14_expand` **e todas as `BatchNormalization` da região descongelada**, **recompilar** (o `train_model` faz isso), lr = `LR_FINE_TUNE` (1e-5). Provar com assert que `moving_mean`/`moving_variance` das BN não mudam no treino. `set_weights` vindo da etapa 1 **antes** de mudar `trainable`, com origem e destino no mesmo estado (no Keras 3 a ordem dos pesos é fixa; no tf.keras 2 dependia do congelamento). Conferir com `predict` que o modelo novo parte das mesmas previsões da etapa 1.
- Reportar parâmetros **totais e treináveis** em cada etapa.

## Avaliação
- Sempre via `evaluate_model`: accuracy, precision/recall/F1 **macro**, `classification_report`, matriz de confusão **normalizada por linha**, F1 por classe, tempo de inferência, parâmetros.
- `evaluate_model` mede **validação e teste**. Decisões usam só as colunas `val_*`; as `test_*` são apenas reportadas. Matriz de confusão e relatório por classe vêm do teste.
- `model.predict` em arrays na ordem original (sem shuffle), para os rótulos não desalinharem.
- O desbalanceamento é leve (razão ≈ 1,5). Só aplicar `class_weight`/reamostragem se o diagnóstico mostrar a classe minoritária prejudicada, e justificar com números.

## CPU
- `os.environ["CUDA_VISIBLE_DEVICES"] = "-1"` antes de importar o TensorFlow. Todos os tempos são de CPU.
- Modo smoke (`SMOKE_TEST=1`) só reduz tamanhos/épocas. O código executado é idêntico ao da execução completa.
