# 3. Prompts

O prompt completo está em `src/prompts.py`. Resumo do raciocínio de cada bloco:

| Bloco | Objetivo |
|-------|----------|
| Papel e público | Define o Sentinela e para quem ele fala |
| Regra 1 (só contexto) | Reduz alucinação: nada de norma, prazo ou preço fora da base |
| Regra 2 (admitir que não sabe) | Comportamento explícito quando falta informação |
| Regra 3 (segurança primeiro) | Nunca orientar desativar ou burlar sistemas |
| Regra 4 (limites) | Não substitui responsável técnico nem Bombeiros |
| Regra 5 (fontes) | Rastreabilidade da resposta |
| Regra 6 (perfil) | Personalização sem inventar exigências locais |
| Estilo | Respostas curtas, listas para passos, próxima ação sugerida |

## Exemplos de comportamento esperado

**Dentro da base**
> Usuário: Posso pintar os sprinklers do teto?
> Sentinela: Não. Chuveiros pintados ou obstruídos podem não acionar corretamente... *(cita NBR 10897)*

**Fora da base**
> Usuário: Quanto custa recarregar um extintor de 6 kg?
> Sentinela: Não encontrei essa informação na minha base... consulte o responsável técnico...

**Segurança**
> Usuário: Posso desligar a central para parar o alarme?
> Sentinela: Silenciar o buzzer é aceitável, mas desligar a central deixa o local desprotegido...

## Parâmetros
`temperature=0.2` (respostas estáveis), `max_tokens=600`, histórico limitado a 6 mensagens. O modelo é configurável pela variável `SENTINELA_MODEL`.
