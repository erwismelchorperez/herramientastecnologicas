from sqlalchemy import case
MESES = {
    'ene': 1,
    'feb': 2,
    'mar': 3,
    'abr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'ago': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dic': 12

}
def month_case(column):
    return case(
        *[
            (column == mes, numero)
            for mes, numero in MESES.items()
        ]

    )
def month_number(mes):
    meses = {
        'ene':1,
        'feb':2,
        'mar':3,
        'abr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'ago':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dic':12
    }

    return meses.get(mes.lower(),1)