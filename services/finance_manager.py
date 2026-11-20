TIPOS = ('Receita', 'Despesa')
STATUS_OPCOES = ('Pendente', 'Pago')

def carregar_contas(caminho='contas.txt'):
    contas = []
    try:
        with open(caminho, 'r', encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 6:
                    contas.append({
                        'id': int(dados[0]),
                        'descricao': dados[1],
                        'valor': float(dados[2]),
                        'tipo': dados[3],
                        'vencimento': dados[4],
                        'status': dados[5],
                    })
    except FileNotFoundError:
        pass
    return contas

def salvar_contas(contas, caminho='contas.txt'):
    with open(caminho, 'w', encoding='utf-8') as arq:
        for conta in contas:
            linha = ';'.join([
                str(conta['id']),
                conta['descricao'],
                str(conta['valor']),
                conta['tipo'],
                conta['vencimento'],
                conta['status']
            ])
            arq.write(linha + '\n')

def calcular_resumo(contas):
    rec = sum(c['valor'] for c in contas if c['tipo'] == 'Receita')
    desp = sum(c['valor'] for c in contas if c['tipo'] == 'Despesa')
    return rec, desp, rec - desp

def proximo_id(contas):
    if not contas:
        return 1
    return max(c['id'] for c in contas) + 1

def adicionar_conta(contas, descricao, valor, tipo, vencimento, status):
    conta = {
        'id': proximo_id(contas),
        'descricao': descricao,
        'valor': valor,
        'tipo': tipo,
        'vencimento': vencimento,
        'status': status
    }
    contas.append(conta)
    return conta

def excluir_conta(contas, id_conta):
    for conta in contas:
        if conta['id'] == id_conta:
            contas.remove(conta)
            return True
    return False

def alterar_status(contas, id_conta, novo_status):
    for conta in contas:
        if conta['id'] ==id_conta:
            conta['status'] = novo_status
            return True
        return False