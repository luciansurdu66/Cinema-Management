from Tests.test_domain import test_card_client, test_film, test_rezervare
from Tests.test_repository import test_repository
from Tests.test_servicii import test_service
from Tests.test_undo_redo import test_undo_redo


def test_all():
    test_card_client()
    test_film()
    test_rezervare()
    test_repository()
    test_service()
    test_undo_redo()
