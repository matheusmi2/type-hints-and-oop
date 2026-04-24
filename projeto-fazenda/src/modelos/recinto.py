from src.core.excecoes import CapacidadeRecintoErro, OperacaoInvalidaErro


class Recinto:
    def __init__(self, codigo: str, nome: str, capacidade: int, animais: list[str] | None = None, limpo: bool = True):
        self._codigo = codigo.strip().upper()
        self.nome = nome
        self.capacidade = capacidade
        self._animais = [animal.upper() for animal in (animais or [])]
        self._limpo = limpo

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise OperacaoInvalidaErro("O nome do recinto nao pode ficar vazio.")
        self._nome = valor.strip().title()

    @property
    def capacidade(self) -> int:
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor: int) -> None:
        if valor <= 0:
            raise OperacaoInvalidaErro("A capacidade do recinto deve ser maior que zero.")
        self._capacidade = valor

    @property
    def animais(self) -> list[str]:
        return list(self._animais)

    @property
    def limpo(self) -> bool:
        return self._limpo

    def adicionar_animal(self, animal_codigo: str) -> None:
        # Impede exceder a capacidade.
        if len(self._animais) >= self.capacidade:
            raise CapacidadeRecintoErro("O recinto atingiu a capacidade maxima.")
        self._animais.append(animal_codigo.upper())

    def remover_animal(self, animal_codigo: str) -> None:
        codigo = animal_codigo.upper()
        if codigo in self._animais:
            self._animais.remove(codigo)

    def marcar_como_sujo(self) -> None:
        # Marca o recinto como sujo.
        self._limpo = False

    def limpar(self) -> str:
        self._limpo = True
        return f"O recinto {self.nome} foi limpo."

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "animais": self.animais,
            "limpo": self.limpo,
        }
