from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class ModifyOperation(UndoRedo):
    def __init__(self, repository: Repository,
                 obiect_vechi: Entitate,
                 obiect_nou: Entitate):
        self.repository = repository
        self.obiect_vechi = obiect_vechi
        self.obiect_nou = obiect_nou

    def do_undo(self):
        self.repository.update(self.obiect_vechi)

    def do_redo(self):
        self.repository.update(self.obiect_nou)
