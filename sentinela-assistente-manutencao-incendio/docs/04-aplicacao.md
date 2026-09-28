# 4. Aplicação funcional

Interface em Streamlit (`src/app.py`) com duas abas:
1. **Conversa:** chat com histórico, perfil na barra lateral e fontes citadas.
2. **Próxima manutenção:** simulação com a data da última manutenção de extintores.

## Como rodar
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"   # opcional
streamlit run src/app.py
```
Sem a chave, o app funciona em **modo offline**: recupera e mostra o trecho mais relevante da base (útil para testar a busca e os guardrails).
