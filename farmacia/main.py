from services.auth import UserAuth
from config.db import Database
from services.tools import create_receipt, create_call_sign, create_ticket

def main():
    auth = UserAuth() # instancio objeto que autoriza cada accion de los usuarios
    username = None
    password = None
    # Database.start_up()
    while True: 
        print("Bienvenido a Farmacia 3000")
        while not username: # se ejecuta siempre que no haya alguien logueado
            
            if not username or not password: # si no hay nadie logueado continua
                
                username = input("Ingrese su nombre de usuario: ")
                print('\n')
                    
                password = input("Ingrese su contraseña: ")
                print('\n')
                
                if auth.login(username, password): #ejecuta login de lo ingresado por el usuario y devuelve True si es exitoso
                    pass
                else:
                    username = None # resetea variable para que se ejeute while externo (linea 11)
                    password = None
                    
        while username =='recepcion': # si se loguea usuario recepcion
            try:
                print(' 1) Atencion\n 2) Salir \n')
                
                event = input('¿A qué puesto quiere derivar a la persona? ')
                
                if event not in ('1', '2'): # control de errores de ingreso
                    raise ValueError('Debe ingresar opcion 1 o 2 \n')
                
                if event == '1': # ingresar una persona en la fila 'atencion'
                    
                    number_in_line = auth.insert_fila_data(username, 'atencion') # funcion que valida permiso para ingresar persona en fila
                    ticket = create_ticket(number_in_line)
                    print(ticket)
                if event == '2': # logout
                    
                    username, password = auth.logout(username, password) # recibe usuario y contraseña y los setea a None para volver a linea 11
                    print('\n Nos vemos pronto! \n')
                    break
                
            except ValueError as e: #catch de error de ingreso de opciones
                print(e)
                
        while username == 'atencion':
            try: 
                event = input(
                    """¿Que desea realizar? \n 1) Llamar al siguiente \n 2) Ver toda la fila \n 3) Salir \n """
                )
                if event not in ('1', '2', '3'):
                    raise ValueError('\nDebe ingresar opcion 1, 2 o 3 \n')
                
                if event == '1': # llamo al siguiente en la fila
                    next = auth.get_one(username) # me quedo con el registro comleto del proximo en la fila
                    
                    if next: # valido que haya alguien en la fila, si es None se va por el else
                        id_next = next[0] # me quedo con el numero del proximo en la fila
                        auth.attend_one(username, id_next)
                        
                        sign = create_call_sign(id_next) # creo cartel que llama al siguiente por pantalla
                        print(sign)
                        # >>>>>>> control
                        # line = auth.get_all_posta(username)
                        # print(line)
                        # print(id_next)
                        # >>>>>>>>>>>>
                        
                        desicion = None
                        while not desicion:
                            try:
                                desicion = input( 
                                """\n¿Que desea realizar? \n1) Cobrar \n2) Finalizar atencion \n""")
                                if desicion not in ('1', '2'):
                                    raise ValueError('Debe ingresar opcion 1, 2 \n')
                                
                                if desicion == '1': # decide cobrar
                                    
                                    if auth.auth_sale(username): # valida que haya stock y devuelve True en caso positivo
                                        recipit = create_receipt(id_next) # crea print del recibo de venta
                                        print(recipit)
                                    else:
                                        print("No tenemos mas productos en Stock.")
                                
                                    auth.finish_one(username, id_next) # termina la atencion
                                    
                                if desicion == '2': # finaliza sin cobrar porque por alguna razon el cliente no compro
                                    auth.finish_one(username, id_next)
                                
                            except ValueError as e: # catch error de ingreso
                                print(e)
                                desicion = None
                    else: # no hay nadie en la fila
                        print('\nLa fila esta vacia. \n')
                                    
                if event == '2': # muestra a todos en la fila de atencion
                    waiting_line = auth.get_all(username) # busca todos en la fila que NO estan atendidos
                    print(waiting_line)
                    
                if event == '3': # logout
                    username, password = auth.logout(username, password)
                    print('\n Nos vemos pronto')
                    break
                
            except ValueError as e:
                
                print(e)
            
        while username == 'reportes': #usuario reportes
            try:
                print(' 1) Ver reporte de atenciones finalizadas \n 2) Ver reporte de atenciones sin finalizar \n 3) Salir')
                
                event = input('¿Qué acción desea realizar?')
                
                if event not in('1', '2', '3'):
                    raise ValueError('Debe ingresar opcion 1, 2 o 3 \n')    
                
                if event == '1': # atenciones finalizadas
                    finished_report, _ = auth.show_report(username)
                    print(finished_report)
                    
                if event == '2': # atenciones en curso
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
