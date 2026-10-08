from city import City
from family import Family
from person import Person


class CityList(City):
    def __init__(self, name: str, count: int):
        super().__init__(name, count)
        self.__person_list: list[Person] = []
        self.__family_list: list[Family] = []

    @property
    def residents(self) -> tuple[Person, ...]:
        return tuple(self.__person_list)

    @property
    def families(self) -> tuple[Family, ...]:
        return tuple(self.__family_list)

    def add_person(self, person: Person | None = None) -> bool:
        if person is None:
            number = len(self.__person_list) + 1
            person = Person("Resident{}".format(number), "Unknown", "")
        if not isinstance(person, Person):
            raise TypeError("Only Person instances can live in a city")

        if not super().add_person():
            return False
        self.__person_list.append(person)
        return True

    def add_family(self, family: Family) -> bool:
        if not isinstance(family, Family):
            raise TypeError("family must be a Family instance")
        if family in self.__family_list:
            return False
        if len(family) > self.available_places:
            return False
        if any(member in self.__person_list for member in family.members):
            return False

        for member in family.members:
            self.add_person(member)
        self.__family_list.append(family)
        return True

    def remove_person(self, index: int) -> bool:
        if not self.__person_list:
            return False

        index %= len(self.__person_list)
        person = self.__person_list[index]
        if any(person in family.members for family in self.__family_list):
            return False

        if not super().remove_person():
            return False
        del self.__person_list[index]
        return True

    def remove_family(self, family: Family) -> bool:
        if family not in self.__family_list:
            return False

        for member in family.members:
            self.__person_list.remove(member)
            super().remove_person()
        self.__family_list.remove(family)
        return True

    def __str__(self) -> str:
        lines = [super().__str__(), "Residents:"]
        if not self.__person_list:
            lines.append("  (none)")
        else:
            lines.extend(
                "  {}. {}".format(index, person)
                for index, person in enumerate(self.__person_list)
            )

        lines.append("Families: {}".format(len(self.__family_list)))
        return "\n".join(lines)
