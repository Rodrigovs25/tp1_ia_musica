import json
import random

# Converte cada estado de uma lista para uma tupla
def carregar_corpus(caminho="corpus_estados.json"):
    with open(caminho) as arquivo:
        dados = json.load(arquivo)

    corpus = []
    for sequencia in dados.values():
        musica = []
        for estado in sequencia:
            musica.append(tuple(estado))
        corpus.append(musica)
    return corpus


class MarkovModel:
    # Estado é o par (altura, duração)

    def __init__(self, ordem=2):
        self.ordem = ordem

        self.tabelas = [] # Armazena as frequências das transições
        for k in range(ordem + 1):
            self.tabelas.append({})

        self.inicios = [] # Armazena os estados iniciais das músicas

    # Treina cada música separadamente, transformado as músicas em tabela de frequências que representa as transições
    def treinar(self, musicas):
        for musica in musicas:
            self.inicios.append(tuple(musica[:self.ordem]))

            for i in range(len(musica)):
                estado = musica[i]

                for tamanho in range(min(i, self.ordem) + 1): # tamanho determina o contexto
                    contexto = tuple(musica[i - tamanho:i])

                    tabela = self.tabelas[tamanho]
                    if contexto not in tabela:
                        tabela[contexto] = {}
                    contagens = tabela[contexto]
                    contagens[estado] = contagens.get(estado, 0) + 1

    def escolher_proximo_estado(self, historico, temperatura, seed):
        
        for tamanho in range(min(self.ordem, len(historico)), -1, -1):
            contexto = tuple(historico[len(historico) - tamanho:])

            if contexto in self.tabelas[tamanho]:
                contagens = self.tabelas[tamanho][contexto]
                estados = list(contagens.keys())

                pesos = []
                for quantidade in contagens.values():
                    pesos.append(quantidade ** (1 / temperatura)) # Altera a influência das frequências

                return seed.choices(estados, weights=pesos)[0]

    # Produz uma sequência de estados
    def gerar(self, quantidade, semente=None, temperatura=1.0):
        seed = random.Random(semente)

        sequencia = list(seed.choice(self.inicios))

        while len(sequencia) < quantidade:
            sequencia.append(self.escolher_proximo_estado(sequencia, temperatura, seed))
        return sequencia

# Guarda os trechos do corpus num conjunto
def calcular_taxa_copia(sequencia, corpus, tamanho=6):
    trechos_corpus = set()
    for musica in corpus:
        for i in range(len(musica) - tamanho + 1):
            trecho = tuple(musica[i:i + tamanho])
            trechos_corpus.add(trecho)

    total = 0
    copiados = 0
    # Conta quantos trechos da música gerada aparecem no corpus
    for i in range(len(sequencia) - tamanho + 1): 
        trecho = tuple(sequencia[i:i + tamanho])
        total += 1
        if trecho in trechos_corpus:
            copiados += 1

    if total == 0:
        return 0.0
    return copiados / total