import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.finance_manager import (
    TIPOS, STATUS_OPCOES,
    carregar_contas, salvar_contas, calcular_resumo,
    adicionar_conta, excluir_conta, alterar_status
)

class App:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Gerenciador financeiro')
        self.janela.geometry('1000x560')
        self.contas = carregar_contas()

        self.montar_titulo()
        self.montar_formulario()
        self.montar_paineis()
        self.montar_botoes()
        self.atualizar_tela()

    def montar_titulo(self):
        tk.Label(self.janela, text='Gerenciador Financeiro', font=('Arial', 16, 'bold')).pack(pady=10)

    def montar_formulario(self):
        painel = tk.Label(self.janela, text='Detalhes para serem preenchidos:', padx=10, pady=10)
        painel.pack(fill='x', padx=15, pady=5)

        tk.Label(painel, text='Descrição').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_descricao = tk.Entry(painel, width=25)
        self.entry_descricao.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(painel, text='Valor:').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_valor = tk.Entry(painel, width=12)
        self.entry_valor.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(painel, text='Vencimento (AAAA/MM/DD):').grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.entry_vencimento = tk.Entry(painel, width=12)
        self.entry_vencimento.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(painel, text='Tipo:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.combo_tipo = ttk.Combobox(painel, values=TIPOS, state='readonly', width=22)
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(painel, text='Status:').grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.combo_status = ttk.Combobox(painel, values=STATUS_OPCOES, state='readonly',  width=10)
        self.combo_status.current(0)
        self.combo_status.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(painel, text='Adicionar', command=self.on_adicionar).grid(row=1, column=5, padx=5, pady=5)

    def criar_tree(self,painel):
        colunas = ('id', 'descricao', 'valor', 'vencimento', 'status')
        larguras = (30, 110, 65, 80, 65)
        nomes = ('ID', 'Descrição', 'Valor', 'Vencimento', 'Status')

        tree = ttk.Treeview(painel, columns=colunas, show='headings', height=10)
        for col, nome, larg in zip(colunas, nomes, larguras):
            tree.heading(col, text=nome)
            tree.column(col, width=larg, anchor='center')
        tree.pack(fill='both', expand=True)
        return tree

    def montar_paineis(self):
        area = tk.Frame(self.janela)
        area.pack(fill='both', expand=True, padx=15, pady=5)
        area.columnconfigure(0, weight=3)
        area.columnconfigure(1, weight=3)
        area.columnconfigure(2, weight=2, minsize=200)
        area.rowconfigure(0, weight=1)

        painel_rec = tk.LabelFrame(area, text='Receitas', padx=5, pady=5)
        painel_rec.grid(row=0, column=0, sticky='nswe', padx=5)
        self.tree_receitas = self.criar_tree(painel_rec)

        painel_desp = tk.LabelFrame(area, text='Despesas', padx=5, pady=5)
        painel_desp.grid(row=0, column=1, sticky='nswe', padx=5)
        self.tree_despesas = self.criar_tree(painel_desp)

        #Ao selecionar numa tabela, limpa a seleção da outra
        self.tree_receitas.bind('<<TreeviewSelect>>',
                                lambda e: self.tree_despesas.selection_remove(self.tree_despesas.selection()))
        self.tree_despesas.bind('<<TreeviewSelect>>',
                                lambda e: self.tree_receitas.selection_remove(self.tree_receitas.selection()))

        painel_total = tk.LabelFrame(area, text='Total', padx=10, pady=10)
        painel_total.grid(row=0, column=2, sticky='nswe', padx=5)
        self.lbl_receitas = tk.Label(painel_total, text='Receitas: R$ 0.00', font=('Arial', 11))
        self.lbl_receitas.pack(anchor='w', pady= 5)
        self.lbl_despesas = tk.Label(painel_total, text='Despesas: R$ 0.00', font=('Arial', 11))
        self.lbl_despesas.pack(anchor='w', pady= 5)
        self.lbl_saldo = tk.Label(painel_total, text='Saldo: R$ 0.00', font=('Arial', 12, 'bold'))
        self.lbl_saldo.pack(anchor='w', pady= 15)

    def montar_botoes(self):
        barra = tk.Frame(self.janela)
        barra.pack(pady=10)
        tk.Button(barra, text='Excluir Selecionada', command=self.on_excluir).pack(side='left', padx=10)
        tk.Button(barra, text='Marcar Como Pago', command=self.on_marcar_pago).pack(side='left', padx=10)

    # Atualização
    def atualizar_tela(self):
        for tree in (self.tree_receitas, self.tree_despesas):
            tree.delete(*tree.get_children())

        for c in self.contas:
            tree = self.tree_receitas if c['tipo'] == 'Receita' else self.tree_despesas
            tree.insert('', 'end', values=(
                c['id'], c['descricao'], f"{c['valor']:.2f}", c['vencimento'], c['status']))

        rec, desp, saldo = calcular_resumo(self.contas)
        self.lbl_receitas.config(text=f'Receitas: R$ {rec:.2f}')
        self.lbl_despesas.config(text=f'Despesas: R$ {desp:.2f}')
        self.lbl_saldo.config(text=f'Saldo: R$ {saldo:.2f}', fg='red' if saldo < 0 else 'green')

    def id_selecionado(self):
        for tree in (self.tree_receitas, self.tree_despesas):
            sel = tree.selection()
            if sel:
                return int(tree.item(sel[0])['values'][0])
        return None

    #Ações dos botõse

    def on_adicionar(self):
        descricao = self.entry_descricao.get().strip()
        valor_txt = self.entry_valor.get().strip()
        vencimento = self.entry_vencimento.get().strip()
        tipo = self.combo_tipo.get()
        status = self.combo_status.get()

        if not descricao:
            messagebox.showwarning('Atenção', 'Preencha a descrição')
            return
        if ';' in descricao:
            messagebox.showwarning('Atenção', 'A descrição não pode conter (;)')
            return

        try:
            datetime.strptime(descricao, '%Y/%m/%d')
        except ValueError:
            messagebox.showerror('Erro', 'Data inválida, use o formato AAAA/MM/DD (Ex: 2026/12/25)')

        adicionar_conta(self.contas, descricao, valor_txt,  tipo, vencimento, status)
        salvar_contas(self.contas)
        self.atualizar_tela()

    def on_excluir(self):
        id_conta = self.id_selecionado()
        if id_conta is None:
            messagebox.showinfo('Atenção', 'Selecione umca onta na tabela')
            return
        if messagebox.askyesno('Confirmar', f'Excluir a conta {id_conta}?'):
            excluir_conta(self.contas, id_conta)
            salvar_contas(self.contas)
            self.atualizar_tela()

    def on_marcar_pago(self):
        id_conta = self.id_selecionado()
        if id_conta is None:
            messagebox.showinfo('Atenção', 'Selecione uma conta na tabela')
            return
        alterar_status(self.contas, id_conta, 'Pago')
        salvar_contas(self.contas)
        self.atualizar_tela()

def iniciar():
    janela = tk.Tk()
    App(janela)
    janela.mainloop()