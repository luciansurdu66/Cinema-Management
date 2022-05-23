from Domain.film import Film


class FilmValidator:

    def valideaza(self, film: Film) -> None:
        """

        :param film:
        :return:
        """
        erori = []
        if film.pret_bilet < 0:
            erori.append("Pretul trebuie sa fie strict pozitiv")
        if erori:
            raise ValueError(erori)
