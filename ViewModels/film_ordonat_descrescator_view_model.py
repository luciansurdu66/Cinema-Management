class FilmOrdonatDescrescatorViewModel:
    def __init__(self, film, rezervari):
        self.film = film
        self.rezervari = rezervari

    def __str__(self):
        return f'Filmul {self.film} are {self.rezervari} rezervari'
