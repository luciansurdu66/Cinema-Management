from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare


def test_card_client():
    card_client = CardClient('1', 'Surdu',
                             'Lucian', '4214142521526814',
                             '01.05.2002', '01.05.2021', 0)
    assert card_client.id_entitate == '1'
    assert card_client.nume == 'Surdu'
    assert card_client.prenume == 'Lucian'
    assert card_client.cnp == '4214142521526814'
    assert card_client.data_nasterii == '01.05.2002'
    assert card_client.data_inregistrarii == '01.05.2021'
    assert card_client.puncte_acumulate == 0


def test_film():
    film = Film('1', 'Red notice', 2021, 30.0, 'da')
    assert film.id_entitate == '1'
    assert film.titlu == 'Red notice'
    assert film.an_aparitie == 2021
    assert film.pret_bilet == 30.0
    assert film.in_program == 'da'


def test_rezervare():
    rezervare = Rezervare('1', '1', '1', '01.05.2021 14:00')
    assert rezervare.id_entitate == '1'
    assert rezervare.id_film == '1'
    assert rezervare.id_card_client == '1'
    assert rezervare.data_ora == '01.05.2021 14:00'
