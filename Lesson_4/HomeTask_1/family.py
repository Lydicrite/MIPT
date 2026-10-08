from person import Child, FamilyMember, masculine_surname


class Family:
    def __init__(
        self,
        surname: str,
        father: FamilyMember,
        mother: FamilyMember | None = None,
    ):
        if not surname.strip():
            raise ValueError("Family surname cannot be empty")

        self._surname = masculine_surname(surname)
        self._father = father
        self._mother = mother
        self._children: list[Child] = []

        self._father.set_family_role("father")
        self._father.start_new_branch(self._surname)
        if self._mother is not None:
            self._mother.set_family_role("mother")
            self._mother.start_new_branch(self._surname)

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def members(self) -> tuple[FamilyMember, ...]:
        parents = (
            (self._father, self._mother)
            if self._mother is not None
            else (self._father,)
        )
        return parents + tuple(self._children)

    def add_child(
        self,
        name: str,
        gender: str = "male",
        middle_name: str | None = None,
        branch_surname: str | None = None,
    ) -> Child:
        surname = branch_surname or self._surname
        child = Child(
            name=name,
            surname=surname,
            father=self._father,
            gender=gender,
            middle_name=middle_name,
        )
        self._children.append(child)
        return child

    def __len__(self) -> int:
        return len(self.members)

    def __str__(self) -> str:
        lines = ["Family {}:".format(self._surname)]
        lines.extend("  - {}".format(member) for member in self.members)
        return "\n".join(lines)
