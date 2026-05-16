import numpy as np
import io
import wave

def generate_hum(energy, duration=0.5, sample_rate=22050):
    """
    Generates a WAV audio buffer where the pitch is determined by the system energy.
    Translates the 'tension' of the quantum state into sound.
    """
    # Map energy to a frequency in the audible range
    # We want more stable (more negative) energy to feel different from unstable energy.
    # Base frequency + some factor of the energy
    # For H2 (~ -1.1) to H2O (~ -75), we want a noticeable range.
    freq = 200.0 + abs(energy) * 10.0
    
    # Keep it within a pleasant/audible range (150Hz - 1200Hz)
    freq = (freq % 1000) + 150.0
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a wave with a slight fade-out to prevent clicking
    envelope = np.exp(-3 * t / duration) 
    audio = np.sin(freq * t * 2 * np.pi) * envelope
    
    # Normalize to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    
    # Write to bytes in memory
    byte_io = io.BytesIO()
    with wave.open(byte_io, 'wb') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
        
    return byte_io.getvalue()
