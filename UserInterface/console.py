import datetime

from Domain.stergere_cascada_operation import StergereCascadaOperation
from Repository.Exceptii import DuplicateIDError, IncorrectData, IncorrectRange
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


class Console:

    def __init__(self, film_service: FilmService,
                 film_repository: JsonRepository,
                 card_client_service: CardClientService,
                 rezervare_service: RezervareService,
                 functionalitati_service: Functionalitati,
                 undo_redo_service: UndoRedoService):
        self.film_repository = film_repository
        self.film_service = film_service
        self.card_client_service = card_client_service
        self.rezervare_service = rezervare_service
        self.functionalitati_service = functionalitati_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('1. CRUD filme')
        print('2. CRUD carduri')
        print('3. CRUD rezervari')
        print('4. Functionalitati')
        print('u. Undo')
        print('r. Redo')
        print('x. Exit')

    def run_crud_filme(self):
        while True:
            print('1. Adaugare film')
            print('2. Stergere film')
            print('3. Modificare film')
            print('a. Afiseaza toate filmele')
            print('x. Inapoi')
            optiune = input('Dati optiunea: ')
            if optiune == '1':
                self.handle_create_film()
            elif optiune == '2':
                self.handle_delete_film()
            elif optiune == '3':
                self.handle_update_film()
            elif optiune == 'a':
                self.handle_show_films()
            elif optiune == 'x':
                break
            else:
                print('Optiune invalida!')

    def run_crud_carduri(self):
        while True:
            print('1. Adaugare card')
            print('2. Stergere card')
            print('3. Modificare card')
            print('a. Afiseaza toate cardurile')
            print('x. Inapoi')
            optiune = input('Dati optiunea: ')
            if optiune == '1':
                self.handle_create_card()
            elif optiune == '2':
                self.handle_delete_card()
            elif optiune == '3':
                self.handle_update_card()
            elif optiune == 'a':
                self.handle_show_cards()
            elif optiune == 'x':
                break
            else:
                print('Optiune invalida!')

    def run_crud_rezervari(self):
        while True:
            print('1. Adaugare rezervare')
            print('2. Stergere rezervare')
            print('3. Modificare rezervare')
            print('a. Afiseaza toate rezervarile')
            print('x. Inapoi')
            optiune = input('Dati optiunea: ')
            if optiune == '1':
                self.handle_create_reservation()
            elif optiune == '2':
                self.handle_delete_reservation()
            elif optiune == '3':
                self.handle_update_reservation()
            elif optiune == 'a':
                self.handle_show_reservations()
            elif optiune == 'x':
                break
            else:
                print('Optiune invalida!')

    def run_console(self):

        while True:
            self.show_menu()
            option = input('Optiunea aleasa:')
            if option == '1':
                self.run_crud_filme()
            elif option == '2':
                self.run_crud_carduri()
            elif option == '3':
                self.run_crud_rezervari()
            elif option == '4':
                self.run_functionalitati()
            elif option == 'u':
                self.undo_redo_service.undo()
            elif option == 'r':
                self.undo_redo_service.redo()
            elif option == 'x':
                break
            else:
                print("Optiune invalida, reincercati.")

    def handle_create_film(self):
        try:
            id_film = input("Dati id-ul filmului: ")
            titlu = input("Dati titlul filmului: ")
            an_aparitie = int(input("Dati anul aparitiei filmului: "))
            pret_bilet = float(input("Dati pretul "
                                     "biletului pentru acest film: "))
            in_program = input("Spuneti daca filmul este sau nu in program: ")
            self.film_service.create(id_film,
                                     titlu,
                                     an_aparitie,
                                     pret_bilet,
                                     in_program)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_delete_film(self):
        try:
            id_film = input('Da id-ul filmului pe care vrei sa-l stergi: ')
            rezervari = self.rezervare_service.stergere_cascada(id_film)
            film = self.film_service.film_repository.read(id_film)
            self.film_service.delete(id_film)
            self.undo_redo_service.clear_redo()
            stergere = StergereCascadaOperation(
                self.film_repository,
                self.rezervare_service.rezervare_repository, film,
                rezervari)
            self.undo_redo_service.add_undo_operation(stergere)
        except DuplicateIDError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def handle_update_film(self):
        try:
            id_film = input('ID-ul filmului: ')
            titlu = input('Titlul filmului: ')
            an_aparitie = input('Anul in care a aparut filmul')
            pret_bilet = float(input('Pretul biletului: '))
            in_program = input('Se afla in program? (da/nu): ')

            self.film_service.update(id_film,
                                     titlu,
                                     an_aparitie,
                                     pret_bilet,
                                     in_program)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_show_films(self):
        print('Avem urmatoarele filme: ')
        for film in self.film_service.get_all():
            print(film)

    def handle_create_card(self):
        try:
            id_card_client = input('ID-ul cardului_cient: ')
            nume = input('Numele clientului: ')
            prenume = input('Prenumele clientului: ')
            cnp = input('CNP-ul clientului: ')
            data_nastere = input('Data de nastere (dd.mm.yyyy):')
            data_inregistrare = input('Data de inregistrare (dd.mm.yyyy):')
            puncte_acumulate = int(input('Cate puncte acumulate sunt:'))
            self.card_client_service.create(id_card_client,
                                            nume,
                                            prenume,
                                            cnp,
                                            data_nastere,
                                            data_inregistrare,
                                            puncte_acumulate)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_delete_card(self):
        try:
            id_card_client = input('ID-ul cardului pe care '
                                   'vreti sa-l stergeti: ')
            self.card_client_service.delete(id_card_client)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_update_card(self):
        try:
            id_card_client = input('ID-ul cardului_cient: ')
            nume = input('Numele clientului: ')
            prenume = input('Prenumele clientului: ')
            cnp = input('CNP-ul clientului: ')
            data_nastere = input('Data de nastere(dd.mm.yyyy): ')
            data_inregistrare = input('Data de inregistrare(dd.mm.yyyy): ')
            puncte_acumulate = int(input("Numarul de puncte acumulate: "))

            self.card_client_service.update(id_card_client,
                                            nume,
                                            prenume,
                                            cnp,
                                            data_nastere,
                                            data_inregistrare,
                                            puncte_acumulate)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_show_cards(self):
        print("Avem urmatoarele carduri: ")
        for card_client in self.card_client_service.get_all():
            print(card_client)

    def handle_create_reservation(self):
        try:
            id_rezervare = input('ID-ul rezervarii: ')
            id_film = input('ID-ul filmului: ')
            id_card_client = input('ID-ul cardului: ')
            data_ora = input('Data si ora: ')

            self.rezervare_service.create(id_rezervare,
                                          id_film,
                                          id_card_client,
                                          data_ora)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_delete_reservation(self):
        try:
            id_rezervare = input('ID-ul rezervarii'
                                 ' pe care vreti sa-l stergeti: ')
            self.rezervare_service.delete(id_rezervare)
            print('Stergere facuta')
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_update_reservation(self):
        try:
            id_rezervare = input('ID-ul rezervarii: ')
            id_film = input('ID-ul filmului: ')
            id_card_client = input('ID-ul cardului: ')
            data_ora = input('Data si ora: ')

            self.rezervare_service.update(id_rezervare,
                                          id_film,
                                          id_card_client,
                                          data_ora)
        except IncorrectData as ID:
            print(ID)
        except DuplicateIDError as DE:
            print(DE)
        except Exception as e:
            print(e)

    def handle_show_reservations(self):
        for rezervare in self.rezervare_service.get_all():
            print(rezervare)

    def run_functionalitati(self):
        while True:
            print('1. Cautare film si clienti full text.')
            print('2. Afiseaza toate rezervarile '
                  'dintr-un interval de ore dat')
            print('3. Afisarea filmelor ordonate '
                  'descrescator dupa numarul de rezervari')
            print('4. Afisarea cardurilor client'
                  ' ordonate descrescator dupa '
                  'numarul de puncte de pe card')
            print('5. Stergerea tuturor rezervarilor'
                  ' dintr-un anumit interval de zile')
            print('6. Incrementarea cu o valoare data a punctelor'
                  'de pe cardurile a caror zi de nastere se afla '
                  'intr-un interval dat.')
            print('r. Random generator')
            print('x. Inapoi')
            option = input('Alegeti optiunea: ')
            if option == '1':
                self.handle_fulltext()
            elif option == '2':
                self.handle_show_interval()
            elif option == '3':
                self.handle_show_sorted()
            elif option == '4':
                self.handle_cards_sorted()
            elif option == '5':
                self.handle_delete_interval()
            elif option == '6':
                self.handle_incrementare()
            elif option == 'r':
                self.handle_random_generator()
            elif option == 'x':
                break
            else:
                print('Optiune invalida.')

    def handle_fulltext(self):
        try:
            secventa = input('Dati secventa pe care o cautati: ')
            ok = 0
            for film in self.film_service.get_all():
                rezultat = self.functionalitati_service. \
                    search_film(film, secventa)
                if rezultat is not None:
                    ok += 1
                    print(rezultat)

            for card_client in self.card_client_service.get_all():
                rezultat = self.functionalitati_service. \
                    search_card(card_client, secventa)
                if rezultat is not None:
                    ok += 1
                    print(rezultat)
            if ok == 0:
                print('Secventa cautata nu exista!')
        except IncorrectData as ID:
            print(ID)

    def handle_random_generator(self):
        try:
            numar = int(input("Cate obiecte doriti? "))
            self.functionalitati_service.random_generator(numar)
            self.handle_show_films()
        except IncorrectData as ID:
            print(ID)
        except Exception as e:
            print(e)

    def handle_show_interval(self):
        start = int(input("Dati ora de la care incepe intervalul: "))
        end = int(input("Dati ora la care se termina intervalul: "))
        rezervari = self.functionalitati_service.\
            afiseaza_interval_orar(start, end)
        for rezervare in rezervari:
            print(rezervare)

    def handle_show_sorted(self):
        filme = self.functionalitati_service.ordonare_filme()
        for film in filme:
            print(film)

    def handle_cards_sorted(self):
        carduri = self.functionalitati_service.ordonare_carduri()
        for card in carduri:
            print(card)

    def handle_delete_interval(self):
        try:
            interval = input("Dati intervalul de zile (de forma ZZ-ZZ): ")
            interval = interval.split("-")
            if len(interval) != 2:
                raise IncorrectRange('Intervalul trebuie sa contina 2 '
                                     'zile pentru a fi considerat unul ')
            left = int(interval[0])
            right = int(interval[1])
            if interval[0] > interval[1]:
                raise IncorrectRange('Intervalul de zile trebuie sa fie '
                                     'crescator!')
            self.rezervare_service.stergere_rezervari_interval(left, right)
            self.handle_show_reservations()
        except Exception as e:
            print(e)

    def handle_incrementare(self):
        try:
            valoare = int(input('Dati valoarea cu care se incrementeaza '
                                'punctele: '))
            an1 = int(input("Dati anul datei 1: "))
            luna1 = int(input("Dati luna datei 1: "))
            zi1 = int(input("Dati ziua datei 1: "))
            data1 = datetime.datetime(an1, luna1, zi1)
            an2 = int(input("Dati anul datei 2: "))
            luna2 = int(input("Dati luna datei 2: "))
            zi2 = int(input("Dati ziua datei 2: "))
            data2 = datetime.datetime(an2, luna2, zi2)
            self.card_client_service.incrementare_valoare(valoare,
                                                          data1, data2)
            self.handle_show_cards()
        except IncorrectData as ID:
            print(ID)
        except Exception as ex:
            print(ex)
