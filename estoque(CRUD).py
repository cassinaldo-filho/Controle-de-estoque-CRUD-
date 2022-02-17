import mysql.connector

from tkinter import *

from tkinter import messagebox

from tkinter import ttk

conexao = mysql.connector.connect(host='localhost', database='estoque_loja', user='root', password='25no1999')

novo_user = 'Y'
nova_senha = 'Y'
campo_usuario_cadastrado = 'Y'
checar_usuario = 'y'
campo_senha_alterada = 'Y'
adcionar_nome = 'y'
adcionar_quant = 0
adcionar_preco = 0.0
logado = 0
janela_cadastro = 0
janela_estoque = 0
tabela_estoque = 0
valores = 0
janela_modificar = 0
janela_adcionar = 0
if conexao.is_connected():
    print(f"\nConexão bem sucedida ao Mysql")
    cursor = conexao.cursor()


def esqueci():
    global campo_usuario_cadastrado
    global campo_senha_alterada

    janela_esqueci = Toplevel()
    janela_esqueci.geometry('460x221')
    janela_esqueci.minsize(460, 221)
    janela_esqueci.maxsize(460, 221)
    janela_esqueci.title('Esqueci minha senha')

    janela_esqueci.grab_set()

    titulo_usuario = Label(janela_esqueci, text='   Informe o nome de usuário atual e a nova senha ')
    titulo_usuario.grid(column=1, row=0, pady=10)

    usuario_cadastrado = Label(janela_esqueci, text='Usuário atual:')
    usuario_cadastrado.grid(column=0, row=1, padx=10, pady=20)

    campo_usuario_cadastrado = Entry(janela_esqueci, justify=CENTER)
    campo_usuario_cadastrado.grid(column=1, row=1)

    campo_usuario_cadastrado.focus_set()

    texto_senha_alterada = Label(janela_esqueci, text='Nova senha:')
    texto_senha_alterada.grid(column=0, row=2, padx=10, pady=10)

    campo_senha_alterada = Entry(janela_esqueci, justify=CENTER, show='*')
    campo_senha_alterada.grid(column=1, row=2)

    botao_continuar = Button(janela_esqueci, text=' Continuar ', command=lambda: continuar())
    botao_continuar.grid(column=1, row=3, pady=20)

    janela_esqueci.mainloop()


def continuar():

    global checar_usuario
    negativo = 1
    checar_usuario = campo_usuario_cadastrado.get()

    if checar_usuario == '' or campo_senha_alterada.get() == '':
        messagebox.showerror(title='Aviso', message='Todos os campos devem está preenchidos.')
    else:


        com_continuar = f'select usuario from login'
        cursor.execute(com_continuar)
        result_usuario = cursor.fetchall()

        for cont in range(len(result_usuario)):
            for cont2 in range(0, 1):
                if checar_usuario == result_usuario[cont][cont2]:
                    mudar_senha(checar_usuario)
                    negativo = 0
                    messagebox.showinfo(title='Aviso', message='Senha alterada com sucesso!')
        if negativo == 1:
            messagebox.showerror(title='Aviso', message='O nome de usuário não existe.')


def mudar_senha(x):
    senha_alterada = campo_senha_alterada.get()

    com_mudar_senha = f'update login set senha = "{senha_alterada}" where usuario = "{x}";'
    cursor.execute(com_mudar_senha)
    conexao.commit()


def cadastro():
    global novo_user
    global nova_senha
    global janela_cadastro

    janela_cadastro = Toplevel()
    janela_cadastro.geometry('340x150')
    janela_cadastro.minsize(340, 150)
    janela_cadastro.maxsize(340, 150)

    janela_cadastro.title('Cadastro de usuário')
    janela_cadastro.grab_set()

    texto_novo_user = Label(janela_cadastro, text='Novo usuário:')
    texto_novo_user.grid(column=0, row=0, padx=10, pady=10)

    novo_user = Entry(janela_cadastro, justify=CENTER)
    novo_user.grid(column=1, row=0, padx=10, pady=10)
    novo_user.focus_set()

    texto_novo_senha = Label(janela_cadastro, text='Nova senha:')
    texto_novo_senha.grid(column=0, row=1, padx=0, pady=10)

    nova_senha = Entry(janela_cadastro, justify=CENTER, show='*')
    nova_senha.grid(column=1, row=1, padx=10, pady=10)

    botao_cadastrar = Button(janela_cadastro, text=' Cadastrar ', command=lambda: faz_cadastro())
    botao_cadastrar.grid(column=1, row=2, pady=10)
    janela.mainloop()


def faz_cadastro():
    new_user = novo_user.get()

    new_senha = nova_senha.get()

    if new_user == '' or new_senha == '':
        messagebox.showerror(title='Aviso', message='Todos os campos devem está preenchidos.')

    else:

        tudocerto = 0
        quebrafor = 0

        com_checar = f"select usuario from login;"
        cursor.execute(com_checar)
        checkk = cursor.fetchall()

        for cont in range(len(checkk)):

            for cont2 in range(0, 1):

                if new_user == checkk[cont][cont2]:
                    messagebox.showerror(title='Aviso', message='Esse nome já está em uso . Tente outro.')

                    nova_senha.delete(0, END)

                    tudocerto = 1
                    quebrafor = 1

            if quebrafor == 1:
                break

        if tudocerto == 0:
            com_cadastrar = f"""insert into login (usuario,senha) 
            value ('{new_user}','{new_senha}' );"""
            cursor.execute(com_cadastrar)
            conexao.commit()
            novo_user.delete(0, END)
            nova_senha.delete(0, END)
            messagebox.showinfo(title='Aviso', message='Cadastro realizado com sucesso!')
            janela_cadastro.destroy()


def login():
    loginsucesso = 0

    use = input_user.get()

    senha = input_senha.get()

    if use == '' or senha == '':
        messagebox.showerror(title='Aviso', message='Todos os campos devem está preenchidos.')
        loginsucesso=2
    else:


        com_checklogin = f'select usuario,senha from login;'
        cursor.execute(com_checklogin)
        result_checklogin = cursor.fetchall()

        

        for cont in range(len(result_checklogin)):

            for cont2 in range(0, 1):

                for cont3 in range(1, 2):

                    if use == result_checklogin[cont][cont2] and senha == result_checklogin[cont][cont3]:
                        messagebox.showinfo(title='Aviso', message='Login realizado com sucesso!')
                        loginsucesso = 1
                        input_user.delete(0, END)
                        input_senha.delete(0, END)

                        acessar_estoque()

    if loginsucesso == 0:
        input_senha.delete(0, END)
        messagebox.showerror(title='Aviso', message='Usuário ou senha inválidos.')


def acessar_estoque():
    global janela_estoque
    global tabela_estoque
    janela_estoque = Toplevel()
    janela_estoque.geometry('600x300')
    janela_estoque.minsize(600, 300)
    janela_estoque.maxsize(600, 300)
    janela_estoque.title('Estoque de loja')

    janela_estoque.grab_set()

    com_carregar_estoque = 'select * from estoque'
    cursor.execute(com_carregar_estoque)
    result_estoque = cursor.fetchall()
    tabela_estoque = ttk.Treeview(janela_estoque, columns=('Código', 'Nome do produto', 'Quantidade', 'Preço'),
                                  show='headings')
    tabela_estoque.column('Código', minwidth=30, width=140, anchor="center")
    tabela_estoque.column('Nome do produto', minwidth=40, width=140, anchor="center")
    tabela_estoque.column('Quantidade', minwidth=30, width=140, anchor="center")
    tabela_estoque.column('Preço', minwidth=30, width=140, anchor="center")
    tabela_estoque.heading('Código', text='Código')
    tabela_estoque.heading('Nome do produto', text='Nome do produto')
    tabela_estoque.heading('Quantidade', text='Unidades')
    tabela_estoque.heading('Preço', text='Preço / R$')
    tabela_estoque.grid(column=0, row=0, padx=10, pady=10)
    for cod in result_estoque:
        tabela_estoque.insert('', 'end', values=(f'{cod[0]}', f'{cod[1]}', f'{cod[2]}', f'%.2f'% (cod[3])))

    botao_adcionar = Button(janela_estoque, text='Adcionar',
                            command=lambda: [janela_estoque.grab_release(), adcionar()])
    botao_adcionar.grid(column=0, row=1, stick='w', padx=10, pady=5)

    botao_modificar = Button(janela_estoque, text=' Modificar ',
                             command=lambda: [janela_estoque.grab_release(), modificar()])
    botao_modificar.grid(column=0, row=1, pady=5, )

    botao_deletar = Button(janela_estoque, text=' Deletar ',
                           command=lambda: [deletar(), janela_estoque.destroy(), acessar_estoque()])
    botao_deletar.grid(column=0, row=1, stick='e', padx=10, pady=5)

    janela_estoque.mainloop()


def adcionar():
    global adcionar_nome
    global adcionar_quant
    global adcionar_preco
    global janela_adcionar
    largura = 885
    altura = 60

    janela_adcionar = Toplevel()
    largura_screen = janela_adcionar.winfo_screenwidth()
    altura_screen = janela_adcionar.winfo_screenheight()

    posx = largura_screen / 2 - largura / 2
    posy = altura_screen / 2 - altura / 2

    janela_adcionar.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

    janela_adcionar.overrideredirect(True)

    janela_adcionar.title('Adcionar produto')

    janela_adcionar.grab_set()

    nome = Label(janela_adcionar, text='Nome do Produto : ')
    nome.grid(column=0, row=0, padx=10, pady=20)

    adcionar_nome = Entry(janela_adcionar, justify=CENTER)
    adcionar_nome.grid(column=1, row=0, padx=10, pady=20)
    adcionar_nome.focus_set()

    quant = Label(janela_adcionar, text='Unidade : ')
    quant.grid(column=2, row=0, padx=10, pady=20)

    adcionar_quant = Entry(janela_adcionar, justify=CENTER)
    adcionar_quant.grid(column=3, row=0, padx=10, pady=10)

    preco = Label(janela_adcionar, text='Preço : ')
    preco.grid(column=4, row=0, padx=10, pady=20)

    adcionar_preco = Entry(janela_adcionar, justify=CENTER)
    adcionar_preco.grid(column=5, row=0, stick='e', padx=15, pady=20)

    botao_adcionar = Button(janela_adcionar, text=' Aplicar ', command=lambda: novo_produto())
    botao_adcionar.grid(column=6, row=0, padx=15)

    botao_fechar = Button(janela_adcionar, text=' Fechar ',
                          command=lambda: [janela_adcionar.destroy(), janela_estoque.destroy(), acessar_estoque()])
    botao_fechar.grid(column=7, row=0, padx=15)


def modificar():
    try:

        global adcionar_nome
        global adcionar_quant
        global adcionar_preco
        global valores
        global janela_modificar
        item_selecionado = tabela_estoque.selection()[0]
        valores = tabela_estoque.item(item_selecionado, 'values')

        largura = 885
        altura = 60

        janela_modificar = Toplevel()
        largura_screen = janela_modificar.winfo_screenwidth()
        altura_screen = janela_modificar.winfo_screenheight()

        posx = largura_screen / 2 - largura / 2
        posy = altura_screen / 2 - altura / 2

        janela_modificar.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

        janela_modificar.overrideredirect(True)

        janela_modificar.grab_set()

        nome = Label(janela_modificar, text='Nome do Produto : ')
        nome.grid(column=0, row=0, padx=10, pady=20)

        adcionar_nome = Entry(janela_modificar, justify=CENTER)
        adcionar_nome.grid(column=1, row=0, padx=10, pady=20)
        adcionar_nome.focus_set()

        quant = Label(janela_modificar, text='Unidade : ')
        quant.grid(column=2, row=0, padx=10, pady=20)

        adcionar_quant = Entry(janela_modificar, justify=CENTER)
        adcionar_quant.grid(column=3, row=0, padx=10, pady=10)

        preco = Label(janela_modificar, text='Preço : ')
        preco.grid(column=4, row=0, padx=10, pady=20)

        adcionar_preco = Entry(janela_modificar, justify=CENTER)
        adcionar_preco.grid(column=5, row=0, stick='e', padx=15, pady=20)

        adcionar_nome.insert(0, valores[1])
        adcionar_quant.insert(0, valores[2])
        adcionar_preco.insert(0, valores[3])

        botao_adcionar = Button(janela_modificar, text=' Aplicar ',
                                command=lambda: [atualizar_prod(), janela_modificar.destroy(), janela_estoque.destroy(),
                                                 acessar_estoque()])
        botao_adcionar.grid(column=6, row=0, padx=15)

        botao_fechar = Button(janela_modificar, text=' Fechar ',
                              command=lambda: [janela_modificar.destroy(), janela_estoque.destroy(), acessar_estoque()])
        botao_fechar.grid(column=7, row=0, padx=15)


    except:
        messagebox.showerror(title='Aviso', message='Por favor selecione um item.')
        janela_estoque.grab_set()


def deletar():
    try:

        item_selecionado = tabela_estoque.selection()[0]
        valores2 = tabela_estoque.item(item_selecionado, 'values')

       

        comando_deletar = f'delete from estoque where codigo = "{valores2[0]}";'
        cursor.execute(comando_deletar)
        conexao.commit()


    except:
        messagebox.showerror(title='Aviso', message='Por favor selecione um item.')


def atualizar_prod():
    vprod = adcionar_nome.get()
    vquant = adcionar_quant.get()
    vpreco = adcionar_preco.get()

    if vprod == '' or vquant == '' or vpreco == '':
        messagebox.showerror(title='Aviso', message='Todos os campos devem está preenchidos.')

    else:
        try:
            comando_atualizar_prod = f'update estoque set produto ="{vprod}", quantidade = {vquant}, preco = {vpreco}  where codigo ="{valores[0]}";'
            cursor.execute(comando_atualizar_prod)
            conexao.commit()
        except:
            messagebox.showerror(title='Aviso',
                                 message='{:^70}''\n\n Nome / número inteiro / número real com ponto "." ex: (2.35)'.format(
                                     'Formato inválido. Use o formato padrão abaixo: '))


def atualizar_tabela():
    global janela_modificar
    global janela_adcionar
    global janela_estoque

    janela_estoque.destroy()
    janela_modificar.destroy()
    janela_adcionar.destroy()
    acessar_estoque()


def novo_produto():
    novo_nome = adcionar_nome.get()
    novo_quant = adcionar_quant.get()
    novo_preco = adcionar_preco.get()
    

    if novo_nome == '' or novo_quant == '' or novo_preco == '':
        messagebox.showerror(title='Aviso', message='Todos os campos devem está preenchidos.')
    else:
        try:
            tudocerto = 0
            quebrafor = 0

            com_checar = f"select * from estoque;"
            cursor.execute(com_checar)
            checkk = cursor.fetchall()

            for cont in range(len(checkk)):

                for cont2 in range(1, 4):

                    if novo_nome == checkk[cont][cont2]:
                        messagebox.showerror(title='Aviso', message='Esse produto já está cadastrado. Tente outro.')
                        adcionar_nome.delete(0, END)
                        adcionar_quant.delete(0, END)
                        adcionar_preco.delete(0, END)
                        tudocerto = 1
                        quebrafor = 1

                if quebrafor == 1:
                    break

            if tudocerto == 0:
                com_adcionar_novoproduto = f'''insert into estoque (produto,quantidade,preco) values("{novo_nome}",{novo_quant},{novo_preco})'''
                cursor.execute(com_adcionar_novoproduto)
                conexao.commit()

                messagebox.showinfo(title='Aviso', message='Cadastro realizado com sucesso!')
                adcionar_nome.delete(0, END)
                adcionar_quant.delete(0, END)
                adcionar_preco.delete(0, END)
        except:
            messagebox.showerror(title='Aviso',
                                 message='{:^70}''\n\n Nome / número inteiro / número real com ponto "." ex: (2.35)'.format(
                                     'Formato inválido. Use o formato padrão abaixo: '))


janela = Tk()
# janela['bg']='#87CEFA'  -  muda para a Cor azul

janela.geometry('536x231')
janela.minsize(536, 231)
janela.maxsize(536, 231)
janela.title('Login de acesso')

textologin = Label(janela, text='Login de acesso')
textologin.grid(column=1, row=0, pady='10')

texto_user = Label(janela, text='Usuário:')
texto_user.grid(column=0, row=1, padx=5, pady=30)

input_user = Entry(janela, justify=CENTER)
input_user.grid(column=1, row=1, padx=50, pady=0)

input_user.focus_set()

texto_senha = Label(janela, text='Senha: ', justify=CENTER)
texto_senha.grid(column=0, row=2, padx=5, pady=10)

input_senha = Entry(janela, justify=CENTER, show='*')
input_senha.grid(column=1, row=2, padx=100, pady=10)

botao = Button(janela, text='    Entrar    ', command=lambda: login())
botao.grid(column=1, row=3, pady='20')

botao_esqueci = Button(janela, text=' Esqueci minha senha ', command=lambda: esqueci())
botao_esqueci.grid(column=2, row=2, pady=0, padx=10)

botao_cadastro = Button(janela, text=' Cadastre-se ', command=lambda: cadastro())
botao_cadastro.grid(column=2, row=3, pady=20, padx=10)

janela.mainloop()
