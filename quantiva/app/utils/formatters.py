def format_currency_short(value):
    if value is None:
        return "$0"
    value = float(value)
    if value >= 1000000000:
        return f"${value / 1000000000:.1f} B"
    elif value >= 1000000:
        return f"${value / 1000000:.1f} M"
    elif value >= 1_000:
        return f"${value / 1000:.1f} K"
    else:
        return f"${value:,.0f}"
def format_number_short(value):

    value=float(value or 0)

    if value>=1000000000:
        return (str(round(value/1000000000,1))+' B')

    if value>=1000000:
        return (str(round(value/1000000,1))+' M')

    if value>=1000:
        return (str(round(value/1000,1))+' K')

    return format(int(value),',')