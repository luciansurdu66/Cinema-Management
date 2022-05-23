from abc import ABC


class UndoRedo(ABC):
    def do_undo(self):
        ...

    def do_redo(self):
        ...
