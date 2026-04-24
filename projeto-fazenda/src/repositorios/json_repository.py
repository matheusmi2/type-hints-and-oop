import json
from pathlib import Path


class RepositorioJSON:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def salvar(self, nome_arquivo: str, dados: list[dict]) -> None:
        # Salva os dados no arquivo JSON.
        caminho = self.base_path / nome_arquivo
        with caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def carregar(self, nome_arquivo: str) -> list[dict]:
        caminho = self.base_path / nome_arquivo
        if not caminho.exists():
            # Retorna lista vazia se o arquivo não existir.
            return []
        with caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
