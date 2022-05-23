from Domain.film import Film
from Repository.json_repository import JsonRepository
from Tests.utils import clear_file


def test_repository():

    filename = 'test_filme.json'
    clear_file(filename)

    repository = JsonRepository(filename)
    f1 = Film('1',
              '1',
              1,
              1.0,
              'da')
    repository.create(f1)
    all = repository.read()
    assert all[-1] == f1
