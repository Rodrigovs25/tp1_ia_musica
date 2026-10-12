from midi2audio import FluidSynth

def midi_para_audio(midi_file, sf2_file, audio_file):
    # Inicia o FluidSynth apontando para o arquivo de soundfont
    fs = FluidSynth(sf2_file)
    # Executa a renderização do áudio
    fs.midi_to_audio(midi_file, audio_file)

# Exemplo de execução
midi_para_audio("musica_A.mid", "FluidR3_GM.sf2", "musica_A.wav")
midi_para_audio("musica_B.mid", "FluidR3_GM.sf2", "musica_B.wav")
midi_para_audio("musica_C.mid", "FluidR3_GM.sf2", "musica_C.wav")

