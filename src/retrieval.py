"""Busca simples (BM25) na base de conhecimento. Sem dependências externas."""
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "um", "uma", "uns", "umas", "e", "ou", "que", "para", "por", "com", "sem", "se", "ao",
    "eu", "me", "meu", "minha", "qual", "quais", "como", "quando", "onde", "posso", "devo",
    "preciso", "fazer", "faco", "isso", "esse", "essa", "esta", "este", "eh", "ser", "ter",
    "vez", "hoje", "aqui", "agora", "tem", "sao", "mais", "muito", "pode", "passa", "quanto",
}


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def tokenizar(texto: str) -> list[str]:
    palavras = re.findall(r"[a-z0-9]+", normalizar(texto))
    saida = []
    for p in palavras:
        if p in STOPWORDS or len(p) < 2:
            continue
        if len(p) > 3 and p.endswith("s"):  # stemming bem simples (plural)
            p = p[:-1]
        saida.append(p)
    return saida


def carregar_base(caminho: Path | None = None) -> list[dict]:
    caminho = caminho or DATA_DIR / "base_conhecimento.json"
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


class Retriever:
    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.docs = [
            tokenizar(c["titulo"] + " " + c["texto"] + " " + " ".join(c.get("palavras_chave", [])))
            for c in chunks
        ]
        self.n = len(self.docs)
        self.avg = sum(len(d) for d in self.docs) / self.n
        df = Counter()
        for d in self.docs:
            df.update(set(d))
        self.idf = {t: math.log(1 + (self.n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def buscar(self, consulta: str, k: int = 3) -> list[tuple[float, dict]]:
        termos = tokenizar(consulta)
        resultados = []
        for chunk, doc in zip(self.chunks, self.docs):
            tf = Counter(doc)
            score = 0.0
            for t in termos:
                if t not in tf:
                    continue
                num = tf[t] * (self.k1 + 1)
                den = tf[t] + self.k1 * (1 - self.b + self.b * len(doc) / self.avg)
                score += self.idf.get(t, 0) * num / den
            resultados.append((score, chunk))
        resultados.sort(key=lambda x: x[0], reverse=True)
        return resultados[:k]
