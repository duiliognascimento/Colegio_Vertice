import os
import re
import time
import sys
import io
import subprocess  # usado para chamar o gerador de relatórios que está em C


# No Windows, força o terminal a usar UTF-8 (necessário para acentos no programa em C)
if os.name == "nt":
    os.system("chcp 65001 >nul")


def limpar_tela():
    """Limpa o console ou terminal. Usa 'cls' para Windows ('nt') e 'clear' para outros SOs."""
    os.system("cls" if os.name == "nt" else "clear")


def exibir_cabecalho():
    """Exibe o cabeçalho principal do sistema 'COLÉGIO VÉRTICES' no console."""
    print("╔══════════════════════════════════════════╗")
    print("║            COLÉGIO VÉRTICES              ║")
    print("╚══════════════════════════════════════════╝")


def menu_disciplinas():
    """Exibe o menu de opções para a seleção de disciplinas."""
    print("\n=== MENU DE DISCIPLINAS ===")
    print("1 - Matemática")
    print("2 - Português")
    print("3 - História")
    print("4 - Geografia")
    print("5 - Física")
    print("6 - Química")
    print("7 - Biologia")
    print("8 - Artes")
    print("9 - Educação Física")
    print("0 - Voltar")


def normalizar_nome_arquivo(disciplina):
    """
    Normaliza o nome da disciplina para ser usado como nome de arquivo.

    Remove acentos, converte para minúsculas e substitui espaços por underscores.
    Ex: 'Educação Física' -> 'educacao_fisica.txt'

    :param disciplina: Nome completo da disciplina (str).
    :return: Nome do arquivo normalizado com a extensão .txt (str).
    """
    nome = disciplina.lower().replace(" ", "_")

    # Mapeamento para remoção de acentos
    acentos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "â": "a",
        "ê": "e",
        "ô": "o",
        "ã": "a",
        "õ": "o",
        "ç": "c",
    }

    for acento, sem in acentos.items():
        nome = nome.replace(acento, sem)
    
    return f"{nome}.txt"


def validar_semestre():
    """
    Solicita e valida a entrada do semestre no formato 'AAAA/1' ou 'AAAA/2'.

    Continua solicitando até que um formato válido seja inserido.

    :return: Semestre formatado e validado (str).
    """
    while True:
        semestre_str = input("Semestre (AAAA/1 ou AAAA/2): ").strip()
        # Permite que o usuário digite com . ou - e padroniza para /
        semestre_str = semestre_str.replace(".", "/").replace("-", "/")

        if re.match(r"^\d{4}/[12]$", semestre_str):
            return semestre_str
        else:
            print("Formato inválido. Use o formato AAAA/1 ou AAAA/2.")


def validar_semestre_alteracao(semestre_atual):
    """
    Solicita o novo semestre, permitindo que o usuário deixe o campo vazio para manter o atual.

    Valida o formato 'AAAA/1' ou 'AAAA/2' se um valor for digitado.

    :param semestre_atual: O valor atual do semestre (str) para ser mantido caso a entrada seja vazia.
    :return: O novo semestre validado ou o semestre_atual (str).
    """
    while True:
        semestre_str = input(
            f"Novo Semestre (deixe vazio para manter '{semestre_atual}'): "
        ).strip()

        # Retorna o valor atual se o usuário deixar o campo vazio
        if not semestre_str:
            return semestre_atual

        semestre_str = semestre_str.replace(".", "/").replace("-", "/")

        if re.match(r"^\d{4}/[12]$", semestre_str):
            return semestre_str
        else:
            print("Formato inválido. Use o formato AAAA/1 ou AAAA/2.")


def coletar_notas(tipo="principais"):
    #  Coleta uma ou mais notas do usuário, validando se são números entre 0 e 10.
    notas = []
    # Define o limite de notas a coletar: 3 para notas principais, 1 para complementar
    limite = 3 if tipo == "principais" else 1

    for i in range(1, limite + 1):
        while True:
            try:
                prompt = (
                    f"Nota {i}{' complementar' if tipo == 'complementar' else ''}: "
                )
                nota_str = input(prompt).replace(",", ".") # Aceita vírgula e substitui por ponto
                nota = float(nota_str)

                if 0 <= nota <= 10:
                    notas.append(nota)
                    break
                else:
                    print("A nota deve estar entre 0 e 10.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    # Retorna o valor único se for nota complementar, ou a lista se forem notas principais
    return notas if tipo == "principais" else notas[0]


def carregar_alunos():
    """
    Carrega os dados dos alunos a partir do arquivo 'alunos.txt'.

    O arquivo é esperado no formato: nome;ra;turma;semestre por linha.

    """
    alunos = []
    arquivo_path = os.path.join("arquivos", "alunos.txt")

    if os.path.exists(arquivo_path):
        with open(arquivo_path, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    try:              
                        nome, ra, turma, semestre = linha.split(";")
                        alunos.append(
                            {
                                "nome": nome,
                                "ra": ra,
                                "turma": turma,
                                "semestre": semestre,
                            }
                        )
                    except ValueError:
                        print(
                            f"Aviso: Ignorando linha mal formatada em alunos.txt: {linha}"
                        )
    return alunos


def salvar_alunos(alunos):
    """
    Salva a lista de alunos no arquivo 'alunos.txt'.

    Cria o diretório 'arquivos' se ele não existir.

    :param alunos: Lista de dicionários de alunos a serem salvos.
    """
    # Cria o diretório se não existir (exist_ok=True evita erro se já existir)
    os.makedirs("arquivos", exist_ok=True)
    arquivo_path = os.path.join("arquivos", "alunos.txt")

    with open(arquivo_path, "w", encoding="utf-8") as f:
        for a in alunos:
            # Escreve os dados do aluno no formato 'nome;ra;turma;semestre\n'
            f.write(f"{a['nome']};{a['ra']};{a['turma']};{a['semestre']}\n")


def cadastrar_aluno():
    """
    Processa o cadastro de um novo aluno, coletando e validando Nome, RA, Turma e Semestre.

    Verifica se o RA já está cadastrado antes de salvar.
    """
    limpar_tela()
    exibir_cabecalho()
    print("\n--- Cadastro de Aluno (Dados Gerais) ---")
    alunos = carregar_alunos()

    # Coleta e valida o Nome (Apenas letras e espaços)
    while True:
        nome = input("Nome do aluno: ").strip()
        if not nome:
            print("O campo 'Nome' não pode ser vazio.")
        elif not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome):
            print("O nome deve conter apenas letras e espaços (sem números ou símbolos).")
        else:
            break

    # Coleta e valida o RA
    while True:
        ra_input = input("RA (5 dígitos): ").strip()
        if not ra_input.isdigit():
            print("O RA deve conter apenas números (0-9).")
        elif len(ra_input) != 5:
            print("O RA deve conter exatamente 5 dígitos.")
        else:
            # Formata o RA no padrão 'XXXX-X' para armazenamento e comparação
            ra_formatado = f"{ra_input[0:4]}-{ra_input[4]}"

            # Verifica se o RA já existe na lista de alunos carregada
            if any(a["ra"] == ra_formatado for a in alunos):
                print("\nJá existe um aluno com esse RA cadastrado.")
                input("Pressione Enter para voltar...")
                return

            ra = ra_formatado
            break

    # Coleta e valida a Turma
    while True:
        turma_input = input("Turma (Ex: 9A): ").strip().upper()

        if len(turma_input) != 2:
            print(
                "Entrada de turma inválida. Digite o número da série (1-9) e a letra da turma (A-F) (Ex: 9A)."
            )
            continue

        serie = turma_input[0]
        letra = turma_input[1]

        if serie not in "123456789":
            print("A série deve ser um número de 1 a 9.")
            continue

        if letra not in "ABCDEF":
            print("A turma deve ser uma letra de A a F.")
            continue

        turma = f"{serie}ª{letra}"
        break

    semestre = validar_semestre()

    # Adiciona o novo aluno à lista e salva
    alunos.append({"nome": nome, "ra": ra, "turma": turma, "semestre": semestre})
    salvar_alunos(alunos)
    print("\nAluno cadastrado com sucesso!")
    input("Pressione Enter para voltar...")


def alterar_cadastro():
    """
    Permite a alteração dos dados (Nome, Turma e Semestre) de um aluno existente.

    """
    limpar_tela()
    exibir_cabecalho()
    print("\n--- Alteração de Cadastro ---")

    alunos = carregar_alunos()
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        input("Pressione Enter para voltar...")
        return

    ra_input = input("Digite o RA do aluno para alteração (XXXX-X ou XXXXX): ")
    ra_busca = formatar_ra_busca(ra_input)

    # Busca o índice do aluno na lista pelo RA
    aluno_idx = next((i for i, a in enumerate(alunos) if a["ra"] == ra_busca), -1)

    if aluno_idx == -1:
        print("\nAluno não encontrado.")
        input("Pressione Enter para voltar...")
        return

    aluno = alunos[aluno_idx]
    
    print(f"\n--- Dados Atuais do Aluno {aluno['ra']} ---")
    print(f"Nome: {aluno['nome']}")
    print(f"Turma: {aluno['turma']}")
    print(f"Semestre: {aluno['semestre']}")
    print("-------------------------------------------\n")

    # Altera o Nome (Apenas letras e espaços, permite vazio para manter atual)
    while True:
        novo_nome = input(
            f"Novo Nome (deixe vazio para manter '{aluno['nome']}'): "
        ).strip()
        
        if not novo_nome:
            novo_nome = aluno["nome"]
            break
        elif not re.match(r"^[A-Za-zÀ-ÿ\s]+$", novo_nome):
            print("O nome deve conter apenas letras e espaços (sem números ou símbolos).")
        else:
            break
            
    aluno["nome"] = novo_nome

    # Altera a Turma (com validação e permite vazio)
    while True:
        turma_input = (
            input(f"Nova Turma (Ex: 9A, deixe vazio para manter '{aluno['turma']}'): ")
            .strip()
            .upper()
        )

        if not turma_input:
            turma = aluno["turma"]
            break

        # Início da validação da Turma
        if len(turma_input) != 2:
            print(
                "Entrada de turma inválida. Digite o número da série (1-9) e a letra da turma (A-F) (Ex: 9A)."
            )
            continue

        serie = turma_input[0]
        letra = turma_input[1]

        if serie not in "123456789":
            print("A série deve ser um número de 1 a 9.")
            continue

        if letra not in "ABCDEF":
            print("A turma deve ser uma letra de A a F.")
            continue

        turma = f"{serie}ª{letra}"
        break
    aluno["turma"] = turma

    # Altera o Semestre
    semestre_input = validar_semestre_alteracao(aluno["semestre"])
    aluno["semestre"] = semestre_input

    # Atualiza o registro na lista e salva no arquivo
    alunos[aluno_idx] = aluno
    salvar_alunos(alunos)

    print("\nCadastro alterado com sucesso!")
    input("Pressione Enter para voltar...")


def formatar_ra_busca(ra_input):
    """
    Formata o RA de entrada (com ou sem o hífen) para o padrão de armazenamento (XXXX-X).

    Essa padronização é usada para a busca/comparação.

    :param ra_input: O RA digitado pelo usuário (str).
    :return: O RA formatado como 'XXXX-X' (str).
    """
    ra_input = ra_input.strip()
    # Se o RA for 5 dígitos numéricos, formata (ex: '12345' -> '1234-5')
    if ra_input.isdigit() and len(ra_input) == 5:
        return f"{ra_input[0:4]}-{ra_input[4]}"
    return ra_input

def executar_programa_c():
    """
    Executa um programa externo compilado em C para gerar relatórios.

    Utilizamos subprocess para chamar o programa e verificar sua existência.
    """
    limpar_tela()
    exibir_cabecalho()
    print("\n--- Executando Programa em C ---\n")
    
    # Define o nome do executável de acordo com o sistema operacional
    executavel = "relatorio.exe" if os.name == "nt" else "./relatorio"
    
    # Verifica se o executável existe
    if not os.path.exists(executavel):
        print(f"Executável '{executavel}' não encontrado. Compile o C primeiro.")
        input("Pressione Enter para voltar...")
        return
    
    try:
        # Chama o programa em C
        subprocess.run([executavel], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o programa em C: {e}")
    except FileNotFoundError:
        print(f"Executável '{executavel}' não encontrado durante a execução.")

    time.sleep(1) #incluido tempo para dar uma sensação de "loading.." enquanto volta ao menu principal


def carregar_dados_disciplina(disciplina):
    fila = []
    arquivo = os.path.join("arquivos", normalizar_nome_arquivo(disciplina))

    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                try:
                    partes = linha.split(";")            
                    if len(partes) == 5:
                        ra, notas_str, media, situacao, nota_comp_str = partes

                        # Converte a string de notas (ex: "7.0,8.5,6.0") para uma lista de floats
                        notas = [float(n) for n in notas_str.split(",")]

                        fila.append(
                            {
                                "ra": ra,
                                "notas": notas,
                                "media": float(media),
                                "situacao": situacao,
                                "nota_complementar": float(nota_comp_str),
                            }
                        )
                    else:
                        print(
                            f"Aviso: Ignorando linha mal formatada em {arquivo}: {linha}"
                        )
                except ValueError as e:
                    print(f"Aviso: Erro ao processar linha em {arquivo} ({e}): {linha}")
    return fila


def salvar_dados_disciplina(disciplina, fila):
    
    # Salva a lista atualizada de registros de notas (fila) para o arquivo da disciplina.

    os.makedirs("arquivos", exist_ok=True)
    arquivo = os.path.join("arquivos", normalizar_nome_arquivo(disciplina))

    with open(arquivo, "w", encoding="utf-8") as f:
        for a in fila:
            # Converte a lista de notas para uma string separada por vírgula
            notas_str = ",".join(map(str, a["notas"]))

            nota_comp = a.get("nota_complementar", 0.0)

            # Escreve a linha no formato: ra;nota1,nota2,nota3;media;situacao;nota_complementar
            f.write(
                f"{a['ra']};{notas_str};{a['media']:.2f};{a['situacao']};{nota_comp:.2f}\n"
            )


def lancar_notas():
    """
    Permite lançar as 3 notas principais e, se necessário, uma nota complementar para um aluno em uma disciplina.

    Calcula a média final e a situação ('Aprovado'/'Reprovado') e salva o registro.
    """
    limpar_tela()
    exibir_cabecalho()
    print("\n--- Lançamento de Notas ---")

    alunos = carregar_alunos()
    if not alunos:
        print("\nNenhum aluno cadastrado. Cadastre primeiro.")
        input("Pressione Enter para voltar...")
        return

    # Busca aluno pelo RA
    ra_input = input("Digite o RA do aluno (XXXX-X ou XXXXX): ")
    ra_busca = formatar_ra_busca(ra_input)
    aluno = next((a for a in alunos if a["ra"] == ra_busca), None)

    if not aluno:
        print("\nAluno não encontrado.")
        input("Pressione Enter para voltar...")
        return

    # Seleção da disciplina
    menu_disciplinas()
    op = input("Escolha a disciplina: ")
    disciplinas = {
        "1": "Matemática",
        "2": "Português",
        "3": "História",
        "4": "Geografia",
        "5": "Física",
        "6": "Química",
        "7": "Biologia",
        "8": "Artes",
        "9": "Educação Física",
    }
    if op not in disciplinas:
        print("Opção inválida.")
        input("Pressione Enter para voltar...")
        return

    disciplina = disciplinas[op]
    fila = carregar_dados_disciplina(disciplina)

    print(f"\nAluno: {aluno['nome']} ({aluno['ra']})")

    print("\nDigite as 3 notas principais:")
    notas = coletar_notas("principais")
    nota_complementar = 0.0

    # Calcula a média inicial apenas com as 3 notas
    media_inicial = sum(notas) / 3
    media_final = media_inicial

    # Lógica condicional para Nota Complementar (se reprovado)
    if media_inicial < 7.0:
        while True:
            print(
                f"\nAluno reprovado (média: {media_inicial:.2f}). Deseja lançar Nota Complementar?"
            )
            resposta = input("(s/n): ").lower()
            if resposta == "s":
                print(
                    "\n[LEMBRETE] Essa nota será SOMADA à média das 3 notas principais para compor a média final."
                )

                nota_complementar = coletar_notas("complementar") 
                
                media_final = media_inicial + nota_complementar
                break
            elif resposta == "n":
                break
            else:
                print("Opção inválida. Digite 's' para Sim ou 'n' para Não.")

    # Limita a média final a 10.0
    if media_final > 10.0:
        media_final = 10.0

    # Define a situação final com base na média final (Média >= 7.0 é Aprovado)
    situacao_final = "Aprovado" if media_final >= 7.0 else "Reprovado"

    print("\n-------------------------------------------")
    print(
        f"    Cálculo: ({sum(notas):.2f}/3){f' + {nota_complementar:.2f}' if nota_complementar > 0 else ''} = {media_final:.2f}"
    )
    print(f"    Situação Final: {situacao_final}")
    print("-------------------------------------------")

    aluno_dados = {
        "ra": aluno["ra"],
        "notas": notas,
        "media": media_final,
        "situacao": situacao_final,
        "nota_complementar": nota_complementar,
    }

    # Verifica se o aluno já tem um registro na disciplina (para atualização ou novo lançamento)
    aluno_idx = next((i for i, a in enumerate(fila) if a["ra"] == aluno["ra"]), -1)

    if aluno_idx != -1:
        # Atualiza o registro existente
        fila[aluno_idx] = aluno_dados
    else:
        # Adiciona novo registro
        fila.append(aluno_dados)

    salvar_dados_disciplina(disciplina, fila)
    print("\nNotas lançadas com sucesso!")
    input("Pressione Enter para voltar...")


def alterar_notas():
    """
    Permite a alteração das notas principais e complementar de um aluno em uma disciplina.

    Recalcula a média e a situação após as alterações.
    """
    limpar_tela()
    exibir_cabecalho()
    print("\n--- Alteração de Notas ---")

    # Busca aluno e disciplina
    ra_input = input("Digite o RA do aluno (XXXX-X ou XXXXX): ")
    ra_busca = formatar_ra_busca(ra_input)

    menu_disciplinas()
    op = input("Escolha a disciplina: ")
    disciplinas = {
        "1": "Matemática",
        "2": "Português",
        "3": "História",
        "4": "Geografia",
        "5": "Física",
        "6": "Química",
        "7": "Biologia",
        "8": "Artes",
        "9": "Educação Física",
    }
    if op not in disciplinas:
        print("Opção inválida.")
        input("Pressione Enter para voltar...")
        return
    disciplina = disciplinas[op]

    # Carrega os dados da disciplina e busca o registro do aluno
    fila = carregar_dados_disciplina(disciplina)
    aluno = next((a for a in fila if a["ra"] == ra_busca), None)

    if not aluno:
        print("\nNenhuma nota lançada para este aluno nesta disciplina.")
        input("Pressione Enter para voltar...")
        return

    # Exibe os dados atuais
    print(f"\nNotas antigas: {', '.join(map(str, aluno['notas']))}")
    print(f"Nota Complementar Antiga: {aluno.get('nota_complementar', 0.0):.2f}")
    print(f"Média Antiga: {aluno['media']:.2f} ({aluno['situacao']})")

    # Coleta as novas notas principais
    print("\nDigite as novas notas principais:")
    notas = coletar_notas("principais")

    nota_complementar = 0.0
    media_final = sum(notas) / 3
    media_inicial = media_final

    # Lógica de Nota Complementar
    if media_inicial < 7.0:
        while True:
            print(
                f"\nAluno reprovado (média: {media_inicial:.2f}). Deseja aplicar/alterar Nota Complementar?"
            )
            resposta = input("(s/n): ").lower()
            if resposta == "s":

                print(
                    "\n[LEMBRETE] Essa nota será SOMADA à média das 3 notas principais para compor a média final."
                )

                nota_complementar = coletar_notas("complementar")
                media_final = media_inicial + nota_complementar
                break
            elif resposta == "n":
                break
            else:
                print("Opção inválida. Digite 's' para Sim ou 'n' para Não.")

    # Limita a média final
    if media_final > 10.0:
        media_final = 10.0

    # Define a nova situação
    situacao_final = "Aprovado" if media_final >= 7.0 else "Reprovado"

    aluno["notas"] = notas
    aluno["nota_complementar"] = nota_complementar
    aluno["media"] = media_final
    aluno["situacao"] = situacao_final

    # Salva a lista de registros atualizada
    salvar_dados_disciplina(disciplina, fila)
    print("\nNotas alteradas com sucesso!")
    input("Pressione Enter para voltar...")


def visualizar_aluno():
    """
    Exibe os dados cadastrais do aluno e todas as notas lançadas em cada disciplina.
    """
    limpar_tela()
    exibir_cabecalho()
    ra_input = input("Digite o RA do aluno (XXXX-X ou XXXXX): ")
    ra_busca = formatar_ra_busca(ra_input)

    alunos = carregar_alunos()
    aluno = next((a for a in alunos if a["ra"] == ra_busca), None)

    if not aluno:
        print("\nAluno não encontrado.")
        input("Pressione Enter para voltar...")
        return

    print(f"\n--- BOLETIM DO ALUNO ---")
    print(f"Nome: {aluno['nome']}")
    print(f"RA: {aluno['ra']}")
    print(f"Turma: {aluno['turma']} | Semestre: {aluno['semestre']}")
    print("\n--- Disciplinas ---")

    disciplinas = [
        "Matemática",
        "Português",
        "História",
        "Geografia",
        "Física",
        "Química",
        "Biologia",
        "Artes",
        "Educação Física",
    ]

    encontrou_notas = False
    
    for disc in disciplinas:
        fila = carregar_dados_disciplina(disc)
        registro = next((a for a in fila if a["ra"] == ra_busca), None)

        if registro:
            encontrou_notas = True
            # Formata as notas principais para exibição
            notas = ", ".join(map(lambda n: f"{n:.1f}", registro["notas"]))
            print(f"\n{disc}")
            print(f"    Notas: {notas}")
            print(f"    Nota Complementar: {registro.get('nota_complementar', 0.0):.2f}")
            print(f"    Média Final: {registro['media']:.2f}")
            print(f"    Situação: {registro['situacao']}")

    if not encontrou_notas:
        print("\nNenhuma nota lançada para este aluno.")

    print("\n-------------------------------------------")
    input("Pressione Enter para voltar...")


def main():
    """
    Função principal do sistema.
    """
    limpar_tela()

    print("╔══════════════════════════════════════════╗")
    print("║                                          ║")
    print("║    SISTEMA INTEGRADO DISCIPLINAR (S.I.D) ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print("\n            Carregando o S.I.D ...        ")
    time.sleep(2)


    while True:
        limpar_tela()
        exibir_cabecalho()
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Cadastrar Aluno")
        print("2 - Alteração de Cadastro")
        print("3 - Lançar Notas")
        print("4 - Alterar Notas")
        print("5 - Visualizar Aluno")
        print("6 - Gerar Relatórios de Disciplina")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_aluno()
        elif op == "2":
            alterar_cadastro()
        elif op == "3":
            lancar_notas()
        elif op == "4":
            alterar_notas()
        elif op == "5":
            visualizar_aluno()
        elif op == "6":
            # Chama a função que executa o programa em C
            executar_programa_c()    
        elif op == "0":
            print("\nEncerrando o S.I.D... Até logo!")
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    # Garante que a função main só será executada quando o script for rodado diretamente
    main()