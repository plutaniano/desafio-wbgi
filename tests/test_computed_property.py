from src.computed_property import computed_property


class Circle:
    def __init__(self, radius: float = 1) -> None:
        self.radius = radius
        self.call_count = 0

    @computed_property("radius")
    def diameter(self) -> float:
        "my docstring"

        self.call_count += 1
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter: float) -> None:
        self.radius = diameter / 2

    @diameter.deleter
    def diameter(self) -> None:
        self.radius = 0


def test_getter() -> None:
    circle = Circle()
    assert circle.diameter == 2


def test_setter() -> None:
    circle = Circle()
    circle.diameter = 3
    assert circle.radius == 1.5


def test_deleter() -> None:
    circle = Circle()
    assert circle.radius == 1

    del circle.diameter
    assert circle.diameter == 0


def test_cache_hit() -> None:
    circle = Circle()
    circle.diameter

    before = circle.call_count
    for _ in range(10):
        circle.diameter

    assert before == circle.call_count


def test_cache_miss() -> None:
    circle = Circle()

    circle.diameter  # call_count = 1
    circle.radius = 5
    circle.diameter  # call_count = 2

    assert circle.call_count == 2


def test_docstring_is_preserved() -> None:
    Circle().diameter.__doc__ == "my docstring"


def test_missing_attr_is_ignored() -> None:
    import time

    class Thing:
        @computed_property("missing_attr")
        def do_the_thing(self) -> int:
            return time.time_ns()

    thing = Thing()
    value1 = thing.do_the_thing
    value2 = thing.do_the_thing

    thing.missing_attr = ":)"
    value3 = thing.do_the_thing

    assert value1 == value2
    assert value1 != value3
