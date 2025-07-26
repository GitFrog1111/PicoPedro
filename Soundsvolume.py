import mutagen
from mutagen.mp3 import MP3
import os
import shutil
from pydub import AudioSegment

def process_sounds():
    # Create output directory if it doesn't exist
    output_dir = "sounds_Updated"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get all sound files from /sounds directory
    sounds_dir = "sounds"
    sound_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    sound_files = []
    
    if os.path.exists(sounds_dir):
        for file in os.listdir(sounds_dir):
            if any(file.lower().endswith(ext) for ext in sound_extensions):
                sound_files.append(os.path.join(sounds_dir, file))
    else:
        print(f"Directory '{sounds_dir}' not found!")
        return
    
    print(f"Found {len(sound_files)} sound files to process")
    
    for sound_file in sound_files:
        try:
            print(f"Processing: {sound_file}")
            
            # Load the audio file
            audio = AudioSegment.from_file(sound_file)
            
            # Reduce volume by 50% (half volume)
            reduced_audio = audio - 8  # -6 dB is approximately half volume
            
            # Save to output directory
            filename = os.path.basename(sound_file)
            output_path = os.path.join(output_dir, filename)
            reduced_audio.export(output_path, format=filename.split('.')[-1])
            
            print(f"Saved: {output_path}")
            
        except Exception as e:
            print(f"Error processing {sound_file}: {e}")

if __name__ == "__main__":
    process_sounds()
