
import gspread
import json

#result = worksheet.get_all_records()
#result = worksheet.get_all_values()
#result = worksheet.col_values(1)
#result = worksheet.row_values(1)
#result = worksheet.get('A1:C2')

headers = ["Pilote", "Appareil", "Date", "Heure"]
new_entrie = ["Goose", "F-18", "20/21/2020", "15h35"]

#worksheet.insert_row(headers, 1)
#worksheet.append_row(new_entrie)
#worksheet.update_cell(3, 4, "17h00")
#worksheet.delete_rows(1)

class Planning():
    gc = gspread.service_account(filename="libaile/credentials.json")
    sh = gc.open_by_key('1wRZ-Ri5o1P5XDUI6lAOfeHsEBSUZv3PgdwOsllM9j5w')
    worksheet = sh.get_worksheet(0)

    def avion(self):
        avions = self.worksheet.get_all_records()
        return avions

    def add_avion(self, pilote, appareil, date, heure ):
        new_entrie = [pilote, appareil, date, heure]
        self.worksheet.append_row(new_entrie)

    def del_avion(self, _id):
        self.worksheet.delete_rows(_id + 1)