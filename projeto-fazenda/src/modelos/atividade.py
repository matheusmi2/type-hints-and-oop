from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Atividade:
    # Registro simples da tarefa.
    codigo: str
    tipo: str
    tratador_codigo: str
    horario: str
    descricao: str
    animal_codigo: str | None = None
    recinto_codigo: str | None = None
    status: str = "pendente"
    resultado: str = ""

    def concluir(self, resultado: str) -> None:
        self.status = "concluida"
        self.resultado = resultado

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "tratador_codigo": self.tratador_codigo,
            "horario": self.horario,
            "descricao": self.descricao,
            "animal_codigo": self.animal_codigo,
            "recinto_codigo": self.recinto_codigo,
            "status": self.status,
            "resultado": self.resultado,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Atividade":
        return cls(
            codigo=dados["codigo"],
            tipo=dados["tipo"],
            tratador_codigo=dados["tratador_codigo"],
            horario=dados["horario"],
            descricao=dados["descricao"],
            animal_codigo=dados.get("animal_codigo"),
            recinto_codigo=dados.get("recinto_codigo"),
            status=dados.get("status", "pendente"),
            resultado=dados.get("resultado", ""),
        )
