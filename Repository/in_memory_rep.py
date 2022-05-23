from Domain.entitate import Entitate
from Repository.Exceptii import DuplicateIDError, NoSuchIDError
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Verifica daca exista o entitate cu id-ul dat
        Daca nu se va pune nici un parametru aceste functii
        ea va returna lista de obiecte
        :param id_entitate: id-ul entitatii pe care il cautam
        :return: Daca id_entitate este None va returna lista de obiecte
                 Daca id_entitate este in lista de entitati va returna id
                 card
                 Daca id_entitate nu este in lista de entitati va returna
                 None
        """
        if id_entitate is None:
            return list(self.entitati.values())

        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga un obiect de tip Entitate in lista
        :param entitate: obiect de tip Entitate
        :return: None
        """
        if self.read(entitate.id_entitate) is not None:
            raise DuplicateIDError("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate: str):
        """
        Sterge un obiect de tip Entitate din lista
        :param id_entitate: obiect de tip Entitate
        :return: None
        """
        if self.read(id_entitate) is None:
            raise NoSuchIDError("Nu exista nicio entitate cu id-ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica un obiect de tip Entitate din lista
        :param entitate: obiect de tip Entitate
        :return: None
        """
        if self.read(entitate.id_entitate) is None:
            raise NoSuchIDError("Nu exista nicio entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate
