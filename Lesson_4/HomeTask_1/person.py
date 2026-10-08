# Мужская фамилия из женской
def masculine_surname(surname: str) -> str:
    surname = surname.strip()
    lower_surname = surname.lower()

    if lower_surname.endswith("skaya"):
        return surname[:-5] + "skiy"
    if lower_surname.endswith(("ova", "eva", "ina")):
        return surname[:-1]
    if lower_surname.endswith("aya"):
        return surname[:-3] + "iy"
    return surname

# Фамилия по полу
def surname_for_gender(surname: str, gender: str) -> str:
    if gender not in ("male", "female"):
        raise ValueError("Gender must be 'male' or 'female'")

    masculine = masculine_surname(surname)
    if gender == "male":
        return masculine

    lower_surname = masculine.lower()
    if lower_surname.endswith(("ov", "ev", "in")):
        return masculine + "a"
    if lower_surname.endswith("skiy"):
        return masculine[:-4] + "skaya"
    if lower_surname.endswith("sky"):
        return masculine[:-3] + "skaya"
    if lower_surname.endswith("iy"):
        return masculine[:-2] + "aya"
    return masculine


class Person:
    def __init__(
        self,
        name: str = "Ivan",
        surname: str = "Ivanov",
        middle_name: str = "Ivanovich",
    ):
        self._name = name
        self._surname = surname
        self._middle_name = middle_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def middle_name(self) -> str:
        return self._middle_name

    @property
    def full_name(self) -> str:
        return "{} {} {}".format(
            self._surname, self._name, self._middle_name
        ).strip()

    def __str__(self) -> str:
        return self.full_name


# Член семьи
class FamilyMember(Person):
    def __init__(
        self,
        name: str,
        surname: str,
        middle_name: str = "",
        role: str = "relative",
        gender: str | None = None,
    ):
        if gender is None:
            gender = "female" if role in ("mother", "daughter") else "male"
        if gender not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")

        super().__init__(name, surname, middle_name)
        self._role = role
        self._gender = gender
        self.start_new_branch(surname)

    @property
    def role(self) -> str:
        return self._role

    @property
    def gender(self) -> str:
        return self._gender

    def set_family_role(self, role: str) -> None:
        if not role.strip():
            raise ValueError("Family role cannot be empty")
        self._role = role.strip()

    def start_new_branch(self, surname: str) -> None:
        if not surname.strip():
            raise ValueError("Branch surname cannot be empty")
        self._surname = surname_for_gender(surname, self._gender)

    def __str__(self) -> str:
        return "{} ({})".format(super().__str__(), self._role)

# Ребёнок
class Child(FamilyMember):
    def __init__(
        self,
        name: str,
        surname: str,
        father: FamilyMember | None = None,
        gender: str = "male",
        middle_name: str | None = None,
    ):
        if gender not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")

        if middle_name is None:
            if father is None:
                raise ValueError(
                    "Father is required when middle_name is not specified"
                )
            middle_name = self.make_patronymic(father.name, gender)

        super().__init__(
            name,
            surname,
            middle_name,
            role="child",
            gender=gender,
        )

    # Создание отчества
    @staticmethod
    def make_patronymic(father_name: str, gender: str) -> str:
        exceptions = {
            "Pavel": ("Pavlovich", "Pavlovna"),
            "Ilya": ("Ilyich", "Ilyinichna"),
            "Lev": ("Lvovich", "Lvovna"),
        }
        if father_name in exceptions:
            return exceptions[father_name][gender == "female"]

        if father_name.endswith(("y", "i")):
            stem = father_name[:-1]
            endings = ("evich", "evna")
        elif father_name.endswith("a"):
            stem = father_name[:-1]
            endings = ("ich", "ichna")
        else:
            stem = father_name
            endings = ("ovich", "ovna")

        return stem + endings[gender == "female"]
