"""Simulação simples: próxima data de manutenção a partir da última realizada.

Os intervalos abaixo são valores de referência DEMONSTRATIVOS, alinhados à base de
conhecimento (data/base_conhecimento.json). Confirme sempre na norma vigente e com o
responsável técnico antes de usar em uma edificação real.
"""
from datetime import date

INTERVALOS_MESES = {
    "Extintor - inspeção visual (nível 1)": 1,
    "Extintor - manutenção completa (nível 2)": 12,
    "Extintor - ensaio hidrostático (nível 3)": 60,
}


def _somar_meses(d: date, meses: int) -> date:
    ano = d.year + (d.month - 1 + meses) // 12
    mes = (d.month - 1 + meses) % 12 + 1
    dias_no_mes = [31, 29 if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0) else 28,
                   31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return date(ano, mes, min(d.day, dias_no_mes[mes - 1]))


def proxima_manutencao(item: str, ultima: date, hoje: date | None = None) -> dict:
    if item not in INTERVALOS_MESES:
        raise ValueError(f"Item desconhecido: {item}")
    hoje = hoje or date.today()
    proxima = _somar_meses(ultima, INTERVALOS_MESES[item])
    dias = (proxima - hoje).days
    if dias < 0:
        situacao = f"VENCIDA há {-dias} dia(s)"
    elif dias <= 30:
        situacao = f"vence em {dias} dia(s) — agendar"
    else:
        situacao = f"em dia ({dias} dias restantes)"
    return {"item": item, "ultima": ultima, "proxima": proxima, "situacao": situacao}
