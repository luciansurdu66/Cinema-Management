from datetime import datetime


class RezervareValidator:
    def valideaza(self, rezervare) -> None:
        try:
            datetime.strptime(rezervare.data_ora, '%d.%m.%Y %H:%M')
        except ValueError:
            raise ValueError("Formatul datei trebuie sa fie: DD.MM.YYYY H:M")
