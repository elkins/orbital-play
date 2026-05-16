from orbital_play import sonify
import wave
import io

def test_generate_hum():
    energy = -75.0
    wav_bytes = sonify.generate_hum(energy)
    assert len(wav_bytes) > 0
    # Check if it's a valid WAV
    with wave.open(io.BytesIO(wav_bytes), 'rb') as f:
        assert f.getnchannels() == 1
        assert f.getsampwidth() == 2
        assert f.getframerate() == 22050
