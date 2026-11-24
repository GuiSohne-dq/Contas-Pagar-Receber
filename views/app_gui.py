import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.finance_manager import (
    TIPOS, STATUS_OPCOES,
    carregar_contas, salvar_contas, calcular_resumo,
    adicionar_conta, excluir_conta, alterar_status
)

# ---------- cores ----------
COR_FUNDO = '#f3f4f6'
COR_TOPO = '#1f2a44'
COR_AZUL = '#3b82f6'
COR_VERDE = '#16a34a'
COR_VERMELHO = '#dc2626'
COR_PAGO = '#9ca3af'

FONTE = ('Segoe UI', 10)


class App:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Gerenciador Financeiro')
        self.janela.geometry('1000x600')
        self.janela.minsize(900, 520)
        self.janela.configure(bg=COR_FUNDO)
        self.contas = carregar_contas()

        self.configurar_estilo()
        self.montar_titulo()
        self.montar_formulario()
        self.montar_paineis()
        self.montar_botoes()
        self.atualizar_tela()

    # ---------- estilo ----------
    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview', font=FONTE, rowheight=26)
        estilo.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        estilo.map('Treeview', background=[('selected', COR_AZUL)],
                   foreground=[('selected', 'white')])

    # ---------- construção da tela ----------
    def montar_titulo(self):
        topo = tk.Frame(self.janela, bg=COR_TOPO)
        topo.pack(fill='x')
        tk.Label(topo, text='Gerenciador Financeiro', bg=COR_TOPO, fg='white',
                 font=('Segoe UI', 16, 'bold')).pack(pady=10)

    def montar_formulario(self):
        painel = tk.LabelFrame(self.janela, text=' Nova conta ', bg=COR_FUNDO,
                               font=FONTE, padx=10, pady=8)
        painel.pack(fill='x', padx=15, pady=(12, 6))

        tk.Label(painel, text='Descrição:', bg=COR_FUNDO, font=FONTE).grid(
            row=0, column=0, padx=5, pady=4, sticky='e')
        self.entry_descricao = ttk.Entry(painel, width=25)
        self.entry_descricao.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(painel, text='Valor:', bg=COR_FUNDO, font=FONTE).grid(
            row=0, column=2, padx=5, pady=4, sticky='e')
        self.entry_valor = ttk.Entry(painel, width=12)
        self.entry_valor.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(painel, text='Vencimento (AAAA/MM/DD):', bg=COR_FUNDO, font=FONTE).grid(
            row=0, column=4, padx=5, pady=4, sticky='e')
        self.entry_vencimento = ttk.Entry(painel, width=12)
        self.entry_vencimento.grid(row=0, column=5, padx=5, pady=4)

        tk.Label(painel, text='Tipo:', bg=COR_FUNDO, font=FONTE).grid(
            row=1, column=0, padx=5, pady=4, sticky='e')
        self.combo_tipo = ttk.Combobox(painel, values=TIPOS, state='readonly', width=22)
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(painel, text='Status:', bg=COR_FUNDO, font=FONTE).grid(
            row=1, column=2, padx=5, pady=4, sticky='e')
        self.combo_status = ttk.Combobox(painel, values=STATUS_OPCOES, state='readonly', width=10)
        self.combo_status.current(0)
        self.combo_status.grid(row=1, column=3, padx=5, pady=4)

        tk.Button(painel, text='Adicionar', font=FONTE, bg=COR_AZUL, fg='white',
                  activebackground='#2563eb', activeforeground='white',
                  relief='flat', padx=14, pady=3,
                  command=self.on_adicionar).grid(row=1, column=5, padx=5, pady=4)

    def criar_tree(self, painel):
        colunas = ('id', 'descricao', 'valor', 'vencimento', 'status')
        nomes = ('ID', 'Descrição', 'Valor', 'Vencimento', 'Status')
        larguras = (35, 120, 70, 85, 70)

        tree = ttk.Treeview(painel, columns=colunas, show='headings', height=10)
        for col, nome, larg in zip(colunas, nomes, larguras):
            tree.heading(col, text=nome)
            tree.column(col, width=larg, anchor='center')

        barra = ttk.Scrollbar(painel, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=barra.set)
        tree.pack(side='left', fill='both', expand=True)
        barra.pack(side='right', fill='y')

        tree.tag_configure('pago', foreground=COR_PAGO)
        return tree

    def montar_paineis(self):
        area = tk.Frame(self.janela, bg=COR_FUNDO)
        area.pack(fill='both', expand=True, padx=15, pady=5)
        area.columnconfigure(0, weight=3)
        area.columnconfigure(1, weight=3)
        area.columnconfigure(2, weight=2, minsize=170)
        area.rowconfigure(0, weight=1)

        painel_rec = tk.LabelFrame(area, text=' Receitas ', bg=COR_FUNDO,
                                   font=FONTE, padx=5, pady=5)
        painel_rec.grid(row=0, column=0, sticky='nsew', padx=5)
        self.tree_receitas = self.criar_tree(painel_rec)

        painel_desp = tk.LabelFrame(area, text=' Despesas ', bg=COR_FUNDO,
                                    font=FONTE, padx=5, pady=5)
        painel_desp.grid(row=0, column=1, sticky='nsew', padx=5)
        self.tree_despesas = self.criar_tree(painel_desp)

        # ao selecionar numa tabela, limpa a seleção da outra
        self.tree_receitas.bind('<<TreeviewSelect>>',
                                lambda e: self.tree_despesas.selection_remove(self.tree_despesas.selection()))
        self.tree_despesas.bind('<<TreeviewSelect>>',
                                lambda e: self.tree_receitas.selection_remove(self.tree_receitas.selection()))

        painel_total = tk.LabelFrame(area, text=' Total ', bg=COR_FUNDO,
                                     font=FONTE, padx=12, pady=10)
        painel_total.grid(row=0, column=2, sticky='nsew', padx=5)

        self.lbl_receitas = tk.Label(painel_total, text='Receitas: R$ 0.00',
                                     bg=COR_FUNDO, fg=COR_VERDE, font=('Segoe UI', 11))
        self.lbl_receitas.pack(anchor='w', pady=6)
        self.lbl_despesas = tk.Label(painel_total, text='Despesas: R$ 0.00',
                                     bg=COR_FUNDO, fg=COR_VERMELHO, font=('Segoe UI', 11))
        self.lbl_despesas.pack(anchor='w', pady=6)
        self.lbl_saldo = tk.Label(painel_total, text='Saldo: R$ 0.00',
                                  bg=COR_FUNDO, font=('Segoe UI', 12, 'bold'))
        self.lbl_saldo.pack(anchor='w', pady=14)

    def montar_botoes(self):
        barra = tk.Frame(self.janela, bg=COR_FUNDO)
        barra.pack(pady=10)
        tk.Button(barra, text='Excluir Selecionada', font=FONTE, bg=COR_VERMELHO,
                  fg='white', activebackground='#b91c1c', activeforeground='white',
                  relief='flat', padx=14, pady=4,
                  command=self.on_excluir).pack(side='left', padx=10)
        tk.Button(barra, text='Marcar Como Pago', font=FONTE, bg=COR_VERDE,
                  fg='white', activebackground='#15803d', activeforeground='white',
                  relief='flat', padx=14, pady=4,
                  command=self.on_marcar_pago).pack(side='left', padx=10)

    # ---------- atualização ----------
    def atualizar_tela(self):
        for tree in (self.tree_receitas, self.tree_despesas):
            tree.delete(*tree.get_children())

        for c in self.contas:
            tree = self.tree_receitas if c['tipo'] == 'Receita' else self.tree_despesas
            tags = ('pago',) if c['status'] == 'Pago' else ()
            tree.insert('', 'end', tags=tags, values=(
                c['id'], c['descricao'], f"{c['valor']:.2f}", c['vencimento'], c['status']))

        rec, desp, saldo = calcular_resumo(self.contas)
        self.lbl_receitas.config(text=f'Receitas: R$ {rec:.2f}')
        self.lbl_despesas.config(text=f'Despesas: R$ {desp:.2f}')
        self.lbl_saldo.config(text=f'Saldo: R$ {saldo:.2f}',
                              fg=COR_VERMELHO if saldo < 0 else COR_VERDE)

    def id_selecionado(self):
        for tree in (self.tree_receitas, self.tree_despesas):
            sel = tree.selection()
            if sel:
                return int(tree.item(sel[0])['values'][0])
        return None

    # ---------- ações dos botões ----------
    def on_adicionar(self):
        descricao = self.entry_descricao.get().strip()
        valor_txt = self.entry_valor.get().strip()
        vencimento = self.entry_vencimento.get().strip()
        tipo = self.combo_tipo.get()
        status = self.combo_status.get()

        if not descricao:
            messagebox.showwarning('Atenção', 'Preencha a descrição.')
            return
        if ';' in descricao:
            messagebox.showwarning('Atenção', "A descrição não pode conter ';'.")
            return

        try:
            valor = float(valor_txt)
        except ValueError:
            messagebox.showerror('Erro', 'Valor inválido. Use ponto como decimal (ex.: 27.50).')
            return
        if valor <= 0:
            messagebox.showwarning('Atenção', 'O valor deve ser maior que zero.')
            return

        try:
            datetime.strptime(vencimento, '%Y/%m/%d')
        except ValueError:
            messagebox.showerror('Erro', 'Data inválida. Use o formato AAAA/MM/DD (ex.: 2026/12/25).')
            return

        adicionar_conta(self.contas, descricao, valor, tipo, vencimento, status)
        salvar_contas(self.contas)
        self.atualizar_tela()

        self.entry_descricao.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        self.entry_vencimento.delete(0, 'end')

    def on_excluir(self):
        id_conta = self.id_selecionado()
        if id_conta is None:
            messagebox.showinfo('Atenção', 'Selecione uma conta na tabela.')
            return
        if messagebox.askyesno('Confirmar', f'Excluir a conta {id_conta}?'):
            excluir_conta(self.contas, id_conta)
            salvar_contas(self.contas)
            self.atualizar_tela()

    def on_marcar_pago(self):
        id_conta = self.id_selecionado()
        if id_conta is None:
            messagebox.showinfo('Atenção', 'Selecione uma conta na tabela.')
            return
        alterar_status(self.contas, id_conta, 'Pago')
        salvar_contas(self.contas)
        self.atualizar_tela()


def iniciar():
    janela = tk.Tk()
    App(janela)
    janela.mainloop()