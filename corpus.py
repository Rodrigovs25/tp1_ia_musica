import json
import os

from music21 import converter

GRADE = 0.25 # semicolcheia
LA = 9 # classe de altura do Lá 
MIN_ESTADOS = 40 # minimo de estados

# Devolve a lista de estados (altura, duração)
def escolher_estados(caminho):
    partitura = converter.parse(caminho)

    tom = partitura.analyze("key")
    if tom.mode != "minor": # uso do tom minor
        return None

    # Transpor as músicas para Lá menor
    desloc = (LA - tom.tonic.pitchClass) % 12
    if desloc > 6:
        desloc = desloc - 12

    sequencia = [] # estado da música
    for elemento in partitura.flatten().notesAndRests:
        duracao = round(elemento.quarterLength / GRADE) * GRADE
        if duracao <= 0:
            continue

        # diferenciar notas de pausas
        if elemento.isRest:
            altura = None
        else:
            altura = max(p.midi for p in elemento.pitches) + desloc

        sequencia.append((altura, duracao))

    # remove as pausa no início e fim
    while sequencia and sequencia[0][0] is None:
        sequencia.pop(0)
    while sequencia and sequencia[-1][0] is None:
        sequencia.pop()

    # filtrar músicas curtas
    if len(sequencia) < MIN_ESTADOS:
        return None
    if sequencia[-1][0] % 12 != LA:
        return None

    return sequencia


if __name__ == "__main__":
    pasta = "melody"

    corpus = {}
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".mid"):
            continue
        sequencia = escolher_estados(os.path.join(pasta, nome))
        if sequencia is not None:
            corpus[nome] = sequencia

    with open("corpus_estados.json", "w") as arquivo:
        json.dump(corpus, arquivo)

    total = 0
    for sequencia in corpus.values():
        total += len(sequencia)
    print(len(corpus), "peças,", total, "estados")