import socket
import json

HOST = 'localhost'
PORT = 5500

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    print("###################")
    print("1. Vendedor")
    print("2. Gerente")
    print("3. Encerrar aplicação")
    print("###################")

    message = input("\nInforme sua função: ")
    if message == '1':
        name = input("Bem vindo, informe seu nome: ")

        print("\n###################")
        print('Lojas')
        print('1 - Atacado Judson')
        print('2 - Supermecado Helioporto')
        print('3 - Açougue Carnificina')
        print("###################")
        store = input('Informe a loja: ')

        if store == '1':
            print("\nAtacado Judson selecionado")
        elif store == '2':
            print("\nSupermecado Helioporto selecionado")
        elif store == '3':
            print("\nAçougue Carnificina selecionado")
        else:
            print(f"{store} não encontrada")

        price = float(input("\nDigite o valor da venda :"))

        day = int(input("Digite o dia da venda: "))
        month = int(input("Digite o mes da venda: "))
        year = int(input("Digite o ano da venda: "))

        soldItem = {
                    'store': store,
                    'day': day,
                    'month': month,
                    'year': year,
                    'sold_price': price,
                    'code': message,
                    'name': name
        }

        msg = json.dumps(soldItem)
        client.sendto(msg.encode("utf-8"), (HOST, PORT))
        print("Item enviado ao servidor")
    elif message == '2':
        print("Menu")
        print("----------------")

        print("1 - Total de vendas do vendedor")
        print("2 - Total de vendas de uma loja")
        print("3 - Total de vendas da rede de lojas")
        print("4 - Melhor vendedor")
        print("5 -  Melhor loja\n")

        options = input("Qual ação deseja realizar: ")

        if options == '1':
            value = input('Digite o nome do funcionário: ')
            info = {'value': value, 'code': message, 'options': options}
            msg = json.dumps(info)
            client.sendto(msg.encode("utf-8"), (HOST, PORT))

        elif options == '2':
            value = input('Digite o código de identificação da loja: ')
            info = {'value': value, 'code': message, 'options': options}
            msg = json.dumps(info)
            client.sendto(msg.encode("utf-8"), (HOST, PORT))
        elif options == '3':
            year = int(input('Digite o ano do perído que quer checar: '))
            start_month = int(input('Digite o mes inicial: '))
            end_month = int(input('Digite o mes final: '))
            value = {'year': year, 'start_month': start_month, 'end_month': end_month}
            info = {'value': value, 'code': message, 'options': options}
            msg = json.dumps(info)
            client.sendto(msg.encode("utf-8"), (HOST, PORT))
        else:
            value = ''
            info = {'value': value, 'code': message, 'options': options}
            msg = json.dumps(info)
            client.sendto(msg.encode("utf-8"), (HOST, PORT))
    elif message == "3":
        break
    else:
        info = {'code': message}
        msg = json.dumps(info)
        client.sendto(msg.encode("utf-8"), (HOST, PORT))

    server_awser, server_network = client.recvfrom(PORT)
    aswer = server_awser.decode("utf-8")
    print(f"\nServidor me respondeu: {aswer}\n")

print("Encerrando sessão")
client.close()
