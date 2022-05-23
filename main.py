from Domain.card_client_validator import CardClientValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.test_all import test_all
from UserInterface.console import Console


def main():
    undo_redo_service = UndoRedoService()

    film_repository = JsonRepository('filme.json')
    film_validator = FilmValidator()

    carduri_repository = JsonRepository('clienti.json')
    card_client_validator = CardClientValidator()

    rezervare_repository = JsonRepository('rezervari.json')
    rezervare_validator = RezervareValidator()

    functionalitati_repository = JsonRepository('functionalitati.json')

    film_serivce = FilmService(film_repository, film_validator,
                               undo_redo_service)
    card_client_service = CardClientService(carduri_repository,
                                            card_client_validator,
                                            undo_redo_service)
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         carduri_repository,
                                         undo_redo_service)
    functionalitati_service = Functionalitati(film_repository,
                                              carduri_repository,
                                              rezervare_repository,
                                              functionalitati_repository,
                                              undo_redo_service)

    console = Console(film_serivce,
                      film_repository,
                      card_client_service,
                      rezervare_service,
                      functionalitati_service,
                      undo_redo_service)

    console.run_console()


if __name__ == '__main__':
    test_all()
    main()
