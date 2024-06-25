import config.db as db
from config.constants import DB_NAME
from tabulate import tabulate
from datetime import datetime
from services.tools import convert_seconds, convert_tuple_list


class UserAuth:
    def __init__(self, db_name=DB_NAME):
        self.db = db.Database(db_name)

    def login(self, username, password):
        
        stored_password = self.db.get_user(username)
        
        if stored_password and stored_password[0] == password:
            
            print("Acceso autorizado. \n")
            return True
        else:
            
            print("Aceso denegado. \nDebe ingresar un usuario y contraseña válidos.")
            print('\n')
            return False


    def insert_fila_data(self, username, station):
        
        if username in ("recepcion") :
            number = self.db.insert_event(station)
            print("Atencion insertada correctamente. \n")
            
            print(f"Tu numero en la fila es el {number} \n")
        else:
            print("No authorizado.")
    
    
    def get_all(self, username):
        if username in ('atencion'):
            cursor = self.db.get_events(username)
            cursor_shorted = [item[:3] for item in cursor]
            headers = ['Número', 'Fila', 'Ingreso']
            line = tabulate(cursor_shorted, headers=headers, tablefmt='pretty')  
            return line
        else:
            print("No authorizado.")
            
            
    # >>>>>>>>>>>>>>>>>> DEBUGUER  >>>>>>>>>>>>>>>>>>>>>>>
    
    def get_all_posta(self, username):
        if username in ('atencion'):
            cursor = self.db.get_every_event(username)
            return cursor
        else:
            print("No authorizado.")
            
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    
    def get_one(self, username):
        if username in ('atencion'):
            cursor = self.db.get_last_event(username)
            return cursor
        else:
            print("No authorizado.")
    
    
    def attend_one(self, username, id):
        if username in ('atencion'):
            self.db.attend_event(id)

        else:
            print("No authorizado.")
            
    def finish_one(self, username, id):
        if username in ('atencion'):
            self.db.finish_event(id)
        else:
            print("No authorizado.")
            
    def auth_sale(self, username):
        if username in ('atencion'):
            stock = self.db.get_stock()
            if stock == 0:
                return False
            else:
                self.db.sale_product()
                return True
        else:
            print("No authorizado.")
            
    def show_report (self, username):
        if username in ('reportes'):
            
            local_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            finished, not_finished = self.db.get_report(local_now)
            
            finished = convert_tuple_list(finished)
            not_finished = convert_tuple_list(not_finished)
            
            finished_headers = ['numero', 'tiempo_espera', 'tiempo_atencion']
            
            not_finished_headers = ['numero', 'tiempo_espera']
            
            finished_report = tabulate(finished, headers=finished_headers, tablefmt='pretty')

            not_finished_report = tabulate(not_finished, headers=not_finished_headers, tablefmt='pretty')
            
            return finished_report, not_finished_report
    
    def logout(self, username, password):
        return None, None
    
# Example usage:
# auth = UserAuth()
# auth.login("testuser", "securepassword")
# auth.login("testuser", "wrongpassword")