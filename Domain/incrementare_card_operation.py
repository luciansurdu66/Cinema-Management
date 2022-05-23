from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class IncrementareCardOperation(UndoRedo):
    def __init__(self, repository: Repository,
                 lista_veche: list[Entitate],
                 lista_noua: list[Entitate]):
        self.repository = repository
        self.lista_veche = lista_veche
        self.lista_noua = lista_noua

    def do_undo(self):
        for entitate in self.lista_veche:
            self.repository.update(entitate)

    def do_redo(self):
        for entitate in self.lista_noua:
            self.repository.update(entitate)
