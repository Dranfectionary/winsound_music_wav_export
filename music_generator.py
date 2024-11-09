import math
import wave
import struct
import os
import winsound
import time


# Function to read frequency data from a text file for chords
def read_frequencies(filename):
    frequencies = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                chord = [float(freq.strip()) for freq in line.strip().split(',')]
                frequencies.append(chord)
            except ValueError:
                print(f"Warning: Could not parse line as frequencies: {line.strip()}")
    return frequencies


# Function to read duration data from a text file
def read_durations(filename):
    durations = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                durations.append(float(line.strip()))
            except ValueError:
                print(f"Warning: Could not convert line to float: {line.strip()}")
    return durations


# Function to generate a tone series with chords and variable durations, with fade-in and fade-out
def generate_song(filename, frequencies, durations, sample_rate=44100, amplitude=32767, fade_duration=0.005):
    if len(frequencies) != len(durations):
        print("Error: The frequencies and durations lists must have the same length.")
        return

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    start_time = time.time()  # Start timing

    with wave.open(downloads_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)

        for chord, duration in zip(frequencies, durations):
            total_samples = int(sample_rate * duration)
            fade_samples = int(sample_rate * fade_duration)

            # Initialize phases and phase increments for each frequency in the chord
            phase_increments = [(2 * math.pi * freq) / sample_rate for freq in chord]
            phases = [0.0] * len(chord)

            # Buffer to store samples for the entire chord duration
            samples = []

            for i in range(total_samples):
                # Determine amplitude multiplier for fade-in and fade-out
                if i < fade_samples:
                    fade_factor = i / fade_samples  # Fade-in
                elif i > total_samples - fade_samples:
                    fade_factor = (total_samples - i) / fade_samples  # Fade-out
                else:
                    fade_factor = 1.0  # Full amplitude

                # Calculate the sample value for the chord
                sample_value = sum(amplitude * fade_factor * math.sin(phases[j]) for j in range(len(chord)))
                sample_value /= len(chord)  # Normalize by number of frequencies in the chord

                # Append the sample to the buffer
                samples.append(struct.pack('<h', int(sample_value)))

                # Update phases for each frequency
                for j in range(len(chord)):
                    phases[j] += phase_increments[j]
                    if phases[j] > 2 * math.pi:
                        phases[j] -= 2 * math.pi

            # Write samples for the chord in one go
            wav_file.writeframes(b''.join(samples))

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time

    # Calculate minutes, seconds, and milliseconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)

    print(f"File saved as {downloads_path}")
    print(f"Time taken to generate the file: {minutes} minutes, {seconds} seconds, {milliseconds} milliseconds")


# Function to play the audio file
def play_audio_file(filename):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
    if os.path.exists(downloads_path):
        print(f"Playing {downloads_path}...")
        winsound.PlaySound(downloads_path, winsound.SND_FILENAME)
    else:
        print("File not found. Please generate the file first.")


# Main function to run the program
def main():
    frequencies_filename = "frequencies.txt"
    durations_filename = "durations.txt"

    frequencies = read_frequencies(frequencies_filename)
    durations = read_durations(durations_filename)

    print("Select an option:")
    print("1. Generate audio file")
    print("2. Play audio file")
    choice = input("Enter your choice (1 or 2): ")

    filename = "Chroma_sink_to_the_deep_sea_world.wav"

    if choice == '1':
        generate_song(filename, frequencies, durations)
    elif choice == '2':
        play_audio_file(filename)
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
