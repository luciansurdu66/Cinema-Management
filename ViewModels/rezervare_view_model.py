from Domain.card_client import CardClient
from Domain.film import Film


class RezervareViewModel:
    def __init__(self, id_rezervare,
                 film: Film,
                 card_client: CardClient,
                 data_ora):
        self.id_rezervare = id_rezervare
        self.film = film
        self.card_client = card_client
        self.data_ora = data_ora

    def __str__(self):
        return f'id rezervare:{self.id_rezervare}' \
               f' cu film {self.film},' \
               f' card client {self.card_client}, ' \
               f' data_ora: {self.data_ora}'
