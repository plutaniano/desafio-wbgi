from src.last_lines import last_lines
from tests import ARTIFACTS


def test_example():
    path = ARTIFACTS / "last_lines_example.txt"
    assert list(last_lines(path, 2)) == [
        "And this is line 3\n",
        "This is line 2\n",
        "This is a file\n",
    ]


def test_empty_file():
    path = ARTIFACTS / "empty_file.txt"
    assert list(last_lines(path)) == ["\n"]


def test_some_empty_lines():
    path = ARTIFACTS / "some_empty_lines.txt"
    assert list(last_lines(path)) == ["5\n", "4\n", "\n", "\n", "1\n"]


def test_unaligned_utf8():
    path = ARTIFACTS / "unaligned_utf8.txt"

    for i in range(1, 6):
        assert list(last_lines(path, i)) == ["a\n", "🗿\n"]
