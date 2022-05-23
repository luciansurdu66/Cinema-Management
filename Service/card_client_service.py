import datetime

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.delete_operation import DeleteOperation
from Domain.incrementare_card_operation import IncrementareCardOperation
from Domain.modify_operation import ModifyOperation
from Repository.Exceptii import IncorrectRange, NoSuchIDError, IncorrectData
from Repository.json_repository import JsonRepository
from Service.undo_redo_service import UndoRedoService


class CardClientService:
    def __init__(self, carduri_repository: JsonRepository,
                 card_client_validator: CardClientValidator,
                 undo_redo_service: UndoRedoService):
        self.__carduri_repository = carduri_repository
        self.card_client_validator = card_client_validator
        self.undo_redo_service = undo_redo_service

    def get_all(self):
        """
        Afiseaza lista de carduri
        :return: lista cu carduri
        """
        return self.__carduri_repository.read()

    def create(self, id_card_client,
               nume,
               prenume,
               cnp,
               data_nasterii,
               data_inregistrarii,
               puncte_acumulate):
        """
        Creeaza un card_client
        :param id_card_client: string
        :param nume: string
        :param prenume: string
        :param cnp: string
        :param data_nasterii: string
        :param data_inregistrarii: string
        :param puncte_acumulate: intreg
        :return:
        """
        if self.__carduri_repository.read(cnp):
            raise IncorrectData('Exista deja un card pe acest cnp')
        card_client = CardClient(id_card_client,
                                 nume,
                                 prenume,
                                 cnp,
                                 data_nasterii,
                                 data_inregistrarii,
                                 puncte_acumulate)
        self.card_client_validator.valideaza(card_client)
        self.__carduri_repository.create(card_client)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            AddOperation(self.__carduri_repository, card_client)
        )

    def delete(self, id_card_client):
        """
        Sterge un card_client dupa un id dat
        :param id_card_client: id-ul dat
        :return:
        """
        if self.__carduri_repository.read(id_card_client) is not None:
            card_client = self.__carduri_repository.read(id_card_client)
        self.__carduri_repository.delete(id_card_client)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            DeleteOperation(self.__carduri_repository, card_client)
        )

    def update(self, id_card_client,
               nume,
               prenume,
               cnp,
               data_nasterii,
               data_inregistrarii,
               puncte_acumulate):
        """
        Modifica un card_client
        :param id_card_client: string
        :param nume: string
        :param prenume: string
        :param cnp: string
        :param data_nasterii:
        :param data_inregistrarii:
        :param puncte_acumulate: numar intre
        :return:
        """
        card_client_vechi = self.__carduri_repository.read(id_card_client)
        if card_client_vechi is None:
            raise NoSuchIDError(f'Nu exista un card cu id-ul {id_card_client}')

        card_client = CardClient(id_card_client, nume, prenume, cnp,
                                 data_nasterii, data_inregistrarii,
                                 puncte_acumulate)
        if nume != "":
            card_client.nume = nume
        if prenume != "":
            card_client.prenume = prenume
        if cnp != "":
            card_client.cnp = cnp
        if data_nasterii != "":
            card_client.data_nasterii = data_nasterii
        if data_inregistrarii != "":
            card_client.data_inregistrarii = data_inregistrarii
        if puncte_acumulate >= 0:
            card_client.puncte_acumulate = puncte_acumulate

        self.card_client_validator.valideaza(card_client)
        self.__carduri_repository.update(card_client)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            ModifyOperation(self.__carduri_repository,
                            card_client_vechi,
                            card_client)
        )

    def get_data(self, card):
        data_si_ora = card.data_nasterii
        data = data_si_ora.split(" ")[0]
        data_components = data.split('.')
        data = datetime.datetime(int(data_components[2]),
                                 int(data_components[1]),
                                 int(data_components[0]))
        return data

    def incrementare_valoare(self, valoare, data1, data2):
        if data2 < data1:
            raise IncorrectRange('Data2 trebuie sa fie mai mare decat data1!')
        if valoare <= 0:
            raise ValueError('Valoarea trebuie sa fie pozitiva!')
        carduri_modificate = []
        lista_carduri = self.get_all()
        lista_finala = list(card for card in lista_carduri if
                            self.get_data(card) < data1 or
                            self.get_data(card) > data2)
        for card in lista_carduri:
            if card not in lista_finala:
                carduri_modificate.append(card)
                card_modificat = CardClient(card.id_entitate, card.nume,
                                            card.prenume,
                                            card.cnp, card.data_nasterii,
                                            card.data_inregistrarii,
                                            card.puncte_acumulate + valoare)
                self.__carduri_repository.update(card_modificat)
        lista_noua = self.__carduri_repository.read()
        self.undo_redo_service.clear_redo()
        modificate = IncrementareCardOperation(self.__carduri_repository,
                                               lista_carduri, lista_noua)
        self.undo_redo_service.add_undo_operation(modificate)
