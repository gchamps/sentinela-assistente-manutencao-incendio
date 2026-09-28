"""Agente Sentinela: recuperação + guardrails + LLM (opcional)."""
import os

from prompts import (MENSAGEM_EMERGENCIA, MENSAGEM_SEM_INFORMACAO, SYSTEM_PROMPT,
                     TEMPLATE_CONTEXTO)
from retrieval import Retriever, carregar_base, normalizar

MODELO = os.getenv("SENTINELA_MODEL", "claude-sonnet-5")
SCORE_MINIMO = float(os.getenv("SENTINELA_SCORE_MIN", "2.5"))
MAX_HISTORICO = 6

GATILHOS_EMERGENCIA = [
    "pegando fogo", "incendio em andamento", "fogo agora", "estou vendo fogo",
    "esta queimando", "fumaca agora", "principio de incendio agora",
]


def e_emergencia(pergunta: str) -> bool:
    p = normalizar(pergunta)
    return any(g in p for g in GATILHOS_EMERGENCIA)


class Agente:
    def __init__(self, chunks: list[dict] | None = None):
        self.retriever = Retriever(chunks or carregar_base())
        self.usa_llm = bool(os.getenv("ANTHROPIC_API_KEY"))

    def _formatar_contexto(self, trechos: list[dict]) -> str:
        return "\n\n".join(
            f"[{c['id']}] {c['titulo']}\n{c['texto']}\nFonte: {c['fonte']}" for c in trechos
        )

    def _chamar_llm(self, pergunta: str, contexto: str, perfil: str, historico: list[dict]) -> str:
        import anthropic

        cliente = anthropic.Anthropic()
        mensagens = [{"role": m["role"], "content": m["content"]} for m in historico[-MAX_HISTORICO:]]
        mensagens.append({
            "role": "user",
            "content": TEMPLATE_CONTEXTO.format(contexto=contexto, perfil=perfil or "não informado",
                                                pergunta=pergunta),
        })
        r = cliente.messages.create(model=MODELO, max_tokens=600, temperature=0.2,
                                    system=SYSTEM_PROMPT, messages=mensagens)
        return r.content[0].text

    def responder(self, pergunta: str, historico: list[dict] | None = None,
                  perfil: str = "") -> dict:
        historico = historico or []

        if e_emergencia(pergunta):
            return {"resposta": MENSAGEM_EMERGENCIA, "fontes": [], "modo": "emergencia", "ids": []}

        achados = self.retriever.buscar(pergunta, k=3)
        relevantes = [(s, c) for s, c in achados if s >= SCORE_MINIMO]
        if not relevantes:
            return {"resposta": MENSAGEM_SEM_INFORMACAO, "fontes": [], "modo": "sem_info", "ids": []}

        trechos = [c for _, c in relevantes]
        contexto = self._formatar_contexto(trechos)
        fontes = sorted({c["fonte"] for c in trechos})
        ids = [c["id"] for c in trechos]

        if self.usa_llm:
            texto = self._chamar_llm(pergunta, contexto, perfil, historico)
            modo = "llm"
        else:  # modo offline: devolve o trecho mais relevante, sem gerar texto novo
            melhor = trechos[0]
            texto = f"**{melhor['titulo']}**\n\n{melhor['texto']}"
            modo = "offline"
        return {"resposta": texto, "fontes": fontes, "modo": modo, "ids": ids}
