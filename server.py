import socket
import json
import datetime

HOST = 'localhost'
PORT = 5500

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("Waiting client connection....")

array_sold_itens = []

while True:
    msg, client_network = server.recvfrom(PORT)
    print("Servidor Funcionando ")

    message = json.loads(msg.decode('utf-8'))

    if message['code'] == '1':
        print("Resposta vendedor")

        if int(message['store']) > 3:
            print("Loja não existe")
            answer = "ERRO"
            server.sendto(answer.encode("utf-8"), client_network)
            continue

        if message['day'] > 31 or message['day'] < 1:
            print("Dia inválido")
            answer = "ERRO"
            server.sendto(answer.encode("utf-8"), client_network)
            continue
        elif message['month'] > 12 or message['month'] < 1:
            print('Mes inválido')
            answer = "ERRO"
            server.sendto(answer.encode("utf-8"), client_network)
            continue
        elif len(message['year'].__str__()) != 4:
            print("Mês Inválido")
            answer = "ERRO"
            server.sendto(answer.encode("utf-8"), client_network)
            continue

        date = datetime.date(message['year'], message['month'], message['day'])

        item = {
            'store': message['store'],
            'sold_price': message['sold_price'],
            'code': message['code'],
            'name': message['name'],
            'date': date
        }

        array_sold_itens.append(item)
        answer = "Item recebido\n"
        server.sendto(answer.encode("utf-8"), client_network)
    elif message['code'] == '2':
        print("Resposta Gerente")

        if int(message['options']) > 5:
            print("Opção inexistente selecionada")
            answer = "ERRO"
            server.sendto(answer.encode("utf-8"), client_network)
            continue


        if message['options'] == '1':
            value = 0
            for item in array_sold_itens:
                if item['name'] == message['value']:
                    value += 1

            if value == 0:
                answer = "Vendedor não vendeou nada ou não existe"
            else:
                answer = f"Vendedor vendeu {value} unidade/s"

            server.sendto(answer.encode("utf-8"), client_network)
        elif message['options'] == '2':

            if int(message['value']) > 3:
                print("Opção inexistente selecionada")
                answer = "ERRO"
                server.sendto(answer.encode("utf-8"), client_network)
                continue

            store = ''
            if int(message['value']) == 1:
                store = 'Atacado Judson'
            elif int(message['value']) == 2:
                store = 'Supermecado Helioporto'
            elif int(message['value']) == 3:
                store = 'Açougue Carnificina'

            value = 0
            for item in array_sold_itens:
                if item['store'] == message['value']:
                    value += 1

            if value == 0:
                answer = f"{store} não vendeou"
            else:
                answer = f"{store} vendeu {value} unidade/s"

            server.sendto(answer.encode("utf-8"), client_network)
        elif message['options'] == '3':

            if message['value']['start_month'] > 12 or message['value']['start_month'] < 1:
                print('Mes inválido')
                answer = "ERRO"
                server.sendto(answer.encode("utf-8"), client_network)
                continue
            elif message['value']['end_month'] > 12 or message['value']['end_month'] < 1:
                print('Mes inválido')
                answer = "ERRO"
                server.sendto(answer.encode("utf-8"), client_network)
                continue
            elif len(message['value']['year'].__str__()) != 4:
                print("Mês Inválido")
                answer = "ERRO"
                server.sendto(answer.encode("utf-8"), client_network)
                continue

            value = 0

            year_search = message['value']['year']
            start_month = message['value']['start_month']
            end_month = message['value']['end_month']

            for item in array_sold_itens:
                if item['date'].year == year_search:
                    if item['date'].month <= end_month and item['date'].month >= start_month:
                        value += item['sold_price']

            answer = f"A arecadação durante essas datas são {value}"
            server.sendto(answer.encode("utf-8"), client_network)
        elif message['options'] == '4':
            max_value = 0
            name = ''
            for item in array_sold_itens:
                add = 0
                for item_double in array_sold_itens:
                    if item['name'] == item_double['name']:
                        add += item_double['sold_price']
                        if add > max_value:
                            max_value = add
                            name = item['name']

            answer = f"{name} tem o maior valor de vendas acumuladas {max_value}"
            server.sendto(answer.encode("utf-8"), client_network)
    else:
        print("Mensagem Inválida...")
        answer = "ERRO"
        server.sendto(answer.encode("utf-8"), client_network)

print("Ecerrando server")
