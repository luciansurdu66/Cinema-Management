
from typing import Dict

import jsonpickle

from Domain.entitate import Entitate
from Repository.Exceptii import NoSuchIDError
from Repository.in_memory_rep import RepositoryInMemory


class JsonRepository(RepositoryInMemory):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Entitate]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects, indent=2))

    def read(self, id_entitate=None):
        self.entitati = self.__read_file()
        return super().read(id_entitate)

    def create(self, entitate: Entitate):
        """
        Creeaza o entitate si verifica daca
        exista deja o entitate cu id-ul dat
        pentru noua entitate
        :param entitate:
        :return:
        """
        entitati = self.__read_file()
        if self.read(entitate.id_entitate) is not None:
            raise NoSuchIDError(f'Exista deja o entitate cu id-ul'
                                f' {entitate.id_entitate}')

        entitati[entitate.id_entitate] = entitate
        self.__write_file(entitati)

    def delete(self, id_entitate: str):
        """
        Sterge o entitate dupa un id dat
        :param id_entitate:
        :return:
        """
        entitati = self.__read_file()
        if self.read(id_entitate) is None:
            raise NoSuchIDError(f'Nu exista o entitate '
                                f'cu id-ul {id_entitate}!')
        del entitati[id_entitate]
        self.__write_file(entitati)

    def update(self, entitate: Entitate):
        """
        Modifica o entitate dupa un id dat
        :param entitate:
        :return:
        """
        entitati = self.__read_file()
        if self.read(entitate.id_entitate) is None:
            raise NoSuchIDError(f'Nu exista o entitate cu id-ul '
                                f'{entitate.id_entitate}!')
        entitati[entitate.id_entitate] = entitate
        self.__write_file(entitati)
