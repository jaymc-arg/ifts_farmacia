from services.auth import UserAuth
from config.db import Database
from services.tools import create_receipt

def main():
    auth = UserAuth()
    username = None
    password = None
    # Database.start_up()
    while True: 
        while not username:
            
            if not username or not password:
                
                username = input("Ingrese su nombre de usuario: ")
                print('\n')
                    
                password = input("Ingrese su contraseña: ")
                print('\n')
                
                if auth.login(username, password):
                    pass
                else:
                    username = None
                    password = None
                    
        while username =='recepcion':
            try:
                print(' 1) Atencion\n 2) Salir \n')
                
                event = input('¿A qué puesto quiere derivar a la persona? ')
                
                if event not in ('1', '2'):
                    raise ValueError('Debe ingresar opcion 1 o 2 \n')
                
                if event == '1':
                    
                    auth.insert_fila_data(username, 'atencion')
                
                if event == '2':
                    
                    username, password = auth.logout(username, password)
                    print('\n Nos vemos pronto! \n')
                    break
                
            except ValueError as e:
                print(e)
                
        while username == 'atencion':
            try: 
                event = input(
                    """¿Que desea realizar? \n 1) Lamar al siguiente \n 2) Ver toda la fila \n 3) Salir \n """
                )
                if event not in ('1', '2', '3'):
                    # print('>>>>>>>>>>>',event)
                    raise ValueError('\nDebe ingresar opcion 1, 2 o 3 \n')
                
                if event == '1':
                    next = auth.get_one(username)
                    
                    # Valido que haya alguien en la fila
                    if next:
                        id_next = next[0]
                        auth.attend_one(username, id_next)
                        
                        # >>>>>>> control
                        # line = auth.get_all_posta(username)
                        # print(line)
                        # print(id_next)
                        # >>>>>>>>>>>>
                        
                        try:
                            desicion = input( 
                            """¿Que desea realizar? \n1) Cobrar \n2) Finalizar atencion \n""")
                            if desicion not in ('1', '2'):
                                raise ValueError('Debe ingresar opcion 1, 2 \n')
                            
                            if desicion == '1':
                                
                                auth.finish_one(username, id_next)
                                
                                if auth.auth_sale(username):
                                    recipit = create_receipt(id_next)
                                    print(recipit)
                                else:
                                    print("No tenemos mas productos en Stock.")
                            
                            if desicion == '2':
                                auth.finish_one(username, id_next)
                                
                        except ValueError as e:
                            print(e)
                    else:
                        print('\nLa fila esta vacia.')
                                    
                if event == '2':
                    waiting_line = auth.get_all(username)
                    print(waiting_line)
                    
                if event == '3':
                    username, password = auth.logout(username, password)
                    print('\n Nos vemos pronto')
                    break
                
            except ValueError as e:
                
                print(e)
            
        while username == 'reportes':
            try:
                print(' 1) Ver reporte de atenciones finalizadas \n 2) Ver reporte de atenciones sin finalizar \n 3) Salir')
                
                event = input('¿Qué acción desea realizar?')
                
                if event not in('1', '2'):
                    raise ValueError('Debe ingresar opcion 1 o 2 \n')    
                
                if event == '1':
                    finished_report, _ = auth.show_report(username)
                    print(finished_report)
                    
                if event == '2':
                    _, finished_report = auth.show_report(username)
                    print(finished_report)

                if event == '3':
                    
                    username, password = auth.logout(username, password)
                    print('\n Nos vemos pronto')
                    break
            
            except ValueError as e:
                print(e)
            
if __name__ == "__main__":
    main()
