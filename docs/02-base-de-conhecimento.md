# 2. Base de conhecimento

Arquivo: `data/base_conhecimento.json` (14 trechos).

| Campo | Uso |
|-------|-----|
| `id` | identificador estável (usado na avaliação) |
| `categoria` | extintores, deteccao, hidrantes, sprinklers, rotas, documentacao, seguranca, limites |
| `titulo`, `texto` | conteúdo recuperado e enviado ao LLM |
| `palavras_chave` | sinônimos e termos do dia a dia que melhoram a busca |
| `fonte` | norma ou referência exibida ao usuário |

## Decisões
- Trechos curtos e autocontidos: cada um responde uma dúvida específica, o que facilita a recuperação e a citação.
- Onde a norma ou o fabricante definem a frequência, o texto diz isso em vez de citar um número.
- Fontes citadas por nome/número da norma, sem reproduzir texto das normas.

## Limitações e cuidados
- **Conteúdo educativo e resumido.** Antes de usar em um cenário real, valide cada trecho com as normas ABNT vigentes e com o responsável técnico.
- Prazos de AVCB/CLCB e exigências variam por estado; a base apenas orienta a consultar o Corpo de Bombeiros local.
- Para ampliar: adicionar novos objetos no JSON (ex.: gás GLP, pressurização de escadas, brigada de incêndio).
