from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Film(Entitate):
    """
    Creeaza un film
    - id_film: id-ul filmului, trebuie sa fie unic
    ...
    """
    titlu: str
    an_aparitie: int
    pret_bilet: float
    in_program: str
