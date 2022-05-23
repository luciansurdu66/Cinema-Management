from datetime import datetime

from Domain.card_client import CardClient
from Repository.Exceptii import IncorrectData


class CardClientValidatorError(Exception):
    pass


class CardClientValidator:
    def valideaza(self, card_client: CardClient) -> None:

        try:
            datetime.strptime(card_client.data_nasterii, '%d.%m.%Y')
            datetime.strptime(card_client.data_inregistrarii, '%d.%m.%Y')
        except IncorrectData as ID:
            print(ID)
