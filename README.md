# TP1 – Composição Musical Algorítmica com Cadeias de Markov

Gerador de música simbólica (MIDI) com cadeias de Markov de ordem n, treinadas em melodias em tom menor do Nottingham Dataset. O estilo-alvo é o do tema de *Requiem for a Dream*: dramático, sombrio, tenso e repetitivo.

## Estrutura do projeto

```
.
├── README.md
├── requirements.txt
├── corpus.py
├── markov.py
├── gerar_musica.py
├── sintetizador.py
├── melody/               # MIDIs do Nottingham Dataset
├── FluidR3_GM.sf2        # soundfont usado na síntese de áudio
├── corpus_estados.json   # gerado por corpus.py
├── musica_A.mid  musica_B.mid  musica_C.mid   # gerados por gerar_musica.py
└── musica_A.wav  musica_B.wav  musica_C.wav   # gerados por sintetizador.py
```

## Instalação

### 1. Python e dependências

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. FluidSynth

O `sintetizador.py` usa o FluidSynth.

**Linux (Ubuntu/Debian)**
```bash
sudo apt install fluidsynth
```

**macOS**
```bash
brew install fluidsynth
```

O soundfont `FluidR3_GM.sf2` já está na pasta do projeto.

## Execução

### Passo 1: preparar o corpus

A pasta `melody` contém os arquivos do `MIDI/melody` do Nottingham Dataset (github.com/jukedeck/nottingham-dataset).

### Passo 2: gerar o corpus de estados

O `corpus.py` lê os MIDIs de `melody/`, mantém as peças em tom menor, transpõe para Lá menor e salva as sequências de estados em `corpus_estados.json`.

```bash
python3 corpus.py
```

### Passo 3: gerar as músicas

O `gerar_musica.py` usa o `markov.py` (que treina a cadeia de Markov) e escreve `musica_A.mid`, `musica_B.mid` e `musica_C.mid`.

```bash
python3 gerar_musica.py
```

### Passo 4: sintetizar o áudio

O `sintetizador.py` usa o `FluidR3_GM.sf2` para converter os `.mid` em `musica_A.wav`, `musica_B.wav` e `musica_C.wav`.

```bash
python3 sintetizador.py
```

## Uso de Inteligência Artificial

No gemini, foi definido a partir da conversa as informações dos instrumentos, dos acordes e das probabilidades de transição da harmonia. Link: https://share.gemini.google/wbVvIB73Dxpd

