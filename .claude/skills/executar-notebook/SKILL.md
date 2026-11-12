---
name: executar-notebook
description: Executa trabalho_eurosat.ipynb de ponta a ponta com nbconvert no ambiente uv do projeto, em modo smoke (rápido, poucos dados) ou completo, e resume erros, tempos por célula e métricas. Use para validar uma fase, antes de revisões e antes de atualizar o relatório.
argument-hint: "[smoke|completo]"
---

# /executar-notebook $ARGUMENTS

Modo: **$ARGUMENTS** (padrão: `smoke`).

| Modo | O que faz | Duração (local) | Como rodar |
|---|---|---|---|
| `smoke` | `SMOKE_TEST=1`: mesmo código, subconjunto mínimo e 1–2 épocas. Valida que tudo executa. | ~2–3 min | primeiro plano |
| `completo` | Execução real que gera os números do trabalho | ~20 min | **background** (`run_in_background`); só com o ok do aluno |

## Comandos (Bash, a partir da raiz do projeto)

Smoke:
```bash
SMOKE_TEST=1 uv run jupyter nbconvert --to notebook --execute trabalho_eurosat.ipynb \
  --ExecutePreprocessor.timeout=-1 --output-dir outputs --output trabalho_eurosat_smoke.ipynb
uv run python .claude/skills/executar-notebook/resumo_execucao.py outputs/trabalho_eurosat_smoke.ipynb
```

Completo:
```bash
uv run jupyter nbconvert --to notebook --execute trabalho_eurosat.ipynb \
  --ExecutePreprocessor.timeout=-1 --output-dir outputs --output trabalho_eurosat_executado.ipynb
uv run python .claude/skills/executar-notebook/resumo_execucao.py outputs/trabalho_eurosat_executado.ipynb
```

Notas:
- O notebook roda com o diretório de trabalho na pasta do `.ipynb`, então `data/` é encontrada.
- Se o nbconvert falhar numa célula, ele ainda salva o notebook parcial quando há `--allow-errors`. Use essa flag só para diagnóstico, nunca para "passar".
- Nunca edite o notebook original para contornar um erro de ambiente. Diagnostique primeiro.

## Depois de executar
1. Mostre o resumo do script: status, erros (célula + exceção), as 5 células mais lentas e as linhas de tempo/métricas.
2. Em caso de erro: identifique a causa (código da fase × ambiente × dados) e proponha a correção. Se a correção for no notebook, aplique e rode o smoke de novo.
3. No modo `completo`: aponte os markdowns com `✍️` cujos números precisam ser conferidos com as saídas, e diga se `outputs/resultados_eurosat.csv` foi gerado.
