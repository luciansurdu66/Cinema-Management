from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Rezervare(Entitate):
    id_film: str
    id_card_client: str
    data_ora: str
