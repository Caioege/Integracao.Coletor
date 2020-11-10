import sys
import os
from zk import ZK, const

    # Menu
    def selecao():
        print ('##O que desejardes fazer?##')
        print ('\n1 - Limpar administradores\n2 - Inserir novo usuário admin (9999 - 123456)\n3 - Listar usuários cadastrados\n4 - Importar CSV com usuários\n')

    def sair():
        conn.disconnect()
        print ('Saindo...')
        
    # Limpar admins
    def limparadmin():
        users = conn.get_users()
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            conn.set_user(uid=user.uid, privilege=const.USER_DEFAULT,)
            print ('+ UID #{}'.format(user.uid))
            print ('  Privilege  : {}'.format(privilege))

            print ('\nFinalizado!')

    # Criar usuário admin
    def criaadmin():
        conn.set_user(uid=9999, name='ADMIN PONTO ID', privilege=const.USER_ADMIN, password='123456', group_id='', user_id='9999', card=0)
        print ('\nInserido com sucesso!')
        conn.get_user(uid=9999)

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
                priv = usuario["privilege"]
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

    