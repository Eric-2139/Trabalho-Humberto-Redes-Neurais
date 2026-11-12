---
name: nova-fase
description: Constrói UMA fase do PLAN.md no notebook do trabalho (ex. A1, A2, B3) seguindo o ciclo escopo → células → smoke test → revisão pelos agentes → explicação → parada para aprovação. Use quando o aluno pedir para começar ou continuar uma fase do notebook.
argument-hint: "<id da fase, ex.: A1>"
---

# /nova-fase $ARGUMENTS

Fase solicitada: **$ARGUMENTS**. Se vier vazio, use a primeira fase com status ⬜ no PLAN.md e confirme com o aluno antes de começar.

## 1. Preparar
1. Leia a linha da fase na tabela da seção 6 do `PLAN.md` (o que entra + critério de pronto) e os itens correspondentes em `docs/enunciado.md`.
2. Verifique se a fase anterior está ✅. Se não estiver, **pare** e pergunte.
3. Se o escopo tiver alguma decisão em aberto (ex.: tamanho de camada, técnica de regularização), apresente a recomendação com 1 frase de porquê e espere o ok **antes** de escrever.
4. Marque a fase como 🔄 no PLAN.md.

## 2. Escrever as células
- Notebook: `trabalho_eurosat.ipynb`. Se não existir (fase A1), crie com a célula de cabeçalho descrita em `.claude/rules/notebook-estilo.md`.
- Use **NotebookEdit**, inserindo as células na posição da seção (após a última célula da fase anterior).
- Siga `.claude/rules/protocolo-ml.md` e `.claude/rules/notebook-estilo.md`: markdown "o que + por quê" → código → (saída) → interpretação.
- Interpretações que dependem de números levam `✍️` até a conferência.
- O hook valida cada edição. Se ele acusar erro, corrija antes de seguir.

## 3. Validar
1. Rode `/executar-notebook smoke` (o notebook inteiro com poucos dados). Corrija os erros até passar.
2. Se a fase produz métricas ou curvas relevantes e o aluno quiser ver os números reais, **ofereça** a execução completa. Não rode sem o ok.

## 4. Revisar (agentes, em paralelo)
- `auditor-ml`: "Revise a fase $ARGUMENTS de trabalho_eurosat.ipynb (células X–Y). Execução smoke em outputs/trabalho_eurosat_smoke.ipynb."
- `revisor-rubrica`: "Revise a fase $ARGUMENTS contra o enunciado e a rubrica."
- Aplique as correções `BLOQUEANTE` e `IMPORTANTE` que forem claras. As que envolvem decisão vão para o aluno.

## 5. Entregar e parar
Responda ao aluno, em português:
1. **O que foi adicionado:** lista das células (título de cada uma), em 1 linha cada.
2. **Conceitos novos** da fase explicados por analogia ao workflow tabular dele (sklearn), no máximo 3 bullets.
3. **Resultado do smoke test** e da revisão: achados corrigidos e pendências que dependem dele.
4. **Perguntas/decisões** para ele, se houver.

Depois marque a fase como 👀 no PLAN.md e **pare**. Só ao receber aprovação explícita: marque ✅, atualize "Status atual" e adicione uma entrada no log (data absoluta).
