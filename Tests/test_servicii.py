from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.utils import clear_file


def test_service():
    test_create_card()
    test_delete_card()
    test_update_card()
    test_create_film()
    test_update_film()
    test_add_reservation()
    test_delete_reservation()
    test_update_reservation()
    test_ordonare_filme()
    test_ordodonare_carduri()
    test_random_generator()
    test_stergere_cascada()
    test_interval_orar()


def test_create_card():
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    card_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_service = CardClientService(card_repo, card_validator,
                                     undo_redo_service)

    card_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                        '01.05.2002', '20.11.2021', 0)
    assert len(card_service.get_all()) == 1
    added = card_repo.read('1')
    assert added is not None
    assert added.id_entitate == '1'
    assert added.nume == 'Surdu'
    assert added.prenume == 'Lucian'
    assert added.cnp == '5020501020477'
    assert added.data_nasterii == '01.05.2002'
    assert added.data_inregistrarii == '20.11.2021'
    assert added.puncte_acumulate == 0


def test_delete_card():
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    card_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_service = CardClientService(card_repo, card_validator,
                                     undo_redo_service)

    card_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                        '01.05.2002', '20.11.2021', 0)

    card_service.delete('1')
    assert len(card_service.get_all()) == 0


def test_update_card():
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    card_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_service = CardClientService(card_repo, card_validator,
                                     undo_redo_service)

    card_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                        '01.05.2002', '20.11.2021', 0)

    card_service.update('1', 'Lucian', 'Surdu', '5020501020477',
                        '01.05.2002', '20.11.2021', 100)
    updated = card_repo.read('1')
    assert updated is not None
    assert updated.id_entitate == '1'
    assert updated.nume == 'Lucian'
    assert updated.prenume == 'Surdu'
    assert updated.cnp == '5020501020477'
    assert updated.data_nasterii == '01.05.2002'
    assert updated.data_inregistrarii == '20.11.2021'
    assert updated.puncte_acumulate == 100


def test_create_film():
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repo, film_validator,
                               undo_redo_service)
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    added = film_repo.read('1')
    assert len(film_service.get_all()) == 1
    assert added.id_entitate == '1'
    assert added.titlu == 'No way home'
    assert added.an_aparitie == 2021
    assert added.pret_bilet == 30.0
    assert added.in_program == 'da'


def test_delete_film():
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repo, film_validator,
                               undo_redo_service)
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    try:
        film_service.delete('2')
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

    film_service.delete('1')
    assert len(film_service.get_all()) == 0


def test_update_film():
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repo, film_validator,
                               undo_redo_service)
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    film_service.update('1', 'Far from home', 2019, 25.0, 'nu')
    updated = film_repo.read('1')
    assert updated.id_entitate == '1'
    assert updated.titlu == 'Far from home'
    assert updated.an_aparitie == 2019
    assert updated.pret_bilet == 25.0
    assert updated.in_program == 'nu'


def test_add_reservation():
    clear_file('rezervari_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    rezervari_validator = RezervareValidator()
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    undo_redo_service = UndoRedoService()
    service = RezervareService(rezervari_repo, rezervari_validator,
                               film_repo, card_repo, undo_redo_service)
    film_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    service.create('1', '1', '1', '3.12.2021 11:28')
    added = rezervari_repo.read('1')
    assert len(service.get_all()) == 1
    assert added is not None
    assert added.id_entitate == '1'
    assert added.id_film == '1'
    assert added.id_card_client == '1'
    assert added.data_ora == '3.12.2021 11:28'


def test_delete_reservation():
    clear_file('rezervari_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    rezervari_validator = RezervareValidator()
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    undo_redo_service = UndoRedoService()
    service = RezervareService(rezervari_repo, rezervari_validator,
                               film_repo, card_repo, undo_redo_service)
    film_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    service.create('1', '1', '1', '3.12.2021 11:28')

    assert rezervari_repo.read('1') is not None

    service.delete('1')
    assert rezervari_repo.read('1') is None


def test_update_reservation():
    clear_file('rezervari_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    rezervari_validator = RezervareValidator()
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    undo_redo_service = UndoRedoService()
    service = RezervareService(rezervari_repo, rezervari_validator,
                               film_repo, card_repo, undo_redo_service)
    film_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    service.create('1', '1', '1', '3.12.2021 11:28')

    service.update('1', '1', '1', '4.11.2019 6:22')
    updated = rezervari_repo.read('1')
    assert updated is not None
    assert updated.id_entitate == '1'
    assert updated.data_ora == '4.11.2019 6:22'


def test_ordonare_filme():
    clear_file('filme_test.json')
    clear_file('rezervari_test.json')
    clear_file('carduri_test.json')
    filme_repo = JsonRepository('filme_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    card_repo = JsonRepository('carduri_test.json')
    funct_repo = JsonRepository('functionalitati_test.json')
    undo_redo_service = UndoRedoService()
    functionalitati = Functionalitati(filme_repo, card_repo,
                                      rezervari_repo, funct_repo,
                                      undo_redo_service)

    filme_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    filme_repo.create(Film('2', 'Far from home,', 2019, 20.0, 'da'))
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    rezervari_repo.create(Rezervare('1', '1', '1', '3.12.2021 11:28'))
    rezervari_repo.create(Rezervare('2', '1', '1', '4.12.2021 6:28'))
    rezervari_repo.create(Rezervare('3', '2', '1', '3.12.2021 11:28'))

    filme_ordonate = functionalitati.ordonare_filme()
    assert len(filme_ordonate) == 2
    assert filme_ordonate[0].rezervari == 2
    assert filme_ordonate[1].rezervari == 1


def test_ordodonare_carduri():
    clear_file('filme_test.json')
    clear_file('rezervari_test.json')
    clear_file('carduri_test.json')
    filme_repo = JsonRepository('filme_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    card_repo = JsonRepository('carduri_test.json')
    funct_repo = JsonRepository('functionalitati_test.json')
    undo_redo_service = UndoRedoService()
    functionalitati = Functionalitati(filme_repo, card_repo,
                                      rezervari_repo, funct_repo,
                                      undo_redo_service)
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    card_repo.create(CardClient('2', 'Surdu', 'David', '5020501020477',
                                '01.05.2002', '20.11.2021', 100))
    card_repo.create(CardClient('3', 'Surdu', 'Alex', '5020501020477',
                                '01.05.2002', '20.11.2021', 10))
    carduri_ordonate = functionalitati.ordonare_carduri()

    assert len(carduri_ordonate) == 3
    assert carduri_ordonate[0].puncte_acumulate == 100
    assert carduri_ordonate[0].id_entitate == '2'
    assert carduri_ordonate[1].puncte_acumulate == 10
    assert carduri_ordonate[2].puncte_acumulate == 0


def test_random_generator():
    clear_file('filme_test.json')
    clear_file('rezervari_test.json')
    clear_file('carduri_test.json')
    filme_repo = JsonRepository('filme_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    card_repo = JsonRepository('carduri_test.json')
    funct_repo = JsonRepository('functionalitati_test.json')
    undo_redo_service = UndoRedoService()
    functionalitati = Functionalitati(filme_repo, card_repo,
                                      rezervari_repo, funct_repo,
                                      undo_redo_service)
    functionalitati.random_generator(3)
    assert len(filme_repo.read()) == 3


def test_stergere_cascada():
    clear_file('rezervari_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    rezervari_validator = RezervareValidator()
    clear_file('filme_test.json')
    film_repo = JsonRepository('filme_test.json')
    clear_file('carduri_test.json')
    card_repo = JsonRepository('carduri_test.json')
    undo_redo_service = UndoRedoService()
    service = RezervareService(rezervari_repo, rezervari_validator,
                               film_repo, card_repo,
                               undo_redo_service)
    film_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    rezervari_repo.create(Rezervare('1', '1', '1', '3.12.2021 11:28'))
    assert len(rezervari_repo.read()) == 1
    service.stergere_cascada('1')
    assert len(rezervari_repo.read()) == 0


def test_interval_orar():
    clear_file('filme_test.json')
    clear_file('rezervari_test.json')
    clear_file('carduri_test.json')
    filme_repo = JsonRepository('filme_test.json')
    rezervari_repo = JsonRepository('rezervari_test.json')
    card_repo = JsonRepository('carduri_test.json')
    funct_repo = JsonRepository('functionalitati_test.json')
    undo_redo_service = UndoRedoService()
    functionalitati = Functionalitati(filme_repo, card_repo,
                                      rezervari_repo, funct_repo,
                                      undo_redo_service)
    filme_repo.create(Film('1', 'No way home', 2021, 30.0, 'da'))
    card_repo.create(CardClient('1', 'Surdu', 'Lucian', '5020501020477',
                                '01.05.2002', '20.11.2021', 0))
    rezervari_repo.create(Rezervare('1', '1', '1', '3.12.2021 2:28'))
    rezervari_repo.create(Rezervare('2', '1', '1', '3.12.2021 4:28'))
    rezervari_repo.create(Rezervare('3', '1', '1', '3.12.2021 6:28'))
    rezultat = functionalitati.afiseaza_interval_orar(4, 6)
    assert len(rezultat) == 2
