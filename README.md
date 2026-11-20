# Projeto Contas a Pagar e Receber

## 1. Descrição
Aplicação de Fluxo de Caixa desenvolvida em Python com Tkinter para o controle de contas a pagar e receber, utilizando arquivos de texto (.txt) para o armazenamento de dados em vez de um banco de dados.

## 2. Estrutura de pastas
```
projeto_contas_gui/
├── docs/          -> documentação (estrutura_dados.md e exemplo_contas.txt)
├── services/      -> regras de negócio e arquivo (finance_manager.py)
├── views/         -> interface gráfica Tkinter (app_gui.py)
├── main.py        -> ponto de entrada: é por ele que o programa começa
└── contas.txt     -> arquivo onde as contas ficam salvas
```

## 3. Estruturas de dados
- Tuplas: TIPOS e STATUS_OPCOES, opções fixas e imutáveis(Receita/Despesa e Pendente/Pago)
- Dicionário: Representa uma conta, com os campos, id, descricao, valor, tipo, vencimento e status
- Lista: Contas, guarda todos os dicionários de conta em memória

## 4. Formato do arquivo contas.txt
Uma conta por linha, com os campos separados por ';', sem espaços e sem aspas na ordem:
`id;descricao;valor;tipo;vencimento;status`

Exemplos:
```5;Aluguel Praia;400.00;Despesa;2027/01/01;Pago```

## 5. Como executar
Dentro da pasta do projeto, rode no terminal:

```
python main.py
```