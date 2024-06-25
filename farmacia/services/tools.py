def convert_seconds(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def convert_tuple_list(tuple_list):
    converted_list = []
    for item in tuple_list:
        if len(item) == 3:
            index, seconds1, seconds2 = item
            formatted_time1 = convert_seconds(seconds1)
            formatted_time2 = convert_seconds(seconds2)
            converted_list.append((index, formatted_time1, formatted_time2))
        elif len(item) == 2:
            index, seconds = item
            formatted_time = convert_seconds(seconds)
            converted_list.append((index, formatted_time))
    return converted_list

def create_receipt(number_in_line):
    receipt_width = 40
    border = '+' + '-' * (receipt_width - 2) + '+'
    space = ' ' * (receipt_width - 2)

    header = '|{:^{width}}|'.format('RECIBO', width=receipt_width-2)
    line1 = '|{:^{width}}|'.format(f'Número: {number_in_line}', width=receipt_width-2)
    line2 = '|{:^{width}}|'.format(f'Producto vendido: Remedio', width=receipt_width-2)
    footer = '|{:^{width}}|'.format('Gracias por su compra!', width=receipt_width-2)

    receipt_lines = [
        border,
        header,
        border,
        line1,
        line2,
        border,
        footer,
        border
    ]

    receipt = '\n'.join(receipt_lines)

    return receipt

def create_call_sign(number_in_line):
    sign_width = 40
    border = '+' + '-' * (sign_width - 2) + '+'
    space = ' ' * (sign_width - 2)
    
    header = '|{:^{width}}|'.format('PRÓXIMO EN LA FILA', width=sign_width-2)
    line1 = '|{:^{width}}|'.format('POR FAVOR ACÉRQUESE AL MOSTRADOR.', width=sign_width-2)
    line2 = '|{:^{width}}|'.format(f'NÚMERO: {number_in_line}', width=sign_width-2)
    footer = '|{:^{width}}|'.format('GRACIAS!', width=sign_width-2)
    
    sign_lines = [
        border,
        header,
        border,
        line1,
        border,
        line2,
        border,
        footer,
        border
    ]
    
    sign = '\n'.join(sign_lines)
    
    return sign

def create_ticket(number_in_line):
    ticket_width = 30
    border = '+' + '-' * (ticket_width - 2) + '+'
    space = ' ' * (ticket_width - 2)

    header = '|{:^{width}}|'.format('TICKET', width=ticket_width-2)
    line1 = '|{:^{width}}|'.format('Tu numero en la fila es:', width=ticket_width-2)
    line2 = '|{:^{width}}|'.format(f'{number_in_line}', width=ticket_width-2)
    footer = '|{:^{width}}|'.format('Espere a ser llamado.', width=ticket_width-2)

    ticket_lines = [
        border,
        header,
        border,
        line1,
        line2,
        border,
        footer,
        border
    ]

    ticket = '\n'.join(ticket_lines)

    return ticket
