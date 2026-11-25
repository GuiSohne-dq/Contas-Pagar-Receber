# Projeto Contas a Pagar e Receber

## 1. Descrição
Aplicação desktop de fluxo de caixa, desenvolvida em Python com Tkinter, para o controle de contas a pagar e receber. Os dados ficam guardados em um arquivo de texto (`contas.txt`), sem uso de banco de dados. Em memória, são mantidos em listas, tuplas e dicionários.

## 2. Estrutura de pastas

```
projeto_contas_gui/
├── docs/          -> documentação (estrutura_dados.md e exemplo_contas.txt)
├── services/      -> regras de negócio e leitura/escrita do arquivo (finance_manager.py)
├── views/         -> interface gráfica Tkinter (app_gui.py)
├── main.py        -> ponto de entrada: é por ele que o programa começa
├── contas.txt     -> arquivo onde as contas ficam salvas
└── README.md      -> este arquivo
```

## 3. Estruturas de dados

- **Tuplas:** `TIPOS` e `STATUS_OPCOES`, opções fixas e imutáveis (Receita/Despesa e Pendente/Pago).
- **Dicionário:** representa uma conta, com os campos `id`, `descricao`, `valor`, `tipo`, `vencimento` e `status`.
- **Lista:** `contas` guarda todos os dicionários de conta em memória.

Detalhes completos em [docs/estrutura_dados.md](docs/estrutura_dados.md).

## 4. Formato do arquivo contas.txt

Uma conta por linha, campos separados por `;`, sem espaços e sem aspas, na ordem:
`id;descricao;valor;tipo;vencimento;status`

Exemplo:

```
5;Aluguel Praia;400.00;Despesa;2027/01/01;Pago
```

Um exemplo com várias contas está em [docs/exemplo_contas.txt](docs/exemplo_contas.txt).

## 5. Funcionalidades

- Listar as contas em duas tabelas (Treeview): uma para receitas e outra para despesas.
- Adicionar uma conta por um formulário.
- Alternar uma conta entre paga e pendente
- Excluir uma conta, com confirmação.
- Mostrar o total de receitas, despesas e o saldo.
- Salvar as alterações automaticamente no `contas.txt`.

## 6. Validações

Antes de adicionar uma conta, o programa confere os dados e avisa com `messagebox`:

- a descrição não pode estar vazia nem conter `;`;
- o valor deve ser um número com ponto decimal e maior que zero;
- o vencimento deve estar no formato `AAAA/MM/DD`;
- tipo e status são escolhidos em listas (Combobox) alimentadas pelas tuplas.

Se o `contas.txt` não existir, o programa começa com a lista vazia e cria o arquivo ao salvar a primeira conta.

## 7. Como executar

Abra o terminal na pasta do projeto e rode:

```
python main.py
```

É necessário o Python 3 com Tkinter, que já vem na instalação padrão.