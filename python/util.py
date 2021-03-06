import file_io, random
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import random as rd


# Função que gera um vetor com 'num_entradas' de valores {0, 1}
# que podem ser usados para alimentar uma experiencia
def gerar_entradas(num_entradas):
    entradas = []
    for x in range(2 ** num_entradas):
        if x == 0:
            entrada = [0] * num_entradas
        else:
            entrada = entradas[x - 1].copy()
        for y in range(num_entradas):
            if x % (2 ** y) == 0:
                index = num_entradas - 1 - y
                if entrada[index] == 0:
                    entrada[index] = 1
                else:
                    entrada[index] = 0
        entradas = entradas + [entrada]
    entradas.reverse()
    return entradas


# Função que toma os dados de entrada e retorna as entradas com uma dada qtd
# de entradas alteradas como ruido
def gerar_ruido(entradas, ruido):
    for entrada in entradas:
        selecoes = []
        for x in range(ruido):
            index = random.randint(0, len(entrada) - 1)
            while selecoes.__contains__(index):
                index = random.randint(0, len(entrada) - 1)
            if entrada[index] == 0:
                entrada[index] = 1
            else:
                entrada[index] = 0
            selecoes = selecoes + [index]
    return entradas


# Função que testa a acurácia do perceptron dada as entradas e as saídas desejadas
def testar_perceptron(entradas, saidas_desejadas, perceptron):
    acuracia = 0
    for entrada, saida_desejada in zip(entradas, saidas_desejadas):
        saida = perceptron.computar(entrada)
        if saida == saida_desejada:
            acuracia = acuracia + 1
    return acuracia / len(saidas_desejadas)


# Função de imprimir opções de aplicação na GUI
def print_opcoes():
    print('#' * 100)
    print("""Escolha uma das opções abaixo:
        1- Treinar Perceptron
        2- Treinar Multilayer Perceptron (MLP)
        3- Comparar Perceptron com MLP
        0- Sair""")
    print('#' * 100)


# Função responsável pelo input do usuário em relação aos dados de treinamento
def input_dados_treinamento():
    nome_arquivo = input('Digite o nome do arquivo de base de dados: ')
    rotulos = ''

    ignorar_linha_1 = input('Rótulos na primeira linha? (s/n): ')
    if ignorar_linha_1 == 's':
        base_dados = pd.read_csv(nome_arquivo)
    else:
        rotulos = input('Digite os rótulos das variáveis, separadas por vírgula: ')
        rotulos = rotulos.split(',')
        base_dados = pd.read_csv(nome_arquivo, names=rotulos)

    col_remover = input('Digite colunas que queira remover (opcional): ')
    if col_remover:
        col_remover = col_remover.split(',')
        for col in col_remover:
            base_dados = base_dados.drop(col, axis=1)

    nome_classe = input('Digite o nome da coluna classe: ')

    entradas = base_dados.drop(nome_classe, axis=1)
    saidas_desejadas = base_dados[nome_classe]

    return [rotulos, entradas, saidas_desejadas]


# Função que aplica o pré-processamento de dados
def pre_processamento(entradas, saidas_desejadas, tamanho_base_treino):
    entrada_treino, entrada_teste, saida_treino, saida_teste = train_test_split(entradas, saidas_desejadas,
                                                                                test_size=tamanho_base_treino)
    scaler = StandardScaler()
    scaler.fit(entrada_treino)

    entrada_treino = scaler.transform(entrada_treino)
    entrada_teste = scaler.transform(entrada_teste)

    return [entrada_treino, entrada_teste, saida_treino, saida_teste]
