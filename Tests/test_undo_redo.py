import datetime

from Domain.card_client_validator import CardClientValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Domain.stergere_cascada_operation import StergereCascadaOperation
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.utils import clear_file


def test_undo_redo():
    test_undo_redo_film_service()
    test_undo_redo_card_client_service()
    test_undo_redo_rezervare_service()
    test_undo_redo_generare_entitati()
    test_undo_redo_stergere_cascada()
    test_undo_redo_stergere_rezervari_interval()
    test_undo_redo_incrementare_valoare()


def test_undo_redo_film_service():
    film_repository = JsonRepository('test_undo_redo.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)

    clear_file('test_undo_redo.json')
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    film_service.create('2', 'Far from home', 2019, 25.0, 'nu')
    assert len(film_service.get_all()) == 2
    film_service.undo_redo_service.undo()
    assert len(film_service.get_all()) == 1
    film_service.undo_redo_service.redo()
    assert len(film_service.get_all()) == 2

    film_service.delete('2')
    assert len(film_service.get_all()) == 1
    film_service.undo_redo_service.undo()
    assert len(film_service.get_all()) == 2
    film_service.undo_redo_service.redo()
    assert len(film_service.get_all()) == 1

    film_service.update('1', 'Avengers', 2021, 30.0, 'da')
    assert film_service.get_all()[0].titlu == 'Avengers'
    film_service.undo_redo_service.undo()
    assert film_service.get_all()[0].titlu == 'No way home'
    film_service.undo_redo_service.redo()
    assert film_service.get_all()[0].titlu == 'Avengers'


def test_undo_redo_card_client_service():
    card_client_repository = JsonRepository('test_undo_redo.json')
    card_client_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    clear_file('test_undo_redo.json')
    card_client_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                               '01.05.2002', '20.11.2021', 0)
    card_client_service.create('2', 'Surdu', 'David', '21487124897',
                               '20.02.1997', '20.11.2021', 12)
    assert len(card_client_service.get_all()) == 2
    card_client_service.undo_redo_service.undo()
    assert len(card_client_service.get_all()) == 1
    card_client_service.undo_redo_service.redo()
    assert len(card_client_service.get_all()) == 2

    card_client_service.delete('2')
    assert len(card_client_service.get_all()) == 1
    card_client_service.undo_redo_service.undo()
    assert len(card_client_service.get_all()) == 2
    card_client_service.undo_redo_service.redo()
    assert len(card_client_service.get_all()) == 1

    card_client_service.update('1', 'Surdu', 'David', '5020501020477',
                               '01.05.2002', '20.11.2021', 0)
    assert card_client_service.get_all()[0].prenume == 'David'
    card_client_service.undo_redo_service.undo()
    assert card_client_service.get_all()[0].prenume == 'Lucian'
    card_client_service.undo_redo_service.redo()
    assert card_client_service.get_all()[0].prenume == 'David'


def test_undo_redo_rezervare_service():
    film_repository = JsonRepository('test_undo_redo_film.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)
    clear_file('test_undo_redo_film.json')
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    film_service.create('2', 'Far from home', 2019, 25.0, 'da')

    card_client_repository = JsonRepository('test_undo_redo_card.json')
    card_client_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    clear_file('test_undo_redo_card.json')
    card_client_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                               '01.05.2002', '20.11.2021', 0)
    card_client_service.create('2', 'Surdu', 'David', '21487124897',
                               '20.02.1997', '20.11.2021', 12)

    rezervare_repository = JsonRepository('test_undo_redo.json')
    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    clear_file('test_undo_redo.json')
    rezervare_service.create('1', '1', '1', '11.11.1111 11:11')
    rezervare_service.create('2', '2', '1', '22.12.1212 12:12')
    assert len(rezervare_service.get_all()) == 2
    rezervare_service.undo_redo_service.undo()
    assert len(rezervare_service.get_all()) == 1
    rezervare_service.undo_redo_service.redo()
    assert len(rezervare_service.get_all()) == 2

    rezervare_service.delete('1')
    assert rezervare_service.rezervare_repository.read('1') is None
    rezervare_service.undo_redo_service.undo()
    assert len(rezervare_service.get_all()) == 2
    rezervare_service.undo_redo_service.redo()
    assert len(rezervare_service.get_all()) == 1

    rezervare_service.update('2', '1', '1', '22.12.1212 12:12')
    assert rezervare_service.get_all()[0].id_film == '1'
    rezervare_service.undo_redo_service.undo()
    assert rezervare_service.get_all()[0].id_film == '2'
    rezervare_service.undo_redo_service.redo()
    assert rezervare_service.get_all()[0].id_film == '1'


def test_undo_redo_generare_entitati():
    filme_repo = JsonRepository('test_undo_redo_film.json')
    rezervari_repo = JsonRepository('test_undo_redo.json')
    card_repo = JsonRepository('test_undo_redo_card.json')
    funct_repo = JsonRepository('functionalitati_test.json')
    undo_redo_service = UndoRedoService()
    functionalitati = Functionalitati(filme_repo, card_repo,
                                      rezervari_repo, funct_repo,
                                      undo_redo_service)
    clear_file('test_undo_redo.json')
    clear_file('test_undo_redo_film.json')
    functionalitati.random_generator(2)
    assert len(filme_repo.read()) == 2
    functionalitati.undo_redo_service.undo()
    assert len(filme_repo.read()) == 0
    functionalitati.undo_redo_service.redo()
    assert len(filme_repo.read()) == 2


def test_undo_redo_stergere_cascada():
    film_repository = JsonRepository('test_undo_redo_film.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)

    clear_file('test_undo_redo_film.json')
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    film_service.create('2', 'Far from home', 2019, 25.0, 'da')

    card_client_repository = JsonRepository('test_undo_redo_card.json')
    card_client_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    clear_file('test_undo_redo_card.json')
    card_client_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                               '01.05.2002', '20.11.2021', 0)
    card_client_service.create('2', 'Surdu', 'David', '21487124897',
                               '20.02.1997', '20.11.2021', 12)

    rezervare_repository = JsonRepository('test_undo_redo.json')
    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    clear_file('test_undo_redo.json')
    rezervare_service.create('1', '1', '1', '11.11.1111 11:11')
    rezervare_service.create('2', '2', '1', '22.12.1212 12:12')

    assert len(film_service.get_all()) == 2
    assert len(rezervare_service.get_all()) == 2
    rezervari = rezervare_service.stergere_cascada('1')
    film = film_repository.read('1')
    film_service.delete('1')
    undo_redo_service.clear_redo()
    stergere = StergereCascadaOperation(film_repository,
                                        rezervare_repository,
                                        film,
                                        rezervari)
    undo_redo_service.add_undo_operation(stergere)

    assert len(film_service.get_all()) == 1
    assert len(rezervare_service.get_all()) == 1

    rezervare_service.undo_redo_service.undo()
    assert len(film_service.get_all()) == 2
    assert len(rezervare_service.get_all()) == 2

    rezervare_service.undo_redo_service.redo()
    assert len(film_service.get_all()) == 1
    assert len(rezervare_service.get_all()) == 1


def test_undo_redo_stergere_rezervari_interval():
    film_repository = JsonRepository('test_undo_redo_film.json')
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)

    clear_file('test_undo_redo_film.json')
    film_service.create('1', 'No way home', 2021, 30.0, 'da')
    film_service.create('2', 'Far from home', 2019, 25.0, 'da')

    card_client_repository = JsonRepository('test_undo_redo_card.json')
    card_client_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    clear_file('test_undo_redo_card.json')
    card_client_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                               '01.05.2002', '20.11.2021', 0)
    card_client_service.create('2', 'Surdu', 'David', '21487124897',
                               '20.02.1997', '20.11.2021', 12)

    rezervare_repository = JsonRepository('test_undo_redo.json')
    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    clear_file('test_undo_redo.json')
    rezervare_service.create('1', '1', '1', '11.11.1111 11:11')
    rezervare_service.create('2', '2', '1', '22.12.1212 12:12')
    rezervare_service.create('3', '1', '1', '16.12.1221 11:11')
    assert len(rezervare_service.get_all()) == 3
    rezervare_service.stergere_rezervari_interval(10, 17)
    assert len(rezervare_service.get_all()) == 1
    rezervare_service.undo_redo_service.undo()
    assert len(rezervare_service.get_all()) == 3
    rezervare_service.undo_redo_service.redo()
    assert len(rezervare_service.get_all()) == 1


def test_undo_redo_incrementare_valoare():
    card_repository = JsonRepository('test_undo_redo_card.json')
    clear_file('test_undo_redo_card.json')
    card_validator = CardClientValidator()
    undo_redo_service = UndoRedoService()
    card_service = CardClientService(card_repository, card_validator,
                                     undo_redo_service)
    card_service.create('1', 'Surdu', 'Lucian', '5020501020477',
                        '01.05.2002', '20.11.2021', 0)
    card_service.create('2', 'Surdu', 'David', '21487124897',
                        '20.02.1997', '20.11.2021', 12)
    data1 = datetime.datetime(2000, 1, 1)
    data2 = datetime.datetime(2003, 6, 12)
    card_service.incrementare_valoare(100, data1, data2)
    card_service.undo_redo_service.undo()
    assert card_service.get_all()[0].puncte_acumulate == 0
    assert card_service.get_all()[1].puncte_acumulate == 12
    card_service.undo_redo_service.redo()
    assert card_service.get_all()[0].puncte_acumulate == 100
    assert card_service.get_all()[1].puncte_acumulate == 12
