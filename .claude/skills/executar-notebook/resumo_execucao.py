"""Resume um notebook executado: erros, células mais lentas e linhas de tempo/métricas.

Uso: uv run python .claude/skills/executar-notebook/resumo_execucao.py <notebook_executado.ipynb>
"""
import sys
from datetime import datetime

import nbformat

MARCADORES = ("⏱", "===", "MLP escolhida", "Razão de desbalanceamento", "Parâmetros treináveis", "treino=")


def duracao(cell):
    ex = cell.get("metadata", {}).get("execution", {})
    ini, fim = ex.get("iopub.execute_input"), ex.get("shell.execute_reply")
    if not (ini and fim):
        return None
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (f(fim) - f(ini)).total_seconds()


def primeira_linha(cell):
    for linha in cell.source.splitlines():
        if linha.strip():
            return linha.strip()[:70]
    return "(vazia)"


def main(path):
    nb = nbformat.read(path, as_version=4)
    code = [(i, c) for i, c in enumerate(nb.cells) if c.cell_type == "code"]
    erros, tempos, destaques = [], [], []
    for i, c in code:
        d = duracao(c)
        if d is not None:
            tempos.append((d, i, primeira_linha(c)))
        for out in c.get("outputs", []):
            if out.get("output_type") == "error":
                tb = [l for l in out.get("traceback", []) if l.strip()][-3:]
                erros.append((i, out.get("ename"), out.get("evalue"), tb))
            elif out.get("output_type") == "stream":
                for linha in out.get("text", "").splitlines():
                    if any(m in linha for m in MARCADORES):
                        destaques.append((i, linha.strip()))

    executadas = sum(1 for _, c in code if c.get("execution_count"))
    print(f"Notebook: {path}")
    print(f"Células de código: {len(code)} | executadas: {executadas} | erros: {len(erros)}")
    print(f"Tempo total das células: {sum(t for t, _, _ in tempos):.0f}s")

    if erros:
        print("\n## ERROS")
        for i, en, ev, tb in erros:
            print(f"- célula {i}: {en}: {ev}")
    if tempos:
        print("\n## 5 células mais lentas")
        for d, i, src in sorted(tempos, reverse=True)[:5]:
            print(f"- célula {i}: {d:.1f}s | {src}")
    if destaques:
        print("\n## Tempos e métricas reportados")
        for i, linha in destaques:
            print(f"- [{i}] {linha}")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1])
