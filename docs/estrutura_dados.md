x# Estrutura de Dados

## 1. Tuplas (constantes)
```
TIPOS = ('Receita', 'Despesa') 
STATUS_OPCOES = ('Pendente', 'Pago') 
```
Usado para definir as regras de validação e são imutáveis. Além disso, diferenciam maiúsculas de minúsculas: escrever 'despesa' com 'd' minúsculo será rejeitado.

## 2. Dicionário (uma conta)
| Campo      | Tipo  | Exemplo         |
|------------|-------|-----------------|
| id         | int   | 1               |
| descricao  | str   | "Conta pessoal" |
| valor      | float | 320.00          |
| tipo       | str   | Receita         |
| vencimento | str   | 2026/12/25      |
| status     | str   | Pendente        |

```
conta = {
    'id': 1,
    'descricao': 'Conta pessoal',
    'valor': 320.00,
    'tipo': 'Receita',
    'vencimento': '2026/12/25',
    'status': 'Pendente'
}
```

## 3. Lista (todas as contas)
Guarda todas as contas

```
contas = [
    {'id':1, 'descricao':'A pagar', 'valor': 27.00, 'tipo': 'Despesa', 'vencimento': '2026/12/25', 'status': 'Pendente'},
    {'id':2, 'descricao':'A ganhar', 'valor': 400.00, 'tipo': 'Receita', 'vencimento': '2026/10/04', 'status': 'Pago'}
]
```


## 4. Formato do arquivo contas.txt
O formato do arquivo é composto por uma linha para cada conta e possui 6 colunas separadas por ';', seguindo a ordem: id, descricao, valor, tipo, vencimento e status.
Formato da ordem:
```
1;A pagar;27.00;Despesa;2026/12/25;Pendente
```

| Posição | Campo      | Tipo  |
|---------|------------|-------|
| 0       | id         | int   |
| 1       | descricao  | str   |
| 2       | valor      | float |
| 3       | tipo       | str   |
| 4       | vencimento | str   |
| 5       | status     | str   |

## 5. Regras e cuidados
### 5.1 Decimal com ponto
- Regra: o valor deve usar ponto (.) como separador decimal, nunca vírgula. Exemplo: 27.00 e não 27,00.
- Por quê: float('27,00') gera um ValueError. Se esse erro não for tratado, o programa fecha na hora da leitura do arquivo ou do cadastro.
- Onde conferir: antes de gravar, no clique em Salvar. A conversão com float() fica dentro de um try/except; se der ValueError, o programa mostra um aviso e não grava a conta.

### 5.2 Maiúsculas em tipo e status
- Regra: tipo e status devem ser exatamente um dos valores das tuplas: Receita ou Despesa; Pendente ou Pago. Escrever 'despesa' em minúsculo não vale.
- Por quê: 'despesa' == 'Despesa' é False. Uma conta com a grafia errada fica fora das somas de calcular_resumo e o saldo sai errado, sem nenhum erro visível.
- Onde conferir: na tela, o usuário escolhe de uma lista alimentada pelas tuplas TIPOS e STATUS_OPCOES (em vez de digitar), e ao carregar o arquivo o valor lido pode ser conferido com "in TIPOS" / "in STATUS_OPCOES".

### 5.3 Data no formato AAAA/MM/DD
- Regra: o vencimento usa o formato AAAA/MM/DD, igual em todo o projeto (tela, memória e arquivo), sem aspas no .txt.
- Por quê: o Python compara texto da esquerda para a direita. Com o ano na frente, a ordem do texto é a ordem do calendário. Em DD/MM/AAAA, '05/01/2027' < '25/12/2026' dá True, embora janeiro de 2027 venha depois.
- Onde conferir: ao salvar, verificando o formato digitado antes de gravar.