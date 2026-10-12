import random
import pretty_midi

from markov import MarkovModel, carregar_corpus, calcular_taxa_copia

ACORDES = {
    "Am": (69, (0, 3, 7)),    
    "F":  (65, (0, 4, 7)),   
    "C":  (72, (0, 4, 7)),   
    "Dm": (74, (0, 3, 7)),    
    "E":  (64, (0, 4, 7)),    
    "Bb": (70, (0, 4, 7)),   
    "G":  (67, (0, 4, 7)),    
}

# as probabilidades foram definidas na mão
TRANSICOES = {
    "Am": {"Am": 0.25, "Bb": 0.25, "G": 0.15, "Dm": 0.20, "E": 0.15},
    "F": {"C": 0.35, "G": 0.25, "Am": 0.25, "E": 0.15},
    "C": {"G": 0.35, "Am": 0.25, "F": 0.20, "Dm": 0.15, "Bb": 0.05},
    "G": {"Am": 0.45, "F": 0.25, "C": 0.20, "E": 0.10},
    "Dm": {"Am": 0.35, "E": 0.30, "Bb": 0.20, "F": 0.15},
    "E": {"Am": 0.70, "F": 0.15, "Dm": 0.15},
    "Bb": {"Am": 0.20, "C": 0.35, "Dm": 0.45},
}

COMPASSO = 4.0 # semínimas por compasso

# faixa de alturas da melodia
FAIXA_MIN = 57
FAIXA_MAX = 81

# Cria a sequência de acorde
def gerar_harmonia(quantidade, seed):
    acordes = []
    atual = seed.choice(list(ACORDES.keys()))
    for _ in range(quantidade):
        acordes.append(atual)
        opcoes = TRANSICOES[atual]
        atual = seed.choices(list(opcoes), weights=list(opcoes.values()))[0]
    return acordes

# Ajusta a altura da nota
def ajustar_altura_faixa(altura):
    while altura < FAIXA_MIN:
        altura += 12
    while altura > FAIXA_MAX:
        altura -= 12
    return altura

# Ajusta a nota para que ela pertença ao acorde atual
def ajustar_altura_acorde(altura, acorde):
    raiz, intervalos = ACORDES[acorde]
    notas_acorde = {(raiz + i) % 12 for i in intervalos}

    for desloc in sorted(range(-3, 4), key=abs):
        if (altura + desloc) % 12 in notas_acorde:
            return ajustar_altura_faixa(altura + desloc)

# Determinar a sequência de notas e durações que será utilizada no primeiro compasso.
def gerar_melodia_base(modelo, seed, temperatura):
    estados = list(seed.choice(modelo.inicios))
    sequencia = []
    tempo = 0.0

    while tempo < COMPASSO:
        if len(sequencia) == len(estados):
            estados.append(modelo.escolher_proximo_estado(estados, temperatura, seed))

        altura, duracao = estados[len(sequencia)]
        if altura is not None:
            altura = ajustar_altura_faixa(altura)

        duracao = min(duracao, COMPASSO - tempo)
        sequencia.append((altura, duracao))
        tempo += duracao

    return sequencia

# Receber a melodia base e produz um versao modificada
def criar_variacao(base, anterior, modelo, seed, temperatura, probabilidade_mutacao, acorde):
    resultado = []
    tempo = 0.0

    for altura, duracao in base:
        if altura is not None:
            if seed.random() < probabilidade_mutacao: # modificação da nota
                estado = modelo.escolher_proximo_estado(anterior + [(altura, duracao)], temperatura, seed)
                altura = estado[0]
                if altura is not None:
                    altura = ajustar_altura_faixa(altura)

            if altura is not None: # ajustar no acorde atual
                altura = ajustar_altura_acorde(altura, acorde)

        resultado.append((altura, duracao))
        tempo += duracao

    return resultado

# Adicionar nota ao instrumento
def adicionar_nota(instrumento, altura, inicio, fim, velocidade):
    instrumento.notes.append(pretty_midi.Note(int(velocidade), altura, inicio, fim))

# Carregar o corpus e treinar o modelo
def gerar_musica(ordem, temperatura, semente, probabilidade_mutacao, saida, bpm=80, compassos=32, por_acorde=2):
    corpus = carregar_corpus()
    seed = random.Random(semente)

    modelo = MarkovModel(ordem)
    modelo.treinar(corpus)

    base = gerar_melodia_base(modelo, seed, temperatura)
    acordes = gerar_harmonia((compassos + por_acorde - 1) // por_acorde, seed)

    batida = 60.0 / bpm
    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    # Instrumentos usados na música.
    violao = pretty_midi.Instrument(program=24)
    cordas = pretty_midi.Instrument(program=44)
    atmosfera = pretty_midi.Instrument(program=99)
    reforco_melodia = pretty_midi.Instrument(program=47)

    anterior = []
    for c in range(compassos): # percorrer os compassos
        acorde = acordes[c // por_acorde]
        raiz, intervalos = ACORDES[acorde]

        inicio = c * COMPASSO * batida
        fim = inicio + COMPASSO * batida

        velocidade = 35 + 80 * c / max(1, compassos - 1)

        adicionar_nota(violao, raiz, inicio, fim, velocidade)
        for i in intervalos:
            adicionar_nota(cordas, raiz + 12 + i, inicio + batida, fim, velocidade * 0.7)

        if c == 0:
            atual = base
        else: # gerar variações 
            atual = criar_variacao(base, anterior, modelo, seed, temperatura, probabilidade_mutacao, acorde)
        anterior = atual

        tempo = 0.0
        for altura, duracao in atual:
            if altura is not None:
                ini = inicio + tempo * batida
                fim_nota = ini + duracao * batida
                adicionar_nota(atmosfera, altura, ini, fim_nota, velocidade)

                if c >= compassos // 2:
                    adicionar_nota(reforco_melodia, altura + 12, ini, fim_nota, velocidade * 0.45)
            tempo += duracao

    midi.instruments.extend([violao, cordas, atmosfera, reforco_melodia])
    midi.write(saida)

    # Gera uma sequência de 120 estados usando o modelo de Markov
    amostra = modelo.gerar(120, semente=semente, temperatura=temperatura)
    # Calcula a proporção de trechos que também aparecem no corpus
    copia = calcular_taxa_copia(amostra, corpus)

    print(f"{saida}: ordem={ordem}, T={temperatura}, semente={semente}, "
          f"mutacao={probabilidade_mutacao}, copia={copia}")
    print("acordes:", " ".join(acordes))


if __name__ == "__main__":
    # ordem: 1 a 5
    # temperatura: 0.1 a 2.0
    # probabilidade: 0.0 a 1.0
    gerar_musica(ordem=1, temperatura=1.8, semente=1, probabilidade_mutacao=0.95, saida="musica_A.mid")
    gerar_musica(ordem=3, temperatura=1.0, semente=5, probabilidade_mutacao=0.45, saida="musica_B.mid")
    gerar_musica(ordem=5, temperatura=0.2, semente=10, probabilidade_mutacao=0.05, saida="musica_C.mid")