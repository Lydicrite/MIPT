class City:
    __max_count = 100
    __free_city_space = 100
    __cur_count = 0

    def __init__(self, name: str, count: int):
        if count < 0:
            raise ValueError("City capacity cannot be negative")

        capacity = min(count, City.__free_city_space)
        self._name = name
        self._max_count = capacity
        self._cur_count = 0
        City.__free_city_space -= capacity

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._max_count

    @property
    def population(self) -> int:
        return self._cur_count

    @property
    def available_places(self) -> int:
        return self._max_count - self._cur_count

    def add_person(self) -> bool:
        if self.available_places == 0:
            return False
        self._cur_count += 1
        City.__cur_count += 1
        return True

    def remove_person(self) -> bool:
        if self._cur_count == 0:
            return False
        self._cur_count -= 1
        City.__cur_count -= 1
        return True

    def __str__(self) -> str:
        return (
            "------------------------\n"
            "City: {}\n"
            "Capacity: {}\n"
            "Population: {}\n"
            "Available places: {}\n"
            "{}"
        ).format(
            self._name,
            self._max_count,
            self._cur_count,
            self.available_places,
            self.info(),
        )

    @classmethod
    def info(cls) -> str:
        return (
            "------------------------\n"
            "Agglomeration:\n"
            "Max population: {}\n"
            "Unallocated city capacity: {}\n"
            "Resident count: {}\n"
        ).format(cls.__max_count, cls.__free_city_space, cls.__cur_count)

    @staticmethod
    def global_info() -> str:
        return "no additional information"
