import copy

class UndoRedoManager:
    """Mag-manage ng undo/redo states gamit ang deep copy ng image objects"""
    def __init__(self):
        self._states = []
        self._index = -1

    def add_state(self, image):
        """I-save ang current state; pwede PIL.Image o anumang mutable object"""
        # tanggalin ang future states kapag bagong action
        self._states = self._states[:self._index + 1]
        self._states.append(copy.deepcopy(image))
        self._index += 1

    def undo(self):
        """Bumalik sa previous state; ibalik None kung wala nang undo"""
        if self._index > 0:
            self._index -= 1
            return copy.deepcopy(self._states[self._index])
        return None

    def redo(self):
        """Pumunta sa next state; ibalik None kung wala nang redo"""
        if self._index < len(self._states) - 1:
            self._index += 1
            return copy.deepcopy(self._states[self._index])
        return None

    def clear(self):
        """I-reset ang history"""
        self._states.clear()
        self._index = -1
