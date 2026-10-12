import os
from music21 import converter

# Configurações dos filtros (ajuste conforme o rigor desejado)
DURACAO_MINIMA = 40.0  # Em tempos/semínimas (exclui trechos curtos ou vinhetas) 20
DURACAO_MAXIMA = 90.0 # Opcional: limite superior de duração 100
EXTENSAO_MAXIMA = 14   # Extensão máxima em semitons (19 = uma oitava e meia) 19

def filtrar_melodias_nottingham(pasta_midi):
    selecionadas = []
    
    for arquivo in os.listdir(pasta_midi):
        if not arquivo.endswith('.mid'):
            continue
            
        caminho_completo = os.path.join(pasta_midi, arquivo)
        
        try:
            # Carrega a estrutura musical do arquivo MIDI
            partitura = converter.parse(caminho_completo)
            
            # 1. Filtro: Apenas Tonalidade Menor
            tonalidade = partitura.analyze('key')
            if tonalidade.mode != 'minor':
                continue
                
            # 2. Filtro: Duração (não curtas)
            duracao = partitura.highestTime
            if duracao < DURACAO_MINIMA or duracao > DURACAO_MAXIMA:
                continue
                
            # 3. Filtro: Extensão (range) não muito grande
            notas = partitura.pitches
            if not notas:
                continue
                
            nota_mais_grave = min(notas).midi
            nota_mais_aguda = max(notas).midi
            extensao = nota_mais_aguda - nota_mais_grave
            
            if extensao > EXTENSAO_MAXIMA:
                continue
                
            print(f"Aceito: {arquivo} | Tom: {tonalidade} | Duração: {duracao} | Extensão: {extensao} st")
            selecionadas.append(arquivo)
            
        except Exception:
            # Pula silenciosamente arquivos mal formatados ou sem notas legíveis
            pass
            
    print(f"\nTotal retornado: {len(selecionadas)} melodias.")
    return selecionadas

# Execução:
# pip install music21
filtrar_melodias_nottingham('.')