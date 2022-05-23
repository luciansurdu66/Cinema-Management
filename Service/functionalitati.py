import random
import string

from Domain.adaugare_entitati_operation import AdaugareEntitatiOperation
from Domain.card_client import CardClient
from Domain.film import Film
from Repository.json_repository import JsonRepository
from Service.undo_redo_service import UndoRedoService
from ViewModels.film_ordonat_descrescator_view_model\
    import FilmOrdonatDescrescatorViewModel
from ViewModels.rezervare_view_model import RezervareViewModel


class Functionalitati:
    def __init__(self, film_repository: JsonRepository,
                 card_client_repository: JsonRepository,
                 rezervare_repository: JsonRepository,
                 functionalitati_repository: JsonRepository,
                 undo_redo_service: UndoRedoService):
        self.film_repository = film_repository
        self.card_client_repository = card_client_repository
        self.rezervare_repository = rezervare_repository
        self.functionalitati_repository = functionalitati_repository
        self.undo_redo_service = undo_redo_service

    def search_film(self, film: Film, secventa):
        """
        Cauta in filme toate datele care contin un string introdus
        :param film: string
        :param secventa: string
        :return:
        """
        lst = [film.id_entitate,
               film.titlu,
               film.an_aparitie,
               film.pret_bilet,
               film.in_program]
        for prop in range(len(lst)):
            if str(lst[prop]).find(secventa) != -1:
                return self.film_repository.read(film)
        return None

    def search_card(self, card_client: CardClient, secventa):
        """
        Cauta in carduri toate datele care contin un string introdus
        :param card_client: string
        :param secventa: string
        :return:
        """
        lst = [card_client.id_entitate,
               card_client.nume,
               card_client.prenume,
               card_client.cnp,
               card_client.data_nasterii,
               card_client.data_inregistrarii,
               card_client.puncte_acumulate]
        for prop in range(len(lst)):
            if str(lst[prop]).find(secventa) != -1:
                return self.card_client_repository.read(card_client)
        return None

    def afiseaza_interval_orar(self, start, end):
        """
        Afiseaza rezervarile dintr-un
         anumit interval de ore dat,
          indiferent de zi
        :param start: intreg
        :param end: intreg
        :return:
        """
        rezervari = self.rezervare_repository.read()
        view_models = []
        for rezervare in rezervari:
            ora = rezervare.data_ora.split(' ')
            ora1 = ora[1].split(':')
            if start <= int(ora1[0]) <= end:
                film = self.film_repository.read(rezervare.id_film)
                card_client = self.card_client_repository.read(
                    rezervare.id_card_client)
                view_models.append(
                    RezervareViewModel(
                        rezervare.id_entitate,
                        film,
                        card_client,
                        rezervare.data_ora))
        return view_models

    def merge(self, array, left_index, right_index, middle, key_func):
        left_copy = array[left_index:middle + 1]
        right_copy = array[middle + 1:right_index + 1]

        left_copy_index = 0
        right_copy_index = 0
        sorted_index = left_index

        while left_copy_index < len(left_copy) \
                and right_copy_index < len(right_copy):

            if key_func(left_copy[left_copy_index],
                        right_copy[right_copy_index]):
                array[sorted_index] = left_copy[left_copy_index]
                left_copy_index = left_copy_index + 1
            else:
                array[sorted_index] = right_copy[right_copy_index]
                right_copy_index = right_copy_index + 1

            sorted_index = sorted_index + 1

        while left_copy_index < len(left_copy):
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index = left_copy_index + 1
            sorted_index = sorted_index + 1

        while right_copy_index < len(right_copy):
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index = right_copy_index + 1
            sorted_index = sorted_index + 1

    def merge_sort(self,
                   array,
                   left_index,
                   right_index,
                   key_func=lambda x, y: x < y):
        if left_index >= right_index:
            return
        middle = (left_index + right_index) // 2
        self.merge_sort(array, left_index, middle, key_func)
        self.merge_sort(array, middle + 1, right_index, key_func)
        self.merge(array, left_index, right_index, middle, key_func)

    def ordonare_filme(self):
        rezultat = []
        r = {}
        filme = self.film_repository.read()
        rezervari = self.rezervare_repository.read()

        for film in filme:
            r[film.id_entitate] = 0
        for rezervare in rezervari:
            if rezervare.id_film in r.keys():
                r[rezervare.id_film] += 1
            else:
                r[rezervare.id_film] = 1
        for id_film in r:
            film = self.film_repository.read(id_film)
            lista = r[id_film]
            if lista:
                rezultat.append(FilmOrdonatDescrescatorViewModel(film, lista))
            else:
                rezultat.append(FilmOrdonatDescrescatorViewModel(film, 0))
        self.merge_sort(rezultat, 0, len(rezultat) - 1,
                        lambda x, y: x.rezervari > y.rezervari)
        return rezultat

    def ordonare_carduri(self):
        carduri = self.card_client_repository.read()
        carduri.sort(key=lambda x: x.puncte_acumulate, reverse=True)
        return carduri

    def random_generator(self, numar: int):
        entitati_adaugate = []
        while numar:
            letters_and_digits = string.ascii_letters + string.digits
            id_film = ''.join(random.choice(letters_and_digits))
            letters = string.ascii_lowercase
            titlu = ''.join(random.choice(letters))
            an_aparitie = random.randint(1900, 2021)
            pret = float(random.randint(1, 100))
            in_program = random.choice(['da', 'nu'])
            film = Film(id_film, titlu, an_aparitie, pret, in_program)
            self.film_repository.create(Film(id_film,
                                        titlu,
                                        an_aparitie,
                                        pret,
                                        in_program))
            entitati_adaugate.append(film)
            numar -= 1
        self.undo_redo_service.clear_redo()
        stergere = AdaugareEntitatiOperation(self.film_repository,
                                             entitati_adaugate)
        self.undo_redo_service.add_undo_operation(stergere)
