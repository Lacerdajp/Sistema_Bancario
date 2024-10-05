menu='''
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

Escolha: '''
saldo = 0
limite = 500
extrato=""
numero_de_saques=0
LIMITE_SAQUES=3

while True:
    opção = input(menu)
    if opção == '1':
        valor = float(input("Digite o valor a ser depositado: "))
        if valor <= 0:
            print("Valor inválido")
        else:
            saldo += valor
            extrato += f"Depósito: R$ {valor}\n"
            print("Depósito efetuado com sucesso!")
    elif opção == '2':
        valor = float(input("Digite o valor a ser sacado: "))
        if valor <= 0:
            print("Valor inválido")
        elif valor > saldo:
            print("Saldo insuficiente")
        elif numero_de_saques >= LIMITE_SAQUES:
            print("Limite de saques atingido")
        elif valor>limite:
            print("Limite de saque ultrapassado")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor}\n"
            numero_de_saques += 1
            print("Saque efetuado com sucesso!")
    elif opção == '3':
        print('\n===============EXTRATO===============')
        if extrato == "":
            print("Nenhuma movimentação realizada")
        else:
            print(extrato)
        print(f"Saldo: R$ {saldo}")
        print('====================================\n')
            
    elif opção == '4':
        print("Saindo...")
        break
    else:
        print("Opção inválida")