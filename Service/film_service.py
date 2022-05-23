from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.modify_operation import ModifyOperation
from Repository.Exceptii import IncorrectData, NoSuchIDError
from Repository.json_repository import JsonRepository
from Service.undo_redo_service import UndoRedoService


class FilmService:

    def __init__(self, film_repository: JsonRepository,
                 film_validator: FilmValidator,
                 undo_redo_service: UndoRedoService):
        """

        :param film_repository:
        :param film_validator:
        """
        self.film_repository = film_repository
        self.film_validator = film_validator
        self.undo_redo_service = undo_redo_service

    def get_all(self):
        return self.film_repository.read()

    def create(self, id_film, titlu, an_aparitie, pret_bilet, in_program):
        """
        Adauga un film
        :param id_film:
        :param titlu:
        :param an_aparitie:
        :param pret_bilet:
        :param in_program:
        :return:
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.film_validator.valideaza(film)

        if in_program != 'da' and in_program != 'nu':
            raise IncorrectData("Trebuie sa raspundeti cu da sau nu!")

        self.film_repository.create(film)

        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            AddOperation(self.film_repository, film))

    def delete(self, id_film):
        """
        Sterge un film dupa un id dat
        :param id_film:
        :return:
        """
        if self.film_repository.read(id_film) is not None:
            film = self.film_repository.read(id_film)
        self.film_repository.delete(id_film)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            DeleteOperation(self.film_repository, film))

    def update(self, id_film, titlu, an_aparitie, pret_bilet, in_program):
        """
        Schimba datele unui film dat prin id
        :param id_film:
        :param titlu:
        :param an_aparitie:
        :param pret_bilet:
        :param in_program:
        :return:
        """
        film = self.film_repository.read(id_film)
        if film is None:
            raise NoSuchIDError(f'Nu exista un film cu id-ul {id_film}')

        if titlu != '':
            film.titlu = titlu
        if an_aparitie != 0:
            film.an_aparitie = an_aparitie
        if pret_bilet != 0:
            film.pret_bilet = pret_bilet
        if in_program != '':
            film.in_program = in_program

        if self.film_repository.read(id_film) is not None:
            film_vechi = self.film_repository.read(id_film)
        self.undo_redo_service.clear_redo()
        self.undo_redo_service.add_undo_operation(
            ModifyOperation(self.film_repository, film_vechi, film)
        )
        self.film_validator.valideaza(film)
        self.film_repository.update(film)
