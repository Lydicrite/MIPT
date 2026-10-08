from city_list import CityList
from family import Family
from person import FamilyMember, Person


def person_test() -> None:
    print(Person("Ivan", "Ivanov", "Ivanovich"))


def city_list_test() -> None:
    city = CityList("Small city", 3)
    city.add_person(Person("Ivan", "Ivanov", "Ivanovich"))
    city.add_person(Person("Petr", "Petrov", "Petrovich"))
    print(city)


def family_test() -> None:
    city = CityList("Family city", 10)

    father = FamilyMember(
        "Aleksandr", "Petrov", "Ivanovich", role="father"
    )
    mother = FamilyMember(
        "Elena",
        "Sidorova",
        "Pavlovna",
        role="mother",
        gender="female",
    )
    family = Family("Petrov", father, mother)

    family.add_child("Mikhail")
    family.add_child("Anna", gender="female")
    family.add_child(
        "Olga",
        gender="female",
        branch_surname="Smirnova",
    )

    if city.add_family(family):
        print("The family was settled successfully.\n")
    else:
        print("There is not enough room for the family.\n")

    print(family)
    print()
    print(city)


if __name__ == "__main__":
    family_test()
