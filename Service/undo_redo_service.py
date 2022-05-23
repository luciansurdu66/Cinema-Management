from typing import List

from Domain.Undo_Redo_Operation import UndoRedo


class UndoRedoService:
    def __init__(self):
        self.undo_list: List[UndoRedo] = []
        self.redo_list: List[UndoRedo] = []

    def add_undo_operation(self, undo_redo_operation: UndoRedo):
        self.undo_list.append(undo_redo_operation)

    def undo(self):
        if self.undo_list:
            top_operation = self.undo_list.pop()
            top_operation.do_undo()
            self.redo_list.append(top_operation)

    def redo(self):
        if self.redo_list:
            top_operation = self.redo_list.pop()
            top_operation.do_redo()
            self.undo_list.append(top_operation)

    def clear_redo(self):
        self.redo_list.clear()
