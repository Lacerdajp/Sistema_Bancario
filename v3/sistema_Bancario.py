from abc import ABC, abstractmethod
from datetime import datetime

class Conta:
    def __init__(self, cliente, numero):
       self._saldo=0
       self._numero=numero
       self._cliente=cliente
       self._agencia="0001"
       self._historico=Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def cliente(self):
        return self._cliente
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico
    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido")
        elif valor > self._saldo:
            print("Saldo insuficiente")
        else:
            self._saldo -= valor
            print("Saque efetuado com sucesso!")
            return True
        return False
    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido")
        else:
            self._saldo += valor
            print("Depósito efetuado com sucesso!")
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero,limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite=limite
        self.limite_saques=limite_saques
    def sacar(self, valor):
        numero_de_saques=len({transacao for transacao in self._historico._transacoes if transacao["tipo"]==Saque.__name__})
        if numero_de_saques >= self.limite_saques:
            print("Limite de saques atingido")
            return False
        elif valor>self.limite:
            print("Limite de saque ultrapassado")
            return False
        else:
            return super().sacar(valor)
    def __str__(self):
        return f'''
        Agencia: {self.agencia}
        Numero: {self.numero}
        Usuario: {self.cliente.nome}
        CPF: {self.cliente.cpf}
        Endereço: {self.cliente.endereco}
        Data de nascimento: {self.cliente.data_nascimento}
        '''
class Historico:
    def __init__(self):
        self._transacoes=[]
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo":transacao.__class__.__name__,
            "valor":transacao.valor,
            "data":datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor=valor
    @property
    def valor(self):
        return self._valor
    def registrar(self,conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
class Saque(Transacao):
    def __init__(self, valor):
        self._valor=valor
    @property
    def valor(self):
        return self._valor
    def registrar(self,conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
class Cliente:
    def __init__(self,endereco):
        self.endereco=endereco
        self.contas=[]
    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)
    def adicionar_conta(self,conta):
        self.contas.append(conta)
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento,endereco):
        super().__init__(endereco)
        self.nome=nome
        self.cpf=cpf
        self.data_nascimento=data_nascimento

def menu():
    return input('''
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar Usuário
    [5] Criar conta
    [6] Listar contas
    [7] Sair
    Escolha: ''')
def Criar_Conta(usuarios:list, contas:list):
    cpf=(input("Digite o CPF do usuário(somente numeros): "))
    if not cpf.isdigit():
        print("CPF inválido")
        return
    while cpf not in [usuario.cpf for usuario in usuarios]:
        print("CPF não cadastrado")
        print("Deseja tentar novamente?")
        print("[1]Sim")
        print("[2]Não")
        opcao=input("Escolha: ")
        if opcao=='1':
            cpf=(input("Digite o CPF do usuário(somente numeros): "))
        else:
            return
    cliente=[usuario for usuario in usuarios if usuario.cpf==cpf]
    cliente=cliente[0] if cliente else None
    if not cliente:
        print("CPF não cadastrado")
        return
    conta=ContaCorrente(cliente, len(contas)+1)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("Conta criada com sucesso!")
    return conta

def Criar_Usuario(usuarios:list):
    nome=input("Digite o nome completo: ")
    data_nascimento=input("Digite a data de nascimento(dd/mm/aaaa): ")
    cpf=(input("Digite o CPF(somente numeros): "))
    while not cpf.isdigit():
        print("CPF inválido")
        cpf=(input("Digite o CPF(somente numeros): "))
    while cpf in [usuario.cpf for usuario in usuarios]:
        print("CPF já cadastrado")
        print("deseja tentar novamente?")
        print("[1]Sim")
        print("[2]Não")
        opcao=input("Escolha: ")
        if opcao=='1':
            cpf=(input("Digite o CPF(somente numeros): "))
        else:
            return
    longradouro=input("Digite o longradouro: ")
    numero=input("Digite o numero: ")
    bairro=input("Digite o bairro: ")
    cidade=input("Digite a cidade(sigla): ")
    estado=input("Digite o estado(Sigla): ")
    endereco=f"{longradouro}, {numero} - {bairro} - {cidade} {estado}"
    usuario=PessoaFisica(nome, cpf, data_nascimento,endereco)
    usuarios.append(usuario)
    print(f"Usuário {usuario.nome} criado com sucesso!")
    return usuario

def saque(clientes):
    cpf=(input("Digite o CPF do usuário(somente numeros): "))
    if not cpf.isdigit():
        print("CPF inválido")
        return
    cliente=[cliente for cliente in clientes if cliente.cpf==cpf]
    cliente=cliente[0] if cliente else None
    if not cliente:
        print("CPF não cadastrado")
        return
    valor=float(input("Digite o valor a ser sacado: "))
    transacao=Saque(valor)
    conta=recuperar_conta(cliente)
    if not conta:
        print("Conta não encontrada")
        return
    cliente.realizar_transacao(conta,transacao)
def extração(clientes):
    cpf=(input("Digite o CPF do usuário(somente numeros): "))
    if not cpf.isdigit():
        print("CPF inválido") 
        return
    cliente=[cliente for cliente in clientes if cliente.cpf==cpf]
    cliente=cliente[0] if cliente else None
    if not cliente:
        print("CPF não cadastrado")
        return
    conta=recuperar_conta(cliente)
    if not conta:
        print("Conta não encontrada")
        return
    print('\n===============EXTRATO===============')
    extrato=""
    transacoes=conta.historico.transacoes
    if not transacoes:
        print("Nenhuma movimentação realizada")
    else:
        for transacao in transacoes:
            extrato+=f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - {transacao['data']}\n"
        print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print('====================================\n')

def recuperar_conta(cliente):
    numero_conta=input("Digite o numero da conta: ")
    conta=[conta for conta in cliente.contas if int(numero_conta)==int(conta.numero)]
    conta=conta[0] if conta else None
    return conta
def deposito(clientes):

    cpf=(input("Digite o CPF do usuário(somente numeros): "))
    if cpf.isdigit():
        pass
    else:
        print("CPF inválido")
        return
    cpf=int(cpf)
    cliente=[cliente for cliente in clientes if cliente.cpf==cpf]
    cliente=cliente[0] if cliente else None
    if not cliente:
        print("CPF não cadastrado")
        return
    valor=float(input("Digite o valor a ser depositado: "))
    transacao=Deposito(valor)
    conta=recuperar_conta(cliente)
    if not conta:
        print("Conta não encontrada")
        return
    cliente.realizar_transacao(conta,transacao)
def listar_contas(contas):
    print('\n===============CONTAS===============')
    for conta in contas:
        print(f"Agencia: {conta.agencia}")
        print(f"Numero: {conta.numero}")
        print(f"Usuario: {conta.cliente.nome}")
        print(f"CPF: {conta.cliente.cpf}")
        print(f"Endereço: {conta.cliente.endereco}")
        print(f"Data de nascimento: {conta.cliente.data_nascimento}")
        print("====================================\n")


def main():
    clientes=[]
    contas=[]
    while True:
        opção = menu()
        if opção == '1':
           deposito(clientes)
        elif opção == '2':
            saque(clientes)
        elif opção == '3':
            extração(clientes)
        elif opção == '4':
            Criar_Usuario(clientes)
        elif opção == '5':
            Criar_Conta(clientes, contas)
        elif opção == '6':
            listar_contas(contas)
        elif opção == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida")
main()