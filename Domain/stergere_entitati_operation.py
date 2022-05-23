from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class StergereEntitatiOperation(UndoRedo):
    def __init__(self, repository: Repository,
                 lista: list[Entitate]):
        self.repository = repository
        self.lista = lista

    def do_undo(self):
        for entitate in self.lista:
            self.repository.create(entitate)

    def do_redo(self):
        for entitate in self.lista:
            self.repository.delete(entitate.id_entitate)
