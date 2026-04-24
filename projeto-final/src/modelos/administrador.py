from collections import Counter

from src.modelos.atividade import Atividade
from src.modelos.tratador import Tratador


class Administrador:
    def __init__(self, nome: str):
        self.nome = nome

    def gerar_relatorio(self, historico: list[Atividade], tratadores: dict[str, Tratador]) -> str:
        if not historico:
            return "Nenhuma atividade foi executada ainda."

        # Conta os dados por tipo e por tratador.
        contador_tipos = Counter(atividade.tipo for atividade in historico)
        contador_tratadores = Counter(atividade.tratador_codigo for atividade in historico)
        animais_tratados = sum(1 for atividade in historico if atividade.tipo == "tratamento")

        linhas = [
            f"Relatorio de {self.nome}",
            f"Total de atividades executadas: {len(historico)}",
            f"Animais tratados: {animais_tratados}",
            "",
            "Atividades por tipo:",
        ]

        for tipo, quantidade in sorted(contador_tipos.items()):
            linhas.append(f"- {tipo}: {quantidade}")

        linhas.append("")
        linhas.append("Atividades por tratador:")
        for codigo, quantidade in sorted(contador_tratadores.items()):
            nome_tratador = tratadores[codigo].nome if codigo in tratadores else codigo
            linhas.append(f"- {nome_tratador} ({codigo}): {quantidade}")

        return "\n".join(linhas)
