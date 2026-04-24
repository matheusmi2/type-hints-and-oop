from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.excecoes import OperacaoInvalidaErro
from src.modelos.animal import Animal


class Tratador(ABC):
    def __init__(self, codigo: str, nome: str, turno: str):
        self._codigo = codigo.strip().upper()
        self.nome = nome
        self.turno = turno
        # Guarda as atividades pendentes.
        self._cronograma: list[str] = []
        self._atividades_realizadas = 0

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise OperacaoInvalidaErro("O nome do tratador nao pode ficar vazio.")
        self._nome = valor.strip().title()

    @property
    def turno(self) -> str:
        return self._turno

    @turno.setter
    def turno(self, valor: str) -> None:
        turno_normalizado = valor.strip().lower()
        if turno_normalizado not in {"manha", "tarde", "noite"}:
            raise OperacaoInvalidaErro("O turno deve ser manha, tarde ou noite.")
        self._turno = turno_normalizado

    @property
    def atividades_realizadas(self) -> int:
        return self._atividades_realizadas

    @property
    def cronograma(self) -> list[str]:
        return list(self._cronograma)

    @property
    def categoria(self) -> str:
        return self.__class__.__name__.replace("Tratador", "").lower() or "base"

    def adicionar_ao_cronograma(self, descricao: str) -> None:
        self._cronograma.append(descricao)

    def registrar_atividade(self, descricao: str) -> None:
        # Soma a atividade e remove do cronograma.
        self._atividades_realizadas += 1
        if descricao in self._cronograma:
            self._cronograma.remove(descricao)

    def restaurar_estado(self, atividades_realizadas: int, cronograma: list[str]) -> None:
        # Restaura o estado ao carregar do arquivo.
        self._atividades_realizadas = atividades_realizadas
        self._cronograma = list(cronograma)

    @abstractmethod
    def pode_cuidar(self, animal: Animal) -> bool:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class TratadorGeral(Tratador):
    def pode_cuidar(self, animal: Animal) -> bool:
        # Pode cuidar de qualquer espécie.
        return True

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "turno": self.turno,
            "categoria": "geral",
            "atividades_realizadas": self.atividades_realizadas,
            "cronograma": self.cronograma,
        }


class TratadorEspecialista(Tratador):
    def __init__(self, codigo: str, nome: str, turno: str, especialidades: list[str]):
        super().__init__(codigo, nome, turno)
        if not especialidades:
            raise OperacaoInvalidaErro("O tratador especialista precisa de ao menos uma especialidade.")
        self._especialidades = [item.strip().lower() for item in especialidades]

    @property
    def especialidades(self) -> list[str]:
        return list(self._especialidades)

    def pode_cuidar(self, animal: Animal) -> bool:
        # Só atende espécies da especialidade.
        return animal.tipo in self._especialidades

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "turno": self.turno,
            "categoria": "especialista",
            "especialidades": self.especialidades,
            "atividades_realizadas": self.atividades_realizadas,
            "cronograma": self.cronograma,
        }


def criar_tratador(
    categoria: str,
    codigo: str,
    nome: str,
    turno: str,
    especialidades: list[str] | None = None,
) -> Tratador:
    # Escolhe o tipo de tratador.
    categoria = categoria.lower()
    if categoria == "geral":
        return TratadorGeral(codigo, nome, turno)
    if categoria == "especialista":
        return TratadorEspecialista(codigo, nome, turno, especialidades or [])
    raise OperacaoInvalidaErro("Categoria de tratador invalida.")
