from __future__ import annotations

from collections import deque

from src.core.excecoes import (
    EntidadeJaExisteErro,
    EntidadeNaoEncontradaErro,
    OperacaoInvalidaErro,
)
from src.modelos.administrador import Administrador
from src.modelos.animal import Animal
from src.modelos.atividade import Atividade
from src.modelos.especies import ESPECIES_DISPONIVEIS, criar_animal
from src.modelos.recinto import Recinto
from src.modelos.tratador import Tratador, criar_tratador
from src.repositorios.json_repository import RepositorioJSON


class SistemaZoologico:
    def __init__(self, repositorio: RepositorioJSON):
        self.repositorio = repositorio
        self.animais: dict[str, Animal] = {}
        self.tratadores: dict[str, Tratador] = {}
        self.recintos: dict[str, Recinto] = {}
        # Mantém a ordem das tarefas agendadas.
        self.fila_atividades: deque[Atividade] = deque()
        self.historico_atividades: list[Atividade] = []
        self.administrador = Administrador("Administrador do Zoologico")

    def especies_disponiveis(self) -> list[str]:
        return sorted(ESPECIES_DISPONIVEIS.keys())

    def listar_animais(self) -> list[Animal]:
        return sorted(self.animais.values(), key=lambda animal: animal.codigo)

    def listar_tratadores(self) -> list[Tratador]:
        return sorted(self.tratadores.values(), key=lambda tratador: tratador.codigo)

    def listar_recintos(self) -> list[Recinto]:
        return sorted(self.recintos.values(), key=lambda recinto: recinto.codigo)

    def cadastrar_recinto(self, codigo: str, nome: str, capacidade: int) -> Recinto:
        codigo = codigo.strip().upper()
        if codigo in self.recintos:
            raise EntidadeJaExisteErro("Ja existe um recinto com esse codigo.")

        recinto = Recinto(codigo, nome, capacidade)
        self.recintos[recinto.codigo] = recinto
        return recinto

    def cadastrar_animal(
        self,
        especie: str,
        codigo: str,
        nome: str,
        idade: int,
        recinto_codigo: str,
    ):
        codigo = codigo.strip().upper()
        recinto = self._buscar_recinto(recinto_codigo)

        if codigo in self.animais:
            raise EntidadeJaExisteErro("Ja existe um animal com esse codigo.")

        # Só cadastra se houver recinto com espaço.
        animal = criar_animal(especie, codigo, nome, idade, recinto.codigo)
        recinto.adicionar_animal(animal.codigo)
        self.animais[animal.codigo] = animal
        return animal

    def cadastrar_tratador(
        self,
        categoria: str,
        codigo: str,
        nome: str,
        turno: str,
        especialidades: list[str] | None = None,
    ) -> Tratador:
        codigo = codigo.strip().upper()
        if codigo in self.tratadores:
            raise EntidadeJaExisteErro("Ja existe um tratador com esse codigo.")

        tratador = criar_tratador(categoria, codigo, nome, turno, especialidades)
        self.tratadores[tratador.codigo] = tratador
        return tratador

    def agendar_atividade(
        self,
        tipo: str,
        tratador_codigo: str,
        horario: str,
        animal_codigo: str | None = None,
        recinto_codigo: str | None = None,
    ) -> Atividade:
        tratador = self._buscar_tratador(tratador_codigo)
        animal = None
        recinto = None

        # Essas atividades precisam de um animal.
        if tipo in {"alimentacao", "tratamento", "banho_de_sol"}:
            if not animal_codigo:
                raise OperacaoInvalidaErro("Essa atividade precisa de um animal.")
            animal = self._buscar_animal(animal_codigo)
            if not tratador.pode_cuidar(animal):
                raise OperacaoInvalidaErro(
                    "Esse tratador nao pode cuidar desse animal."
                )
            if tipo == "banho_de_sol" and not animal.precisa_banho_sol:
                raise OperacaoInvalidaErro("Esse animal nao precisa de banho de sol.")

        if tipo == "limpeza":
            if not recinto_codigo:
                raise OperacaoInvalidaErro("A limpeza precisa de um recinto.")
            recinto = self._buscar_recinto(recinto_codigo)

        # Gera um código simples para a atividade.
        codigo_atividade = (
            f"ATV-{len(self.fila_atividades) + len(self.historico_atividades) + 1:03d}"
        )
        descricao = self._montar_descricao(
            tipo, tratador.codigo, animal, recinto, horario
        )
        atividade = Atividade(
            codigo=codigo_atividade,
            tipo=tipo,
            tratador_codigo=tratador.codigo,
            horario=horario,
            descricao=descricao,
            animal_codigo=animal.codigo if animal else None,
            recinto_codigo=recinto.codigo if recinto else None,
        )

        self.fila_atividades.append(atividade)
        tratador.adicionar_ao_cronograma(descricao)
        return atividade

    def executar_proxima_atividade(self) -> Atividade:
        if not self.fila_atividades:
            raise OperacaoInvalidaErro("Nao ha atividades pendentes na fila.")

        # Executa a atividade mais antiga da fila.
        atividade = self.fila_atividades.popleft()
        tratador = self._buscar_tratador(atividade.tratador_codigo)
        resultado = ""

        if atividade.tipo == "limpeza":
            recinto = self._buscar_recinto(atividade.recinto_codigo or "")
            resultado = recinto.limpar()
        else:
            animal = self._buscar_animal(atividade.animal_codigo or "")
            recinto = self._buscar_recinto(animal.recinto_codigo)

            if not tratador.pode_cuidar(animal):
                raise OperacaoInvalidaErro(
                    "O tratador nao tem permissao para essa atividade."
                )

            if atividade.tipo == "alimentacao":
                resultado = animal.alimentar()
                recinto.marcar_como_sujo()
            elif atividade.tipo == "tratamento":
                resultado = animal.tratar()
                recinto.marcar_como_sujo()
            elif atividade.tipo == "banho_de_sol":
                resultado = animal.tomar_banho_de_sol()
            else:
                raise OperacaoInvalidaErro("Tipo de atividade invalido.")

        tratador.registrar_atividade(atividade.descricao)
        atividade.concluir(resultado)
        self.historico_atividades.append(atividade)
        return atividade

    def gerar_relatorio_administrador(self) -> str:
        return self.administrador.gerar_relatorio(
            self.historico_atividades, self.tratadores
        )

    def salvar_dados(self) -> None:
        # Salva cada grupo em um arquivo.
        self.repositorio.salvar(
            "animais.json", [animal.to_dict() for animal in self.animais.values()]
        )
        self.repositorio.salvar(
            "tratadores.json",
            [tratador.to_dict() for tratador in self.tratadores.values()],
        )
        self.repositorio.salvar(
            "recintos.json", [recinto.to_dict() for recinto in self.recintos.values()]
        )
        self.repositorio.salvar(
            "fila_atividades.json",
            [atividade.to_dict() for atividade in self.fila_atividades],
        )
        self.repositorio.salvar(
            "historico_atividades.json",
            [atividade.to_dict() for atividade in self.historico_atividades],
        )

    def carregar_dados(self) -> None:
        # Limpa a memória antes de recarregar.
        self.animais.clear()
        self.tratadores.clear()
        self.recintos.clear()
        self.fila_atividades.clear()
        self.historico_atividades.clear()

        for dados_recinto in self.repositorio.carregar("recintos.json"):
            recinto = Recinto(
                codigo=dados_recinto["codigo"],
                nome=dados_recinto["nome"],
                capacidade=dados_recinto["capacidade"],
                animais=dados_recinto.get("animais", []),
                limpo=dados_recinto.get("limpo", True),
            )
            self.recintos[recinto.codigo] = recinto

        for dados_animal in self.repositorio.carregar("animais.json"):
            animal = criar_animal(
                especie=dados_animal["especie"],
                codigo=dados_animal["codigo"],
                nome=dados_animal["nome"],
                idade=dados_animal["idade"],
                recinto_codigo=dados_animal["recinto_codigo"],
            )
            self.animais[animal.codigo] = animal

        for dados_tratador in self.repositorio.carregar("tratadores.json"):
            tratador = criar_tratador(
                categoria=dados_tratador["categoria"],
                codigo=dados_tratador["codigo"],
                nome=dados_tratador["nome"],
                turno=dados_tratador["turno"],
                especialidades=dados_tratador.get("especialidades", []),
            )
            tratador.restaurar_estado(
                atividades_realizadas=dados_tratador.get("atividades_realizadas", 0),
                cronograma=dados_tratador.get("cronograma", []),
            )
            self.tratadores[tratador.codigo] = tratador

        for dados_atividade in self.repositorio.carregar("fila_atividades.json"):
            self.fila_atividades.append(Atividade.from_dict(dados_atividade))

        for dados_atividade in self.repositorio.carregar("historico_atividades.json"):
            self.historico_atividades.append(Atividade.from_dict(dados_atividade))

    def popular_dados_exemplo(self) -> None:
        # Carrega dados prontos para teste.
        self.animais.clear()
        self.tratadores.clear()
        self.recintos.clear()
        self.fila_atividades.clear()
        self.historico_atividades.clear()

        self.cadastrar_recinto("R1", "Savana", 3)
        self.cadastrar_recinto("R2", "Floresta", 4)
        self.cadastrar_recinto("R3", "Polo", 2)

        self.cadastrar_animal("leao", "A1", "Simba", 5, "R1")
        self.cadastrar_animal("elefante", "A2", "Dumbo", 12, "R1")
        self.cadastrar_animal("macaco", "A3", "Kiko", 3, "R2")
        self.cadastrar_animal("pinguim", "A4", "Lolo", 4, "R3")

        self.cadastrar_tratador("geral", "T1", "Marina", "manha")
        self.cadastrar_tratador(
            "especialista", "T2", "Carlos", "tarde", ["leao", "elefante"]
        )
        self.cadastrar_tratador(
            "especialista", "T3", "Bianca", "manha", ["macaco", "pinguim"]
        )

    def _buscar_animal(self, codigo: str):
        codigo = codigo.strip().upper()
        if codigo not in self.animais:
            raise EntidadeNaoEncontradaErro("Animal nao encontrado.")
        return self.animais[codigo]

    def _buscar_tratador(self, codigo: str) -> Tratador:
        codigo = codigo.strip().upper()
        if codigo not in self.tratadores:
            raise EntidadeNaoEncontradaErro("Tratador nao encontrado.")
        return self.tratadores[codigo]

    def _buscar_recinto(self, codigo: str) -> Recinto:
        codigo = codigo.strip().upper()
        if codigo not in self.recintos:
            raise EntidadeNaoEncontradaErro("Recinto nao encontrado.")
        return self.recintos[codigo]

    def _montar_descricao(
        self, tipo: str, tratador_codigo: str, animal, recinto, horario: str
    ) -> str:
        # Monta a descrição da atividade.
        if tipo == "limpeza" and recinto is not None:
            return (
                f"{tipo} do recinto {recinto.codigo} por {tratador_codigo} as {horario}"
            )
        if animal is not None:
            return (
                f"{tipo} do animal {animal.codigo} por {tratador_codigo} as {horario}"
            )
        return f"{tipo} por {tratador_codigo} as {horario}"
