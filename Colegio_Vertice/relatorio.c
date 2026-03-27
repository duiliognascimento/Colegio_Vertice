#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define o tamanho máximo para strings/arrays de caracteres
#define MAX_LEN 100

// --------------------------------
// Estrutura de dados
// --------------------------------

typedef struct {
    char nome[MAX_LEN];      // Nome completo do aluno.
    char ra[MAX_LEN];        // Registro de Aluno (RA), chave de busca.
    char turma[MAX_LEN];     // Turma do aluno (Ex: 9ªA).
    char semestre[MAX_LEN];  // Semestre de matrícula (Ex: AAAA/1).
} Aluno;

// --------------------------------
// Funções utilitárias
// --------------------------------

void limpar_tela() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

void pausar() {
    printf("\nPressione Enter para continuar...");
    getchar();
    // Consome o buffer residual se necessário
    while (getchar() != '\n'); 
}

void exibir_cabecalho() {
    printf("========================================================\n");
    printf("                RELATORIO ESCOLAR                       \n");
    printf("========================================================\n");
}

// --------------------------------
// Funções de leitura de arquivos
// --------------------------------

/**
 * Lê os dados cadastrais dos alunos do arquivo 'arquivos/alunos.txt'.
 * Retorna o número de alunos lidos.
 */
int ler_alunos(Aluno alunos[], int max_alunos) {
    FILE *arquivo = fopen("arquivos/alunos.txt", "r");
    if (!arquivo) {
        printf("Aviso: Nenhum aluno matriculado ou arquivo nao encontrado.\n");
        return 0;
    }

    int i = 0;
    // Formato %[^\n] ou %[^\n\r] para lidar com quebras de linha de diferentes SOs
    while (i < max_alunos && fscanf(arquivo, " %99[^;];%99[^;];%99[^;];%99[^\n]",
                  alunos[i].nome, alunos[i].ra, alunos[i].turma, alunos[i].semestre) == 4) {
        i++;
    }

    fclose(arquivo);
    return i;
}

// --------------------------------
// Exibição de relatórios
// --------------------------------

/**
 * Exibe o relatório de notas de uma disciplina específica.
 */
void exibir_notas(const Aluno alunos[], int num_alunos, const char *disciplina) {
    limpar_tela();
    exibir_cabecalho();
    printf("\n--- RELATORIOS DE DISCIPLINAS ---\n");

    char caminho[MAX_LEN];
    snprintf(caminho, MAX_LEN, "arquivos/%s.txt", disciplina);

    FILE *arquivo = fopen(caminho, "r");
    if (!arquivo) {
        printf("Aviso: Nenhuma nota lancada ainda para esta disciplina.\n");
        pausar();
        return;
    }

    char ra[MAX_LEN], notas[MAX_LEN], situacao[MAX_LEN];
    float media;
    int encontrado;

    // Lendo o formato: ra;nota1,nota2,nota3;media;situacao;nota_complementar
    // Como o Python salva 5 campos, vamos ler os 4 primeiros e ignorar o resto da linha
    while (fscanf(arquivo, " %99[^;];%99[^;];%f;%99[^;\n]", ra, notas, &media, situacao) != EOF) {
        // Limpa o restante da linha (como a nota complementar que o Python envia)
        fscanf(arquivo, "%*[^\n]\n"); 
        
        encontrado = 0;

        for (int i = 0; i < num_alunos; i++) {
            if (strcmp(alunos[i].ra, ra) == 0) {
                printf("\nAluno: %s\n", alunos[i].nome);
                printf("RA: %s | Turma: %s | Semestre: %s\n",
                       alunos[i].ra, alunos[i].turma, alunos[i].semestre);
                printf("Notas: %s | Media: %.2f | Situacao: %s\n",
                       notas, media, situacao);
                printf("----------------------------------------------\n");
                encontrado = 1;
                break;
            }
        }

        if (!encontrado) {
            printf("Aviso: RA %s nao encontrado no cadastro geral.\n", ra);
        }
    }

    fclose(arquivo);
    pausar();
}

// --------------------------------
// Menu de disciplinas
// --------------------------------

void menu_disciplinas(Aluno alunos[], int num_alunos) {
    int opcao;

    do {
        limpar_tela();
        exibir_cabecalho();
        printf("\n=== MENU DE DISCIPLINAS ===\n");
        printf("1 - Matematica\n");
        printf("2 - Portugues\n");
        printf("3 - Historia\n");
        printf("4 - Geografia\n");
        printf("5 - Fisica\n");
        printf("6 - Quimica\n");
        printf("7 - Biologia\n");
        printf("8 - Artes\n");
        printf("9 - Educacao Fisica\n");
        printf("0 - Voltar\n");
        printf("\nEscolha: ");
        
        if (scanf("%d", &opcao) != 1) {
            while (getchar() != '\n'); // Limpa buffer em caso de erro
            continue;
        }

        switch (opcao) {
            case 1: exibir_notas(alunos, num_alunos, "matematica"); break;
            case 2: exibir_notas(alunos, num_alunos, "portugues"); break;
            case 3: exibir_notas(alunos, num_alunos, "historia"); break;
            case 4: exibir_notas(alunos, num_alunos, "geografia"); break;
            case 5: exibir_notas(alunos, num_alunos, "fisica"); break;
            case 6: exibir_notas(alunos, num_alunos, "quimica"); break;
            case 7: exibir_notas(alunos, num_alunos, "biologia"); break;
            case 8: exibir_notas(alunos, num_alunos, "artes"); break;
            case 9: exibir_notas(alunos, num_alunos, "educacao_fisica"); break;
            case 0: break;
            default: printf("Opcao invalida.\n"); pausar(); break;
        }

    } while (opcao != 0);
}

// --------------------------------
// Funcao principal
// --------------------------------

int main() {
    Aluno alunos[100];
    int num_alunos = ler_alunos(alunos, 100);

    if (num_alunos == 0) {
        printf("Nenhum dado de aluno foi encontrado para gerar relatorios.\n");
        pausar();
        return 0;
    }

    int opcao;
    while (1) {
        limpar_tela();
        exibir_cabecalho();
        printf("\n=== MENU DE RELATORIOS ===\n");
        printf("1 - Relatorio de Alunos Matriculados\n");
        printf("2 - Relatorios por Disciplina\n");
        printf("0 - Voltar ao menu principal (Python)\n");
        printf("\nEscolha: ");
        
        if (scanf("%d", &opcao) != 1) {
            while (getchar() != '\n');
            continue;
        }

        switch (opcao) {
            case 1:
                limpar_tela();
                exibir_cabecalho();
                printf("\n--- ALUNOS MATRICULADOS ---\n\n");
                for (int i = 0; i < num_alunos; i++) {
                    printf("Nome: %s\n", alunos[i].nome);
                    printf("RA: %s | Turma: %s | Semestre: %s\n",
                           alunos[i].ra, alunos[i].turma, alunos[i].semestre);
                    printf("----------------------------------------------\n");
                }
                pausar();
                break;

            case 2:
                menu_disciplinas(alunos, num_alunos);
                break;

            case 0:
                limpar_tela();
                printf("\nSaindo do modulo de relatorios...\n");
                return 0;

            default:
                printf("Opcao invalida.\n");
                pausar();
                break;
        }
    }

    return 0;
}