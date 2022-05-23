from Domain.Undo_Redo_Operation import UndoRedo
from Repository.repository import Repository


class DeleteOperation(UndoRedo):
    def __init__(self, repository: Repository, obiect):
        self.repository = repository
        self.obiect = obiect

    def do_undo(self):
        self.repository.create(self.obiect)

    def do_redo(self):
        self.repository.delete(self.obiect.id_entitate)
