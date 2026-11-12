"""Edita UMA célula do notebook (equivalente ao NotebookEdit) e valida com o hook do projeto.

Uso:
  editar_celula.py <notebook> replace <cell_id> <arquivo_fonte>
  editar_celula.py <notebook> insert  <depois_do_id> <code|markdown> <arquivo_fonte>
"""
import json, subprocess, sys
import nbformat

caminho, operacao = sys.argv[1], sys.argv[2]
nb = nbformat.read(caminho, as_version=4)
ids = [c.get("id") for c in nb.cells]
if operacao == "replace":
    alvo, fonte = sys.argv[3], open(sys.argv[4], encoding="utf-8").read()
    nb.cells[ids.index(alvo)].source = fonte
    novo_id = alvo
elif operacao == "insert":
    depois, tipo, fonte = sys.argv[3], sys.argv[4], open(sys.argv[5], encoding="utf-8").read()
    celula = nbformat.v4.new_code_cell(fonte) if tipo == "code" else nbformat.v4.new_markdown_cell(fonte)
    nb.cells.insert(ids.index(depois) + 1, celula)
    novo_id = celula.id
else:
    sys.exit(f"operação desconhecida: {operacao}")
nbformat.write(nb, caminho)
hook = subprocess.run([sys.executable, ".claude/hooks/validar_notebook.py"],
                      input=json.dumps({"tool_input": {"notebook_path": caminho}}),
                      capture_output=True, text=True, encoding="utf-8")
print(f"{operacao} ok · id={novo_id} · validador: {'ok' if hook.returncode == 0 else 'ERRO ' + hook.stderr}")
