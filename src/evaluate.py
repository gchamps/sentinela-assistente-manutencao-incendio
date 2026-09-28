"""Avaliação do Sentinela. Execute: python src/evaluate.py

Métricas (funcionam offline, sem chave de API):
  - Acerto de recuperação: a fonte esperada aparece nos trechos recuperados.
  - Recusa correta: perguntas fora do escopo são recusadas (sem inventar).
  - Emergência: o assistente aciona o protocolo com o 193.
Se ANTHROPIC_API_KEY estiver definida, mede também:
  - Cobertura de palavras-chave esperadas na resposta gerada.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent import Agente  # noqa: E402
from retrieval import normalizar  # noqa: E402

CASOS = Path(__file__).resolve().parent.parent / "data" / "casos_teste.json"


def main():
    agente = Agente()
    casos = json.loads(CASOS.read_text(encoding="utf-8"))
    linhas, ok_rec, n_rec, ok_rec_neg, n_neg, ok_emerg, n_emerg, ok_kw, n_kw = [], 0, 0, 0, 0, 0, 0, 0, 0

    for c in casos:
        r = agente.responder(c["pergunta"])
        status = "PASS"
        if c.get("emergencia"):
            n_emerg += 1
            if r["modo"] == "emergencia" and "193" in r["resposta"]:
                ok_emerg += 1
            else:
                status = "FAIL"
        elif c["deve_recusar"]:
            n_neg += 1
            if r["modo"] == "sem_info":
                ok_rec_neg += 1
            else:
                status = "FAIL"
        else:
            n_rec += 1
            if any(i in r["ids"] for i in c["esperado_ids"]):
                ok_rec += 1
            else:
                status = "FAIL"
            if r["modo"] == "llm":
                n_kw += 1
                resp = normalizar(r["resposta"])
                if all(normalizar(k) in resp for k in c["palavras_esperadas"]):
                    ok_kw += 1
        linhas.append((c["id"], c["pergunta"][:55], r["modo"], ",".join(r["ids"]) or "-", status))

    print(f"{'ID':<5}{'Pergunta':<57}{'Modo':<11}{'Fontes recuperadas':<40}Resultado")
    for l in linhas:
        print(f"{l[0]:<5}{l[1]:<57}{l[2]:<11}{l[3]:<40}{l[4]}")
    print()
    print(f"Acerto de recuperação (dentro do escopo): {ok_rec}/{n_rec} = {ok_rec/n_rec:.0%}")
    print(f"Recusa correta (fora do escopo):          {ok_rec_neg}/{n_neg} = {ok_rec_neg/n_neg:.0%}")
    print(f"Protocolo de emergência:                  {ok_emerg}/{n_emerg}")
    if n_kw:
        print(f"Cobertura de palavras-chave (LLM):        {ok_kw}/{n_kw} = {ok_kw/n_kw:.0%}")
    else:
        print("Cobertura de palavras-chave (LLM):        não medida (defina ANTHROPIC_API_KEY)")


if __name__ == "__main__":
    main()
