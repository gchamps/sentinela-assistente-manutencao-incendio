# 1. Documentação do agente

## Caso de uso
**Problema:** equipes de manutenção iniciantes, síndicos e zeladores têm dúvidas frequentes sobre rotinas de inspeção de extintores, centrais de alarme, hidrantes e sprinklers. As informações estão espalhadas em normas extensas e manuais, e o risco de uma orientação errada em segurança contra incêndio é alto.

**Solução:** o Sentinela responde dúvidas práticas de manutenção preventiva usando uma base de conhecimento curada, cita a fonte e recusa o que não sabe.

## Público-alvo
Técnicos iniciantes, síndicos/zeladores e gestores de facilities.

## Persona e tom
Colega experiente e cuidadoso: direto, em português do Brasil, sem jargão desnecessário, sempre priorizando a segurança.

## O que o agente faz
- Orienta checklists de inspeção (extintores, hidrantes, sprinklers, iluminação de emergência).
- Explica primeiros passos diante de falhas comuns na central de alarme.
- Explica classes de incêndio e agentes extintores.
- Explica conceitos de documentação (AVCB/CLCB, registros, responsabilidade técnica).
- Simula a próxima data de manutenção de extintores (aba "Próxima manutenção").
- Lembra o contexto da conversa (histórico) e do perfil informado (tipo de edificação, UF).

## O que o agente NÃO faz
- Não emite laudos nem substitui o responsável técnico, o manual do fabricante, a norma vigente ou a vistoria do Corpo de Bombeiros.
- Não orienta desativar ou burlar sistemas de proteção.
- Não informa preços, prazos legais locais ou números que não estejam na base.
- Não responde assuntos fora do escopo (ele diz que não tem a informação).

## Guardrails
1. **Fundamentação:** só responde com base nos trechos recuperados da base.
2. **Limiar de relevância:** se nenhum trecho passa do score mínimo, o LLM nem é chamado e o assistente recusa.
3. **Emergência:** frases como "está pegando fogo" acionam uma resposta fixa com o 193, sem passar pelo LLM.
4. **Segurança:** o prompt proíbe orientar desativação de sistemas.
5. **Transparência:** toda resposta cita a fonte e exibe o aviso legal.

## Arquitetura
```
Pergunta ─► detector de emergência ─► (sim) resposta fixa com 193
                │ não
                ▼
        Recuperação BM25 (data/base_conhecimento.json)
                │
     score >= mínimo? ─► (não) recusa educada
                │ sim
                ▼
   Prompt (regras + contexto + perfil + histórico) ─► LLM ─► resposta + fontes
   (sem chave de API: modo offline devolve o trecho mais relevante)
```

## Persistência de contexto
Histórico das últimas 6 mensagens na sessão do Streamlit, mais o perfil (tipo de edificação e UF) enviado ao prompt.
