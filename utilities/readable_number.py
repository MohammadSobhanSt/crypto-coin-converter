def readable_number(number: str):
    if '.' in number:
        integer_part, decimal_part = number.split('.')
        return f"{int(integer_part):,}.{decimal_part}"
    else:
        return f"{int(number):,}"