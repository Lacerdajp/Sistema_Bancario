menu='''
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar Usuário
    [5] Criar conta
    [6] Listar contas
    [7] Sair

Escolha: '''
saldo = 0
limite = 500
extrato=""
numero_de_saques=0
LIMITE_SAQUES=3
usuarios=[]
contas=[]
def Criar_Conta(usuarios:list, contas:list):
    cpf=int(input("Digite o CPF do usuário(somente numeros): "))
    while cpf not in [usuario['cpf'] for usuario in usuarios]:
        print("CPF não cadastrado")
        print("Deseja tentar novamente?")
        print("[1]Sim")
        print("[2]Não")
        opcao=input("Escolha: ")
        if opcao=='1':
            cpf=int(input("Digite o CPF do usuário(somente numeros): "))
        else:
            return
    
    conta={
        'agencia':"0001",
        'numero':len(contas)+1,
        'usuario':[usuario for usuario in usuarios if usuario['cpf']==cpf][0]
    }
    contas.append(conta)
    print("Conta criada com sucesso!")
    return conta

def Criar_Usuario(usuarios:list):
    nome=input("Digite o nome completo: ")
    data_nascimento=input("Digite a data de nascimento(dd/mm/aaaa): ")
    cpf=int(input("Digite o CPF(somente numeros): "))
    while cpf in [usuario['cpf'] for usuario in usuarios]:
        print("CPF já cadastrado")
        print("deseja tentar novamente?")
        print("[1]Sim")
        print("[2]Não")
        opcao=input("Escolha: ")
        if opcao=='1':
            cpf=int(input("Digite o CPF(somente numeros): "))
        else:
            return
    longradouro=input("Digite o longradouro: ")
    numero=input("Digite o numero: ")
    bairro=input("Digite o bairro: ")
    cidade=input("Digite a cidade(sigla): ")
    estado=input("Digite o estado(Sigla): ")
    endereco=f"{longradouro}, {numero} - {bairro} - {cidade} {estado}"
    usuario={
        'nome':nome,
        'data_nascimento':data_nascimento,
        'cpf':cpf,
        'endereco':endereco
    }
    usuarios.append(usuario)
    print(f"Usuário {usuario["nome"]} criado com sucesso!")
    return usuario

def saque(*,saldo,valor, limite, extrato, numero_de_saques,limite_saque):
    if valor <= 0:
        print("Valor inválido")
    elif valor > saldo:
        print("Saldo insuficiente")
    elif numero_de_saques >= limite_saque:
        print("Limite de saques atingido")
    elif valor>limite:
        print("Limite de saque ultrapassado")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor}\n"
        numero_de_saques += 1
        print("Saque efetuado com sucesso!")
    return saldo, extrato, numero_de_saques


def extração(saldo,/,*,extrato):
    print('\n===============EXTRATO===============')
    if extrato == "":
        print("Nenhuma movimentação realizada")
    else:
        print(extrato)
    print(f"Saldo: R$ {saldo}")
    print('====================================\n')


def deposito(saldo,valor, extrato,/):
    if valor <= 0:
        print("Valor inválido")
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor}\n"
        print("Depósito efetuado com sucesso!")
    return saldo, extrato

def listar_contas(contas):
    print('\n===============CONTAS===============')
    for conta in contas:
        print(f"Agencia: {conta['agencia']}")
        print(f"Numero: {conta['numero']}")
        print(f"Usuario: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
        print(f"Endereço: {conta['usuario']['endereco']}")
        print(f"Data de nascimento: {conta['usuario']['data_nascimento']}")
        print("====================================\n")

while True:
    opção = input(menu)
    if opção == '1':
        valor = float(input("Digite o valor a ser depositado: "))
        saldo, extrato = deposito(saldo,valor, extrato)
    elif opção == '2':
        valor = float(input("Digite o valor a ser sacado: "))
        saldo, extrato, numero_de_saques = saque(saldo=saldo,valor=valor, 
                                                 limite=limite, extrato=extrato,
                                                 numero_de_saques=numero_de_saques, limite_saque=LIMITE_SAQUES)
    elif opção == '3':
        extração(saldo, extrato=extrato)
    elif opção == '4':
        Criar_Usuario(usuarios)
    elif opção == '5':
        Criar_Conta(usuarios, contas)
    elif opção == '6':
        listar_contas(contas)
    elif opção == '7':
        print("Saindo...")
        break
    else:
        print("Opção inválida")