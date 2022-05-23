from typing import Protocol, Type, Union, Optional, List

from Domain.entitate import Entitate


class Repository(Protocol):
    def read(self, id_entitate=None) -> None:
        ...

    def create(self, entitate: Entitate) -> \
            Type[Union[Optional[Entitate], List[Entitate]]]:
        ...

    def delete(self, id_entitate: str) -> None:
        ...

    def update(self, entitate: Entitate) -> None:
        ...
