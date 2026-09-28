# 🧯 Sentinela — Assistente de Manutenção Preventiva Contra Incêndio

Assistente virtual com IA generativa que apoia técnicos, síndicos e gestores na manutenção preventiva de sistemas de combate a incêndio (extintores, detecção e alarme, hidrantes, sprinklers e iluminação de emergência).

Projeto do Lab **"Construa Seu Assistente Virtual Com Inteligência Artificial"** (DIO).

> ⚠️ Conteúdo educativo. Não substitui o responsável técnico, as normas ABNT vigentes nem a vistoria do Corpo de Bombeiros.

## O que ele faz
- Responde dúvidas com base em uma **base de conhecimento** própria e cita a fonte.
- **Não inventa:** se não há informação, diz que não sabe e indica quem consultar.
- Aciona um **protocolo de emergência** (193) sem passar pela IA.
- Nunca orienta desativar ou burlar sistemas de proteção.
- Mantém o **contexto** da conversa e um perfil (tipo de edificação e UF).
- Inclui uma **simulação** da próxima manutenção de extintores.

## Os 6 passos do desafio
| Passo | Onde está |
|-------|-----------|
| 1. Documentação | [docs/01-documentacao-agente.md](docs/01-documentacao-agente.md) |
| 2. Base de conhecimento | [data/base_conhecimento.json](data/base_conhecimento.json) · [docs/02-base-de-conhecimento.md](docs/02-base-de-conhecimento.md) |
| 3. Prompts | [src/prompts.py](src/prompts.py) · [docs/03-prompts.md](docs/03-prompts.md) |
| 4. Aplicação funcional | [src/app.py](src/app.py) · [docs/04-aplicacao.md](docs/04-aplicacao.md) |
| 5. Avaliação e métricas | [src/evaluate.py](src/evaluate.py) · [docs/05-avaliacao-metricas.md](docs/05-avaliacao-metricas.md) |
| 6. Pitch | [docs/06-pitch.md](docs/06-pitch.md) |

## Estrutura
```
sentinela-assistente-manutencao-incendio/
  README.md
  requirements.txt
  data/    base_conhecimento.json · casos_teste.json
  docs/    documentação dos 6 passos
  src/     app.py · agent.py · retrieval.py · prompts.py · calculadora.py · evaluate.py
```

## Como rodar
```bash
git clone https://github.com/gchamps/sentinela-assistente-manutencao-incendio
cd sentinela-assistente-manutencao-incendio
pip install -r requirements.txt

# Opcional: ativa a IA generativa (sem a chave, roda em modo offline)
export ANTHROPIC_API_KEY="sua-chave"

streamlit run src/app.py
```

Avaliação: `python src/evaluate.py`

## Como funciona
Pergunta → detector de emergência → busca BM25 na base → se a relevância for baixa, recusa → senão monta o prompt (regras + trechos + perfil + histórico) e chama o LLM.

## Tecnologias
Python · Streamlit · API de LLM (Anthropic) · BM25 implementado em Python puro

## Limitações
- Base pequena (14 trechos), com conteúdo resumido que deve ser validado por um responsável técnico.
- Avaliação inicial com 14 casos escritos pelo autor; veja a análise em [docs/05-avaliacao-metricas.md](docs/05-avaliacao-metricas.md).
- Busca por palavras-chave (sem embeddings).

## Autor
Gabriel Champin — [LinkedIn](https://linkedin.com/in/gabrielchampin) · [GitHub](https://github.com/gchamps)
