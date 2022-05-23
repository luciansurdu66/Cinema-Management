from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class StergereCascadaOperation(UndoRedo):
    def __init__(self, entitate_repo: Repository,
                 entitati_repo: Repository,
                 entitate_stearsa: Entitate,
                 lista: list[Entitate]):
        self.entitate_repository = entitate_repo
        self.entitati_repository = entitati_repo
        self.entitate_stearsa = entitate_stearsa
        self.lista = lista

    def do_undo(self):
        self.entitate_repository.create(self.entitate_stearsa)
        for entitate in self.lista:
            self.entitati_repository.create(entitate)

    def do_redo(self):
        self.entitate_repository.delete(self.entitate_stearsa.id_entitate)
        for entitate in self.lista:
            self.entitati_repository.delete(entitate.id_entitate)
