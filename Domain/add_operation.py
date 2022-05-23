from Domain.Undo_Redo_Operation import UndoRedo
from Domain.entitate import Entitate
from Repository.repository import Repository


class AddOperation(UndoRedo):
    def __init__(self, repository: Repository,
                 obiect: Entitate):
        self.repository = repository
        self.obiect = obiect

    def do_undo(self):
        self.repository.delete(self.obiect.id_entitate)

    def do_redo(self):
        self.repository.create(self.obiect)
