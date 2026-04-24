# Projeto Final de POO - Zoológico

Este projeto foi desenvolvido em Python para simular o controle básico de um zoológico. A ideia do trabalho foi aplicar os principais conceitos de POO de uma forma organizada.
O sistema permite cadastrar animais, tratadores e recintos, agendar atividades do dia a dia e gerar um relatório simples para o administrador acompanhar o que foi feito

## Objetivo do projeto

O foco do sistema é ajudar no controle de tarefas comuns de um zoológico, por exemplo:

- alimentação dos animais
- tratamento
- limpeza dos recintos
- banho de sol
- acompanhamento das atividades realizadas

O projeto também trabalha com gravação e leitura de arquivos, para os dados poderem ser salvos em JSON.

## Conceitos de POO usados

- Classes e objetos: `Animal`, `Tratador`, `Recinto`, `Atividade` e `Administrador`
- Herança: espécies como `Leão`, `Macaco`, `Elefante` e `Pinguim` herdam de `Animal`
- Polimorfismo: cada espécie possui sua própria forma de alimentação e tratamento
- Encapsulamento: alguns atributos são controlados por `property`
- Classes abstratas: usadas nas classes base `Animal` e `Tratador`
- Tratamento de exceções: evita cadastros e operações inválidas

## Estruturas de dados usadas

- Lista: histórico de atividades executadas
- Fila: atividades pendentes com `deque`
- Dicionário: armazenamento de animais, tratadores e recintos por código
- Arquivos JSON: persistência dos dados

## Explicação da estrutura

O projeto foi separado em partes simples para facilitar o entendimento:

- `modelos`: contém as classes principais do sistema
- `servicos`: contém as regras do zoológico
- `repositorios`: faz a leitura e a gravação dos arquivos JSON
- `menu.py`: mostra o menu e recebe os dados digitados pelo usuário
- `main.py`: inicia o programa

## Como executar

No terminal, dentro da pasta do projeto, execute:

`python3 main.py`

## O que o sistema faz

Pelo menu é possível:

1. cadastrar recintos
2. cadastrar animais
3. cadastrar tratadores
4. listar os dados cadastrados
5. agendar atividades
6. executar a próxima atividade da fila
7. ver o relatório do administrador
8. carregar dados de exemplo
9. salvar os dados

## Exemplo de passo a passo

Um jeito simples de testar o projeto é o seguinte:

1. Execute `python3 main.py`
2. Escolha a opção `8` para carregar dados de exemplo
3. Escolha a opção `4` para ver os recintos, animais e tratadores cadastrados
4. Escolha a opção `5` para agendar uma atividade
5. Informe o tipo da atividade
   Exemplo: `1` para alimentação
6. Digite o código do tratador
   Exemplo: `T1`
7. Digite o horário
   Exemplo: `08:00`
8. Digite o código do animal
   Exemplo: `A1`
9. Escolha a opção `6` para executar a próxima atividade da fila
10. Escolha a opção `7` para visualizar o relatório
11. Escolha a opção `9` para salvar os dados
12. Escolha a opção `0` para encerrar o sistema
