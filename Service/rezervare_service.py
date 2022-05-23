import datetime

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Domain.stergere_entitati_operation import StergereEntitatiOperation
from Repository.Exceptii import NoSuchIDError, IncorrectRange
from Repository.json_repository import JsonRepository
from Service.undo_redo_service import UndoRedoService


class RezervareService:
    def __init__(self, rezervare_repository: JsonRepository,
                 rezervare_validator: RezervareValidator,
                 filme_repository: JsonRepository,
                 carduri_repository: JsonRepository,
                 undo_redo_service: UndoRedoService):
        self.rezervare_repository = rezervare_repository
        self.rezervare_validator = rezervare_validator
        self.filme_repository = filme_repository
        self.carduri_repository = carduri_repository
        self.undo_redo_service = undo_redo_service

    def get_all(self):
        return self.rezervare_repository.read()

    def create(self, id_rezervare, id_film, id_card_client, data_ora):
        """
        Creeaza o tranzactie
        :param id_rezervare: string
        :param id_film: string
        :param id_card_client: string
        :param data_ora: string
        :return:
        """
        rezervare = Rezervare(id_rezervare, id_film, id_card_client, data_ora)
        if self.filme_repository.read(id_film) is None:
            raise NoSuchIDError(f'Nu exista niciun film cu id-ul {id_film}')
        if self.carduri_repository.read(id_card_client) is None:
            raise NoSuchIDError(f'Nu exista niciun card_client cu id-ul '
                                f'{id_card_client}')
        card_client = self.carduri_repository.read(id_card_client)
        film = self.filme_repository.read(id_film)
        card_client.puncte_acumulate += int(10/100*film.pret_bilet)
        if film.in_program == 'da':
            self.rezervare_validator.valideaza(rezervare)
            self.carduri_repository.update(card_client)
            self.rezervare_repository.create(rezervare)
            self.undo_redo_service.clear_redo()
            self.undo_redo_service.add_undo_operation(
                AddOperation(self.rezervare_repository, rezervare))
        else:
            print('Nu se poate face rezervarea pentru ca '
                  'filmul nu mai este in program')

    def delete(self, id_rezervare):
        """
        Sterge o rezervare dupa un id dat
        :return:
        """
        rezervare = self.rezervare_repository.read(id_rezervare)
        self.rezervare_repository.delete(id_rezervare)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            DeleteOperation(self.rezervare_repository, rezervare))

    def update(self, id_rezervare, id_film, id_card_client, data_ora):
        """
        Modifica o rezervare dupa un id dat
        :param id_rezervare: string
        :param id_film: string
        :param id_card_client: string
        :param data_ora: string
        :return:
        """
        rezervare = self.rezervare_repository.read(id_rezervare)
        rezervare_veche = self.rezervare_repository.read(id_rezervare)
        if rezervare is None:
            raise NoSuchIDError(f'Nu exista nicio tranzactie cu id-ul'
                                f' {id_rezervare}')
        if id_film != '':
            if self.filme_repository.read(id_film) is None:
                raise NoSuchIDError(f'Nu exista niciun film cu id-ul'
                                    f' {id_film}')
            rezervare.id_film = id_film
        if id_card_client != '':
            if self.carduri_repository.read(id_card_client) is None:
                raise NoSuchIDError(f'Nu exista niciun card_client cu id-ul'
                                    f' {id_card_client}')
            rezervare.id_card_client = id_card_client
        if data_ora != '':
            rezervare.data_ora = data_ora
        self.rezervare_validator.valideaza(rezervare)
        self.rezervare_repository.update(rezervare)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            ModifyOperation(self.rezervare_repository, rezervare_veche,
                            rezervare))

    def get_day(self, rezervare):
        data_si_ora = rezervare.data_ora
        data = data_si_ora.split(" ")[0]
        data_components = data.split('.')
        return int(data_components[0])

    def stergere_cascada(self, id_film: str):
        lista = self.rezervare_repository.read()
        rezervari = list(filter(lambda x: x.id_film == id_film, lista))
        for rezervare in rezervari:
            self.rezervare_repository.delete(rezervare.id_entitate)
        return rezervari

    def stergere_rezervari_interval(self, data1, data2):
        if data2 < data1:
            raise IncorrectRange("Data2 trebuie sa fie mai mare decat data1")
        rezervari_sterse = []
        rezervari = self.get_all()
        rezervari_finala = list(rez for rez in rezervari if
                                self.get_day(rez) < data1 or
                                self.get_day(rez) > data2)
        for rezervare in rezervari:
            if rezervare not in rezervari_finala:
                rezervari_sterse.append(rezervare)
                self.rezervare_repository.delete(rezervare.id_entitate)
        self.undo_redo_service.clear_redo()
        stergere = StergereEntitatiOperation(self.rezervare_repository,
                                             rezervari_sterse)
        self.undo_redo_service.add_undo_operation(stergere)
