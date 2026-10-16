from pathlib import Path
import zipfile

base = Path("/mnt/data/Projeto_Produtos_C")
base.mkdir(exist_ok=True)

c_code = r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARQUIVO "produtos.csv"

typedef struct {
    char nome[100];
    char categoria[50];
    float preco;
} Produto;

/* Prototipos */
void limparBuffer();
void pausar();
void cadastrar();
void listar();
void buscarPorNome();
void buscarPorCategoria();
void buscarPorFaixa();
void remover();
void atualizar();
int lerProduto(FILE *arquivo, Produto *produto);
void mostrarProduto(Produto produto);

void limparBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void pausar() {
    printf("\nPressione ENTER para continuar...");
    getchar();
}

int lerProduto(FILE *arquivo, Produto *produto) {
    char linha[256];
    char *campo;

    if (fgets(linha, sizeof(linha), arquivo) == NULL) {
        return 0;
    }

    linha[strcspn(linha, "\n")] = '\0';

    campo = strtok(linha, ";");
    if (campo == NULL) return 0;
    strcpy(produto->nome, campo);

    campo = strtok(NULL, ";");
    if (campo == NULL) return 0;
    strcpy(produto->categoria, campo);

    campo = strtok(NULL, ";");
    if (campo == NULL) return 0;
    produto->preco = (float)atof(campo);

    return 1;
}

void mostrarProduto(Produto produto) {
    printf("Nome      : %s\n", produto.nome);
    printf("Categoria : %s\n", produto.categoria);
    printf("Preco     : R$ %.2f\n", produto.preco);
}

void cadastrar() {
    Produto produto;
    FILE *arquivo;

    printf("\n========== CADASTRAR PRODUTO ==========\n");

    printf("Nome do produto: ");
    fgets(produto.nome, sizeof(produto.nome), stdin);
    produto.nome[strcspn(produto.nome, "\n")] = '\0';

    if (strlen(produto.nome) == 0 || strchr(produto.nome, ';') != NULL) {
        printf("Erro: nome invalido.\n");
        return;
    }

    printf("Categoria: ");
    fgets(produto.categoria, sizeof(produto.categoria), stdin);
    produto.categoria[strcspn(produto.categoria, "\n")] = '\0';

    if (strlen(produto.categoria) == 0 || strchr(produto.categoria, ';') != NULL) {
        printf("Erro: categoria invalida.\n");
        return;
    }

    printf("Preco: R$ ");
    if (scanf("%f", &produto.preco) != 1) {
        limparBuffer();
        printf("Erro: preco invalido.\n");
        return;
    }
    limparBuffer();

    if (produto.preco < 0) {
        printf("Erro: o preco nao pode ser negativo.\n");
        return;
    }

    arquivo = fopen(ARQUIVO, "a");

    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }

    fprintf(arquivo, "%s;%s;%.2f\n",
            produto.nome, produto.categoria, produto.preco);

    fclose(arquivo);

    printf("Produto cadastrado com sucesso!\n");
}

void listar() {
    FILE *arquivo;
    Produto produto;
    int contador = 0;

    printf("\n========== PRODUTOS CADASTRADOS ==========\n");

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado ainda.\n");
        return;
    }

    while (lerProduto(arquivo, &produto)) {
        contador++;

        printf("\nProduto %d\n", contador);
        printf("------------------------------------------\n");
        mostrarProduto(produto);
    }

    fclose(arquivo);

    if (contador == 0) {
        printf("Nenhum produto cadastrado.\n");
    }
}

void buscarPorNome() {
    FILE *arquivo;
    Produto produto;
    char nomeBusca[100];
    int encontrado = 0;

    printf("\n========== BUSCAR POR NOME ==========\n");

    printf("Digite o nome do produto que deseja buscar: ");
    fgets(nomeBusca, sizeof(nomeBusca), stdin);
    nomeBusca[strcspn(nomeBusca, "\n")] = '\0';

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado.\n");
        return;
    }

    while (lerProduto(arquivo, &produto)) {
        if (strcmp(produto.nome, nomeBusca) == 0) {
            printf("\nProduto encontrado!\n");
            printf("------------------------------------------\n");
            mostrarProduto(produto);
            encontrado = 1;
            break;
        }
    }

    fclose(arquivo);

    if (!encontrado) {
        printf("Produto nao encontrado.\n");
    }
}

void buscarPorCategoria() {
    FILE *arquivo;
    Produto produto;
    char categoriaBusca[50];
    int encontrado = 0;

    printf("\n========== BUSCAR POR CATEGORIA ==========\n");

    printf("Digite a categoria desejada: ");
    fgets(categoriaBusca, sizeof(categoriaBusca), stdin);
    categoriaBusca[strcspn(categoriaBusca, "\n")] = '\0';

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado.\n");
        return;
    }

    printf("\nProdutos encontrados:\n");

    while (lerProduto(arquivo, &produto)) {
        if (strcmp(produto.categoria, categoriaBusca) == 0) {
            printf("- %s - R$ %.2f\n", produto.nome, produto.preco);
            encontrado = 1;
        }
    }

    fclose(arquivo);

    if (!encontrado) {
        printf("Nenhum produto pertence a essa categoria.\n");
    }
}

void buscarPorFaixa() {
    FILE *arquivo;
    Produto produto;
    float minimo, maximo;
    int encontrado = 0;

    printf("\n========== BUSCAR POR FAIXA DE PRECO ==========\n");

    printf("Preco minimo: R$ ");
    if (scanf("%f", &minimo) != 1) {
        limparBuffer();
        printf("Erro: valor invalido.\n");
        return;
    }

    printf("Preco maximo: R$ ");
    if (scanf("%f", &maximo) != 1) {
        limparBuffer();
        printf("Erro: valor invalido.\n");
        return;
    }
    limparBuffer();

    if (minimo < 0 || maximo < 0) {
        printf("Erro: os valores nao podem ser negativos.\n");
        return;
    }

    if (minimo > maximo) {
        printf("Erro: o preco minimo nao pode ser maior que o preco maximo.\n");
        return;
    }

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado.\n");
        return;
    }

    printf("\nProdutos encontrados na faixa:\n");

    while (lerProduto(arquivo, &produto)) {
        if (produto.preco >= minimo && produto.preco <= maximo) {
            printf("- %s - R$ %.2f\n", produto.nome, produto.preco);
            encontrado = 1;
        }
    }

    fclose(arquivo);

    if (!encontrado) {
        printf("Nenhum produto encontrado nessa faixa de preco.\n");
    }
}

void remover() {
    FILE *arquivo;
    FILE *temporario;
    Produto produto;
    char nomeBusca[100];
    int encontrado = 0;

    printf("\n========== REMOVER PRODUTO ==========\n");

    printf("Digite o nome do produto que deseja remover: ");
    fgets(nomeBusca, sizeof(nomeBusca), stdin);
    nomeBusca[strcspn(nomeBusca, "\n")] = '\0';

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado.\n");
        return;
    }

    temporario = fopen("temp.csv", "w");

    if (temporario == NULL) {
        fclose(arquivo);
        printf("Erro ao criar arquivo temporario.\n");
        return;
    }

    while (lerProduto(arquivo, &produto)) {
        if (strcmp(produto.nome, nomeBusca) == 0 && !encontrado) {
            encontrado = 1;
        } else {
            fprintf(temporario, "%s;%s;%.2f\n",
                    produto.nome, produto.categoria, produto.preco);
        }
    }

    fclose(arquivo);
    fclose(temporario);

    if (encontrado) {
        remove(ARQUIVO);
        rename("temp.csv", ARQUIVO);
        printf("Produto removido com sucesso!\n");
    } else {
        remove("temp.csv");
        printf("Produto nao encontrado.\n");
    }
}

void atualizar() {
    FILE *arquivo;
    FILE *temporario;
    Produto produto;
    char nomeBusca[100];
    int encontrado = 0;

    printf("\n========== ATUALIZAR PRODUTO ==========\n");

    printf("Digite o produto que deseja atualizar: ");
    fgets(nomeBusca, sizeof(nomeBusca), stdin);
    nomeBusca[strcspn(nomeBusca, "\n")] = '\0';

    arquivo = fopen(ARQUIVO, "r");

    if (arquivo == NULL) {
        printf("Nenhum produto cadastrado.\n");
        return;
    }

    temporario = fopen("temp.csv", "w");

    if (temporario == NULL) {
        fclose(arquivo);
        printf("Erro ao criar arquivo temporario.\n");
        return;
    }

    while (lerProduto(arquivo, &produto)) {
        if (strcmp(produto.nome, nomeBusca) == 0 && !encontrado) {
            Produto novo;

            printf("\nProduto encontrado.\n");

            printf("Novo nome: ");
            fgets(novo.nome, sizeof(novo.nome), stdin);
            novo.nome[strcspn(novo.nome, "\n")] = '\0';

            if (strlen(novo.nome) == 0 || strchr(novo.nome, ';') != NULL) {
                printf("Erro: nome invalido. Atualizacao cancelada.\n");
                fprintf(temporario, "%s;%s;%.2f\n",
                        produto.nome, produto.categoria, produto.preco);
                continue;
            }

            printf("Nova categoria: ");
            fgets(novo.categoria, sizeof(novo.categoria), stdin);
            novo.categoria[strcspn(novo.categoria, "\n")] = '\0';

            if (strlen(novo.categoria) == 0 || strchr(novo.categoria, ';') != NULL) {
                printf("Erro: categoria invalida. Atualizacao cancelada.\n");
                fprintf(temporario, "%s;%s;%.2f\n",
                        produto.nome, produto.categoria, produto.preco);
                continue;
            }

            printf("Novo preco: R$ ");
            if (scanf("%f", &novo.preco) != 1) {
                limparBuffer();
                printf("Erro: preco invalido. Atualizacao cancelada.\n");
                fprintf(temporario, "%s;%s;%.2f\n",
                        produto.nome, produto.categoria, produto.preco);
                continue;
            }
            limparBuffer();

            if (novo.preco < 0) {
                printf("Erro: o preco nao pode ser negativo. Atualizacao cancelada.\n");
                fprintf(temporario, "%s;%s;%.2f\n",
                        produto.nome, produto.categoria, produto.preco);
                continue;
            }

            fprintf(temporario, "%s;%s;%.2f\n",
                    novo.nome, novo.categoria, novo.preco);

            encontrado = 1;
        } else {
            fprintf(temporario, "%s;%s;%.2f\n",
                    produto.nome, produto.categoria, produto.preco);
        }
    }

    fclose(arquivo);
    fclose(temporario);

    if (encontrado) {
        remove(ARQUIVO);
        rename("temp.csv", ARQUIVO);
        printf("Produto atualizado com sucesso!\n");
    } else {
        remove("temp.csv");
        printf("Produto nao encontrado ou atualizacao cancelada.\n");
    }
}

int main() {
    int opcao;

    do {
        printf("\n========================================\n");
        printf("       SISTEMA DE CADASTRO DE PRODUTOS\n");
        printf("========================================\n");
        printf("[1] Cadastrar produto\n");
        printf("[2] Listar produtos\n");
        printf("[3] Buscar por nome\n");
        printf("[4] Buscar por categoria\n");
        printf("[5] Buscar por faixa de precos\n");
        printf("[6] Remover produto\n");
        printf("[7] Atualizar produto\n");
        printf("[0] Sair\n");
        printf("----------------------------------------\n");
        printf("Escolha uma opcao: ");

        if (scanf("%d", &opcao) != 1) {
            limparBuffer();
            printf("\nOpcao invalida! Digite um numero do menu.\n");
            continue;
        }
        limparBuffer();

        switch (opcao) {
            case 1:
                cadastrar();
                pausar();
                break;

            case 2:
                listar();
                pausar();
                break;

            case 3:
                buscarPorNome();
                pausar();
                break;

            case 4:
                buscarPorCategoria();
                pausar();
                break;

            case 5:
                buscarPorFaixa();
                pausar();
                break;

            case 6:
                remover();
                pausar();
                break;

            case 7:
                atualizar();
                pausar();
                break;

            case 0:
                printf("\nPrograma encerrado. Obrigado!\n");
                break;

            default:
                printf("\nOpcao invalida! Escolha uma opcao do menu.\n");
        }

    } while (opcao != 0);

    return 0;
}
'''

csv_content = """Teclado;Perifericos;89.90
Mouse Gamer;Perifericos;149.90
Monitor;Eletronicos;899.00
Headset;Perifericos;199.90
Notebook;Computadores;3499.90
"""

readme = r'''# Projeto Prático em C - Sistema de Cadastro de Produtos

## Integrantes

1. Nome do integrante 1
2. Nome do integrante 2
3. Nome do integrante 3
4. Nome do integrante 4
5. Nome do integrante 5
6. Nome do integrante 6

## Descrição

Sistema desenvolvido em linguagem C para cadastro e gerenciamento de produtos de uma loja.

O programa utiliza:

- `struct`
- funções
- menu de opções
- `switch`
- estruturas de repetição e condicionais
- arquivos texto/CSV
- `fopen()` e `fclose()`
- `fprintf()` e `fgets()`
- `strtok()`
- `strcpy()`
- `strcmp()`

## Funcionalidades

1. Cadastrar produto
2. Listar produtos
3. Buscar produto por nome
4. Buscar produtos por categoria
5. Buscar produtos por faixa de preços
6. Remover produto
7. Atualizar produto
0. Sair

## Estrutura do produto

Cada produto possui:

- Nome
- Categoria
- Preço

A estrutura utilizada no programa é:

```c
typedef struct {
    char nome[100];
    char categoria[50];
    float preco;
} Produto;
