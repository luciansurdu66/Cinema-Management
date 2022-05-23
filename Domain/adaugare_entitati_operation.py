from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class AdaugareEntitatiOperation(UndoRedo):
    def __init__(self, repository: Repository,
                 lista: list[Entitate]):
        self.repository = repository
        self.lista = lista

    def do_undo(self):
        for entity in self.lista:
            self.repository.delete(entity.id_entitate)

    def do_redo(self):
        for entity in self.lista:
            self.repository.create(entity)
