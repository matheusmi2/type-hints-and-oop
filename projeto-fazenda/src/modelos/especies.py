from src.core.excecoes import OperacaoInvalidaErro
from src.modelos.animal import Animal


class Leao(Animal):
    def __init__(self, codigo: str, nome: str, idade: int, recinto_codigo: str):
        super().__init__(codigo, nome, idade, recinto_codigo, precisa_banho_sol=True)

    def descricao_alimentacao(self) -> str:
        return "carne e suplementos"

    def descricao_tratamento(self) -> str:
        return "avaliacao veterinaria e cuidados com a juba"


class Macaco(Animal):
    def __init__(self, codigo: str, nome: str, idade: int, recinto_codigo: str):
        super().__init__(codigo, nome, idade, recinto_codigo, precisa_banho_sol=True)

    def descricao_alimentacao(self) -> str:
        return "frutas, sementes e verduras"

    def descricao_tratamento(self) -> str:
        return "enriquecimento ambiental e observacao comportamental"


class Elefante(Animal):
    def __init__(self, codigo: str, nome: str, idade: int, recinto_codigo: str):
        super().__init__(codigo, nome, idade, recinto_codigo, precisa_banho_sol=True)

    def descricao_alimentacao(self) -> str:
        return "feno, frutas e vegetais"

    def descricao_tratamento(self) -> str:
        return "hidratacao da pele e avaliacao dos pes"


class Pinguim(Animal):
    def __init__(self, codigo: str, nome: str, idade: int, recinto_codigo: str):
        super().__init__(codigo, nome, idade, recinto_codigo, precisa_banho_sol=False)

    def descricao_alimentacao(self) -> str:
        return "peixes e suplementos vitamicos"

    def descricao_tratamento(self) -> str:
        return "controle termico e avaliacao das penas"


ESPECIES_DISPONIVEIS = {
    "leao": Leao,
    "macaco": Macaco,
    "elefante": Elefante,
    "pinguim": Pinguim,
}


def criar_animal(especie: str, codigo: str, nome: str, idade: int, recinto_codigo: str) -> Animal:
    # Centraliza a criação das espécies.
    classe_animal = ESPECIES_DISPONIVEIS.get(especie.lower())
    if classe_animal is None:
        raise OperacaoInvalidaErro("Especie de animal nao suportada.")
    return classe_animal(codigo, nome, idade, recinto_codigo)
