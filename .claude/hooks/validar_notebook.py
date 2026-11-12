"""Hook PostToolUse: valida notebooks .ipynb após cada edição feita pelo Claude.

Checagens:
  1. O arquivo é um notebook válido (JSON + schema nbformat v4).
  2. Toda célula de código compila como Python (ignora linhas de magia: %, %%, !).

Recebe o JSON do hook no stdin. Sai com 0 se estiver tudo ok ou se o arquivo não for .ipynb.
Sai com 2 em caso de problema: o stderr volta para o Claude, que deve corrigir antes de seguir.
"""
import ast
import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = payload.get("tool_input", {}) or {}
    path = tool_input.get("notebook_path") or tool_input.get("file_path") or ""
    if not path.lower().endswith(".ipynb"):
        return 0

    import warnings
    import nbformat  # importado só quando necessário (o hook roda em toda edição)

    warnings.filterwarnings("ignore", module="nbformat")  # avisos de versão não são erro do notebook

    try:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
    except Exception as e:  # JSON quebrado, schema inválido, arquivo ausente
        print(f"[validar_notebook] {path} NÃO é um notebook válido: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    problemas = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        src = "\n".join(
            "" if line.lstrip().startswith(("%", "!")) else line
            for line in cell.source.splitlines()
        )
        try:
            ast.parse(src)
        except SyntaxError as e:
            linha = (e.text or "").strip()
            problemas.append(f"célula {idx} (linha {e.lineno}): {e.msg} -> {linha!r}")

    if problemas:
        print(f"[validar_notebook] Erros de sintaxe em {path}:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
