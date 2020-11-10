import sys
import os
import csv
import socket
from datetime import datetime
from zk import ZK, const
import mysql.connector
from mysql.connector import errorcode

conn = None
escolha = ''
continua = ''
ip = ''
retorno = False
con = None
idcten = ''
idcoletor = ''

config = {
  'host':'10.1.1.175',
  'user':'root',
  'password':'masterkey',
  'database':'gestaoescolar'
}

## FUNÇÕES
# Menu
def selecao():
    print ('\n##O que desejardes fazer?##')
    print ('\n1 - Limpar administradores\n2 - Inserir novo usuário admin (9999 - 123456)\n3 - Listar usuários cadastrados\n4 - Importar CSV com usuários\n5 - Informações do dispositivo\n6 - Deletar usuários\n7 - Reiniciar equipamento\n8 - Formatar equipamento\n9 - Atualizar data e hora\n10 - Listar administradores\n0 - Sair\n')
    
# Limpar admins
def limparadmin():
    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        conn.set_user(uid=user.uid, name=user.name, privilege=const.USER_DEFAULT, password=user.password, group_id=user.group_id, user_id=user.user_id, card=user.card)
        print ('+ UID #{}'.format(user.uid))
        print ('  Privilege  : {}'.format(privilege))

        print ('\nFinalizado!')

# Criar usuário admin
def criaadmin():
    conn.set_user(uid=9999, name='ADMIN PONTO ID', privilege=const.USER_ADMIN, password='123456', group_id='', user_id='9999', card=0)
    print ('\nInserido com sucesso!')

# Listar todos os usuários
def listausu():
    users = conn.get_users()
    for user in users:
        print ('+ UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        else:
            privilege = 'Padrão'
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  User  ID   : {}'.format(user.user_id))

# Importar CSV com usuários
def importacsv():
    with open('usuarios.csv', encoding='utf-8') as csvfile:
        usuarios = csv.DictReader(csvfile, delimiter=';')
        for usuario in usuarios:
            print(usuario)
            uid = usuario["uid"]
            priv = usuario["privilege"].upper()
            if priv == 'USER_DEFAULT':
                conn.set_user(uid=int(uid), name=usuario["name"], privilege=const.USER_DEFAULT, password= usuario["password"], group_id='', user_id=usuario["user_id"], card=0)
            else:
                conn.set_user(uid=int(uid), name=usuario["name"], privilege=const.USER_ADMIN, password= usuario["password"], group_id='', user_id=usuario["user_id"], card=0)
        print('\nUsuários inseridos:\n')
        users = conn.get_users()
        for user in users:
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            else:
                privilege = 'Padrão'
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  User  ID   : {}'.format(user.user_id))

# Informações do dispositivo
def dispositivo():
    print ("-- Device Information --")
    print ("   Current Time            : %s" % conn.get_time())
    print ("   Firmware Version        : %s" % conn.get_firmware_version())
    print ("   Device Name             : %s" % conn.get_device_name())
    print ("   Serial Number           : %s" % conn.get_serialnumber())
    print ("   Mac Address             : %s" % conn.get_mac())
    print ("   Face Algorithm Version  : %s" % conn.get_face_version())
    print ("   Finger Algorithm        : %s" % conn.get_fp_version())
    print ("   Platform Information    : %s" % conn.get_platform())
    #print (conn.get_extend_fmt())
    #print (conn.get_user_extend_fmt())
    #print (conn.get_face_fun_on())
    #print (conn.get_compat_old_firmware())
    network_info = conn.get_network_params()
    print ("-- Network Information")
    print ("   IP                      : %s" % network_info.get('ip'))
    print ("   Netmask                 : %s" % network_info.get('mask'))
    print ("   Gateway                 : %s" % network_info.get('gateway'))
    #print (conn.get_pin_width())
    #print (conn.free_data())
    #print (conn.refresh_data())

def reiniciar():
    print ("Reiniciando Equipamento...")
    conn.restart()

def formatar():
    confirma = input('Tem certeza que deseja formatar o equipamento? [s/n]: ').lower()
    if confirma == 's':
        print ("Formatando...")
        conn.clear_data()
        print ("Formatado!\n")
    else:
        print ("Saindo...")

def datahora():
    print ("Sincronizando data e hora...\n")
    conn.set_time(datetime.now())
    print ("Alterado com sucesso!...\n")

def deletausu():
    confirma = input('Tem certeza que deseja deletar todos os usuários? [s/n]: ').lower()
    if confirma == 's':
        print ("Deletando...\n")
        users = conn.get_users()
        for user in users:
            conn.delete_user(uid=user.uid)
            print ("Usuário deletado!\n") 
    else:
        print ("Saindo...\n")

def listaadmin():
    users = conn.get_users()
    for user in users:
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  User  ID   : {}'.format(user.user_id))

def ping(ip):
    import os, platform

    if  platform.system().lower()=="windows":
        resposta = str(os.system("ping -n 1 " + ip))
        print("OLHA AKI DOIDO: " + resposta)
        if resposta == 0:
            return  True
        else:
            return  False
    else:
        resposta = os.system("ping -c 1 " + ip)
        if resposta == 0:
            return  True
        else:
            return  False

def validaip(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def reiniciaprograma():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def obtemcoletorid():
    try:
        con = mysql.connector.connect(**config)
        print("Conexão com o banco estabelecida")
        print (ip, conn.get_serialnumber())
        cursor = con.cursor()
        cursor.execute("SELECT ID_CCOL FROM cadcol WHERE IP_CCOL = '" + ip + "' AND NUMSERIE_CCOL = '" + conn.get_serialnumber() + "';")
        rows = cursor.fetchone()
        print (rows)

    except e as err:
        print (err)
    finally:
        con.close()

if __name__ == "__main__":

    try:
        
        while True:
            ip = input('IP do equipamento: ')
            ipvalido = validaip(ip)
            if ipvalido == True:
                break

            print ('\nIP incorreto\n')

    except Exception as e:
        print ("Erro: {}".format(e))

    # create ZK instance
    try:
        zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        # connect to device
        conn = zk.connect()

        print ('\n-- Conexão bem sucedida! --')

        print ('\nDesabilitando equipamento...')
        # conn.disable_device()

        while escolha != 0:

            selecao()
            escolha = int(input())

            #Sair
            if escolha == 0:
                break
            # Apagar admins
            elif escolha == 1:
                limparadmin()
            # Criar usuário admin
            elif escolha == 2:
                criaadmin()
            # Listar todos os usuários
            elif escolha == 3:
                listausu()
            # Importar CSV com usuários
            elif escolha == 4:
                importacsv()
            elif escolha == 5:
                dispositivo()
            # Deletar todos os usuários
            elif escolha == 6:
                deletausu()
            # Reiniciar o equipamento
            elif escolha == 7:
                reiniciar()
            # Formatar o equipamento 
            elif escolha == 8:
                print ('Em desenvolvimento...')
            # Atualizar data e hora
            elif escolha == 9:
                datahora()
            # Listar todos os usuários administradores
            elif escolha == 10:
                listaadmin()
            # Enviar matriculas -- Em dev
            elif escolha == 11:
                obtemcoletorid()
                #coletamatriculas()
                # conectarabbit()
                # enviamatriculas()
            else:
                print ('\nOpção inválida!')

    except Exception as e:
        print ("\nErro: {}".format(e))
        input ('\nAperte para continuar...')

    finally:
        if conn:
            print ('Habilitando equipamento...')
            # conn.enable_device()
            input ('\nAperte para sair...')
            print ('Saindo...')
            conn.disconnect() 