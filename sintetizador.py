from midi2audio import FluidSynth

SOUNDFONT = "GeneralUser-GS.sf2" 

def midi_para_audio(midi_file, sf2_file, audio_file):
    # Inicia o FluidSynth apontando para o arquivo de soundfont
    fs = FluidSynth(sf2_file)
    # Executa a renderização do áudio
    fs.midi_to_audio(midi_file, audio_file)

midi_para_audio("musica_A.mid", SOUNDFONT, "musica_A.wav")
midi_para_audio("musica_B.mid", SOUNDFONT, "musica_B.wav")
midi_para_audio("musica_C.mid", SOUNDFONT, "musica_C.wav")