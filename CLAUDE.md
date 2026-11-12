# CLAUDE.md — Trabalho de Redes Neurais (EuroSAT)

Trabalho acadêmico de Redes Neurais: classificação de imagens de satélite (EuroSAT RGB, 10 classes) comparando
MLP × CNN própria × Transfer Learning (MobileNetV2), tudo em **CPU**. O aluno vem de ML tabular (sklearn: SVM,
Random Forest, AdaBoost, pipelines, CV) e está aprendendo o fluxo de deep learning para imagens.

- Requisitos e rubrica: @docs/enunciado.md
- Plano, decisões, status e log: @PLAN.md

## Como colaborar (obrigatório)

1. **Fase por fase.** Trabalhe apenas na fase combinada do PLAN.md. Ao terminar, explique o que foi feito e **pare** até o aluno aprovar.
   Nunca adiante fases nem rode execuções longas sem pedido.
2. **Pergunta não é ordem.** Se o aluno fizer uma pergunta, responda e espere.
3. **Português do Brasil** em tudo: conversa, markdown do notebook, comentários de código e nomes de variáveis descritivos (exceto termos técnicos consagrados).
4. **Ensine por analogia** ao workflow tabular dele (ex.: `Rescaling` dentro do modelo ≈ `Pipeline` do sklearn; curva de treino ≈ learning curve).
5. **Decisões de protocolo** (split, métricas, épocas, arquitetura) só mudam com acordo do aluno e precisam ser registradas no PLAN.md (seção 3 + log).

## Gestão de memória

| Onde | O que guardar |
|---|---|
| `CLAUDE.md` (este arquivo) | Regras estáveis de colaboração, stack e comandos. Muda raramente. |
| `PLAN.md` | Estado do trabalho: decisões, pontos em aberto, status das fases e log. **Atualizar ao fim de cada fase.** |
| `.claude/rules/` | Regras técnicas detalhadas (protocolo de ML, estilo do notebook, relatório). |
| `docs/enunciado.md` | Cópia literal do enunciado. Não editar. |
| Auto-memória do Claude Code | Preferências pessoais do aluno que valem entre sessões. |

Ao concluir uma fase: marcar o status na tabela da seção 6 do PLAN.md, atualizar a linha "Status atual" e adicionar uma entrada ao log (data absoluta).

## Stack e comandos

- Python 3.12 gerenciado pelo **uv** (`pyproject.toml`, `uv.lock`, `.venv/`). Keras 3 com backend TensorFlow.
- Instalar/sincronizar: `uv sync` · adicionar pacote: `uv add <pacote>` (dev: `uv add --dev <pacote>`)
- Python do projeto: `uv run python ...`
- Executar o notebook: use a skill **/executar-notebook** (`smoke` ≈ 2–3 min; `completo` ≈ 20 min local, rodar em background).
- O dataset fica em `data/eurosat_rgb.zip` e é lido direto do zip, sem extrair (não versionar, não editar). Saídas executadas e CSV de resultados vão para `outputs/`.

## Arquivos

| Caminho | Papel |
|---|---|
| `trabalho_eurosat.ipynb` | Notebook principal (Parte A: dados + MLP · Parte B: CNN + TL + comparação) |
| `relatorio.ipynb` | Relatório detalhado: markdown + código que carrega as tabelas de `outputs/*.csv` |
| `outputs/` | Notebooks executados, `resultados_eurosat.csv` |
| `docs/enunciado.md` | Enunciado do professor |

## Harness deste projeto

- **Skills**
  - `/nova-fase <id>`: constrói uma fase do PLAN.md seguindo o ciclo completo e para para aprovação.
  - `/executar-notebook [smoke|completo]`: roda o notebook com nbconvert e resume erros, tempos e métricas.
  - `/atualizar-relatorio`: sincroniza `relatorio.ipynb` com os CSVs de `outputs/`.
- **Agents** (revisão somente leitura, usados no fim de cada fase)
  - `auditor-ml`: corretude técnica (vazamento, protocolo, armadilhas do Keras, métricas).
  - `revisor-rubrica`: aderência ao enunciado e à rubrica, e clareza para o professor.
- **Rules**: `.claude/rules/protocolo-ml.md` (sempre), `notebook-estilo.md` (ao mexer em `.ipynb`), `relatorio.md` (ao mexer no relatório).
- **Hook**: após qualquer edição de `.ipynb`, `.claude/hooks/validar_notebook.py` valida o formato nbformat e a sintaxe Python de cada célula de código. Se acusar erro, corrija antes de seguir.

## Edição de notebooks

- Edite **uma célula por vez** (o aluno acompanha). Não gere o notebook inteiro por script.
- O `trabalho_eurosat.ipynb` passou do limite da ferramenta Read (~33 mil tokens), então o NotebookEdit falha por exigir leitura prévia. Use o script do projeto, que faz o mesmo que o NotebookEdit e roda o validador do hook:
  - `uv run python .claude/scripts/editar_celula.py trabalho_eurosat.ipynb replace <cell_id> <arquivo_fonte>`
  - `uv run python .claude/scripts/editar_celula.py trabalho_eurosat.ipynb insert <depois_do_id> <code|markdown> <arquivo_fonte>`

  O conteúdo da célula vai num arquivo temporário (heredoc para o scratchpad). Para ler células, use `nbformat` (ex.: imprimir `cell.source` pelo id).
- Ids das últimas células, para inserir depois: fim da A6 = `9ebf0204`; fim da B1 = `d71bef19` (célula "Por que a CNN superou a MLP" + resumo); fim da B2 = `55d8edcb` ("Resumo da B2"); fim da B3 = `beff00a6` ("Resumo da B3"); fim da B4 = `d99aba53` ("Discussão", última célula do notebook).
- Toda célula de código é precedida por um markdown "o que + por quê". Interpretações vêm depois das saídas que as sustentam.
- Números citados em markdown que dependem da execução levam o marcador `✍️` até serem conferidos com as saídas reais.
