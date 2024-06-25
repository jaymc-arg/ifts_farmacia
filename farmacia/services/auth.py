import config.db as db
from config.constants import DB_NAME
from tabulate import tabulate
from datetime import datetime
from services.tools import convert_seconds, convert_tuple_list


class UserAuth:
    def __init__(self, db_name=DB_NAME):
        self.db = db.Database(db_name)

    def login(self, username, password):  # recibe usuario y contraseña desde main
        
        stored_password = self.db.get_user(username) # busca al usuario en la base
        
        if stored_password and stored_password[0] == password: # valida que la pass guardada y la ingresada sean iguales
            
            print("Acceso autorizado. \n")
            return True # da acceso a la app
        else:
            
            print("Aceso denegado. \nDebe ingresar un usuario y contraseña válidos.")
            print('\n')
            return False


    def insert_fila_data(self, username, station): # recibe usuario para validar y fila a la que ingresar a la persona
        
        if username in ("recepcion") : # valida permiso de usuario
            
            number = self.db.insert_event(station) # recibe fila en la que insertar persona y retorna numero de atencion de la persona
            print("Atencion insertada correctamente. \n")
            
            #print(f"Tu numero en la fila es el {number} \n") # imprime el numero en la fila de la persona
            return number
        else:
            print("No autorizado.")
    
    
    def get_all(self, username): 
        if username in ('atencion'):
            cursor = self.db.get_events(username) # busca en bbdd
            cursor_shorted = [item[:3] for item in cursor] # se queda con los 3 primeros valores de cada registro (id, fila, created_at)
            headers = ['Número', 'Fila', 'Ingreso'] # headers de tabla para pretty print
            line = tabulate(cursor_shorted, headers=headers, tablefmt='pretty')  # genera tabla de fila de espera
            return line
        else:
            print("No autorizado.")
            
            
    # >>>>>>>>>>>>>>>>>> DEBUGUER  >>>>>>>>>>>>>>>>>>>>>>>
    
    def get_all_posta(self, username):
        if username in ('atencion'):
            cursor = self.db.get_every_event(username)
            return cursor
        else:
            print("No autorizado.")
            
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    
    def get_one(self, username):
        if username in ('atencion'):
            cursor = self.db.get_last_event(username)
            return cursor
        else:
            print("No autorizado.")
    
    
    def attend_one(self, username, id):
        if username in ('atencion'):
            self.db.attend_event(id)

        else:
            print("No autorizado.")
            
    def finish_one(self, username, id):
        if username in ('atencion'):
            self.db.finish_event(id)
        else:
            print("No autorizado.")
            
    def auth_sale(self, username):
        if username in ('atencion'):
            stock = self.db.get_stock() # devuelve el stock de remedios
            if stock == 0:
                return False # cancela la venta si el stock es == 0
            else: # si el stock es > 0
                self.db.sale_product() # vende el producto
                return True
        else:
            print("No autorizado.")
            
    def show_report (self, username):
        if username in ('reportes'): # valida usuario reportes
            
            local_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # hora local del momento para restar con creacion y asi

            finished, not_finished = self.db.get_report(local_now) # devuelve dos reportes = finalizado y no finalizado
            
            finished = convert_tuple_list(finished) # recorta la tupla de finalizados para dejar solo los campos que usamos 
            not_finished = convert_tuple_list(not_finished) # recorta la tupla de no finalizados para dejar solo los campos que usamos 
            
            finished_headers = ['numero', 'tiempo_espera', 'tiempo_atencion'] # encabezados
            
            not_finished_headers = ['numero', 'tiempo_espera']
            
            finished_report = tabulate(finished, headers=finished_headers, tablefmt='pretty') # convierte la tupla a tabla linda

            not_finished_report = tabulate(not_finished, headers=not_finished_headers, tablefmt='pretty') # convierte la tupla a tabla linda
            
            return finished_report, not_finished_report 
    
    def logout(self, username, password):
        return None, None
    
# Example usage:
# auth = UserAuth()
# auth.login("testuser", "securepassword")
# auth.login("testuser", "wrongpassword")