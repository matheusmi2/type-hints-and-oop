from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.excecoes import OperacaoInvalidaErro


class Animal(ABC):
    def __init__(self, codigo: str, nome: str, idade: int, recinto_codigo: str, precisa_banho_sol: bool):
        # Padroniza o código em maiúsculo.
        self._codigo = codigo.strip().upper()
        self.nome = nome
        self.idade = idade
        self._recinto_codigo = recinto_codigo.strip().upper()
        self._precisa_banho_sol = precisa_banho_sol

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise OperacaoInvalidaErro("O nome do animal nao pode ficar vazio.")
        self._nome = valor.strip().title()

    @property
    def idade(self) -> int:
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        if valor < 0:
            raise OperacaoInvalidaErro("A idade do animal nao pode ser negativa.")
        self._idade = valor

    @property
    def recinto_codigo(self) -> str:
        return self._recinto_codigo

    @property
    def tipo(self) -> str:
        # Usa o nome da classe como espécie.
        return self.__class__.__name__.lower()

    @property
    def precisa_banho_sol(self) -> bool:
        return self._precisa_banho_sol

    @abstractmethod
    def descricao_alimentacao(self) -> str:
        # Define a alimentação da espécie.
        pass

    @abstractmethod
    def descricao_tratamento(self) -> str:
        # Define o tratamento da espécie.
        pass

    def alimentar(self) -> str:
        return f"{self.nome} recebeu {self.descricao_alimentacao()}."

    def tratar(self) -> str:
        return f"{self.nome} recebeu {self.descricao_tratamento()}."

    def tomar_banho_de_sol(self) -> str:
        if not self.precisa_banho_sol:
            raise OperacaoInvalidaErro(f"{self.nome} nao precisa de banho de sol hoje.")
        return f"{self.nome} tomou banho de sol no horario planejado."

    def to_dict(self) -> dict:
        # Converte o objeto para salvar em JSON.
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "idade": self.idade,
            "recinto_codigo": self.recinto_codigo,
            "especie": self.tipo,
        }
