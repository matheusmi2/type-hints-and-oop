from pathlib import Path

from src.core.excecoes import ZoologicoErro
from src.repositorios.json_repository import RepositorioJSON
from src.servicos.zoologico import SistemaZoologico


def exibir_menu() -> None:
    print("\n=== Zoologico ===")
    print("1. Cadastrar recinto")
    print("2. Cadastrar animal")
    print("3. Cadastrar tratador")
    print("4. Listar dados")
    print("5. Agendar atividade")
    print("6. Executar proxima atividade")
    print("7. Exibir relatorio do administrador")
    print("8. Popular dados de exemplo")
    print("9. Salvar dados")
    print("0. Sair")


def escolher_tipo_atividade() -> str:
    print("\nTipos de atividade:")
    print("1. alimentacao")
    print("2. tratamento")
    print("3. limpeza")
    print("4. banho_de_sol")

    # Converte o número para o tipo da atividade.
    opcoes = {
        "1": "alimentacao",
        "2": "tratamento",
        "3": "limpeza",
        "4": "banho_de_sol",
    }
    escolha = input("Escolha o tipo: ").strip()
    return opcoes.get(escolha, "")


def listar_dados(sistema: SistemaZoologico) -> None:
    # Separa a listagem por blocos.
    print("\n--- Recintos ---")
    if not sistema.recintos:
        print("Nenhum recinto cadastrado.")
    for recinto in sistema.listar_recintos():
        print(
            f"{recinto.codigo} | {recinto.nome} | capacidade: {recinto.capacidade} "
            f"| animais: {len(recinto.animais)} | limpo: {'sim' if recinto.limpo else 'nao'}"
        )

    print("\n--- Animais ---")
    if not sistema.animais:
        print("Nenhum animal cadastrado.")
    for animal in sistema.listar_animais():
        print(
            f"{animal.codigo} | {animal.nome} | especie: {animal.tipo} | "
            f"idade: {animal.idade} | recinto: {animal.recinto_codigo}"
        )

    print("\n--- Tratadores ---")
    if not sistema.tratadores:
        print("Nenhum tratador cadastrado.")
    for tratador in sistema.listar_tratadores():
        print(
            f"{tratador.codigo} | {tratador.nome} | categoria: {tratador.categoria} | "
            f"turno: {tratador.turno} | atividades: {tratador.atividades_realizadas}"
        )

    print(f"\nAtividades pendentes na fila: {len(sistema.fila_atividades)}")


def cadastrar_recinto(sistema: SistemaZoologico) -> None:
    codigo = input("Codigo do recinto: ").strip()
    nome = input("Nome do recinto: ").strip()
    capacidade = int(input("Capacidade do recinto: ").strip())
    sistema.cadastrar_recinto(codigo, nome, capacidade)
    print("Recinto cadastrado com sucesso.")


def cadastrar_animal(sistema: SistemaZoologico) -> None:
    print("\nEspecies disponiveis:", ", ".join(sistema.especies_disponiveis()))
    especie = input("Especie: ").strip().lower()
    codigo = input("Codigo do animal: ").strip()
    nome = input("Nome do animal: ").strip()
    idade = int(input("Idade: ").strip())
    recinto_codigo = input("Codigo do recinto: ").strip()
    sistema.cadastrar_animal(especie, codigo, nome, idade, recinto_codigo)
    print("Animal cadastrado com sucesso.")


def cadastrar_tratador(sistema: SistemaZoologico) -> None:
    print("\nCategorias disponiveis: geral, especialista")
    categoria = input("Categoria do tratador: ").strip().lower()
    codigo = input("Codigo do tratador: ").strip()
    nome = input("Nome do tratador: ").strip()
    turno = input("Turno (manha/tarde/noite): ").strip().lower()
    especialidades: list[str] = []

    if categoria == "especialista":
        # Lê as especialidades separadas por vírgula.
        texto = input("Especialidades separadas por virgula: ").strip()
        especialidades = [item.strip().lower() for item in texto.split(",") if item.strip()]

    sistema.cadastrar_tratador(categoria, codigo, nome, turno, especialidades)
    print("Tratador cadastrado com sucesso.")


def agendar_atividade(sistema: SistemaZoologico) -> None:
    tipo = escolher_tipo_atividade()
    if not tipo:
        print("Tipo de atividade invalido.")
        return

    tratador_codigo = input("Codigo do tratador: ").strip()
    horario = input("Horario planejado (ex: 08:00): ").strip()
    animal_codigo = None
    recinto_codigo = None

    if tipo in {"alimentacao", "tratamento", "banho_de_sol"}:
        animal_codigo = input("Codigo do animal: ").strip()
    if tipo == "limpeza":
        recinto_codigo = input("Codigo do recinto: ").strip()

    atividade = sistema.agendar_atividade(
        tipo=tipo,
        tratador_codigo=tratador_codigo,
        horario=horario,
        animal_codigo=animal_codigo,
        recinto_codigo=recinto_codigo,
    )
    print(f"Atividade agendada: {atividade.descricao}")


def executar() -> None:
    # Mantém o menu rodando até a saída.
    base_dados = Path(__file__).resolve().parents[1] / "dados"
    repositorio = RepositorioJSON(base_dados)
    sistema = SistemaZoologico(repositorio)
    sistema.carregar_dados()

    while True:
        try:
            exibir_menu()
            opcao = input("Escolha uma opcao: ").strip()

            if opcao == "1":
                cadastrar_recinto(sistema)
            elif opcao == "2":
                cadastrar_animal(sistema)
            elif opcao == "3":
                cadastrar_tratador(sistema)
            elif opcao == "4":
                listar_dados(sistema)
            elif opcao == "5":
                agendar_atividade(sistema)
            elif opcao == "6":
                atividade = sistema.executar_proxima_atividade()
                print(f"Atividade concluida: {atividade.resultado}")
            elif opcao == "7":
                print("\n" + sistema.gerar_relatorio_administrador())
            elif opcao == "8":
                sistema.popular_dados_exemplo()
                print("Dados de exemplo carregados com sucesso.")
            elif opcao == "9":
                sistema.salvar_dados()
                print("Dados salvos com sucesso.")
            elif opcao == "0":
                sistema.salvar_dados()
                print("Encerrando o sistema.")
                break
            else:
                print("Opcao invalida.")
        except ValueError:
            print("Entrada invalida. Verifique se voce digitou numeros nos campos corretos.")
        except ZoologicoErro as erro:
            print(f"Erro: {erro}")
