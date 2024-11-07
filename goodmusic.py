import math
import wave
import struct
import os
import winsound


# Function to read data from a text file
def read_values_from_file(filename):
    """
    Reads a list of float values from a text file.
    Each line in the file should contain one number.
    """
    values = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                values.append(float(line.strip()))
            except ValueError:
                print(f"Warning: Could not convert line to float: {line.strip()}")
    return values


# Function to generate a tone series with variable durations
def generate_variable_duration_tone_series(filename, frequencies, durations, sample_rate=44100, amplitude=32767):
    """
    Generates an audio file from a list of frequencies with variable durations.
    :param filename: Name of the .wav file to save
    :param frequencies: List of frequencies in Hz
    :param durations: List of durations for each frequency in seconds
    :param sample_rate: Number of samples per second (Hz)
    :param amplitude: Amplitude of the waveform (maximum for 16-bit audio)
    """
    # Check that frequencies and durations lists are of the same length
    if len(frequencies) != len(durations):
        print("Error: The frequencies and durations lists must have the same length.")
        return

    # Construct full path to the Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

    # Open a new .wav file in write mode
    with wave.open(downloads_path, 'w') as wav_file:
        # Set audio parameters: 1 channel, 2 bytes per sample, sample rate, etc.
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)

        # Initialize the phase to ensure continuity across frequency changes
        phase = 0.0

        # Generate wave data for each frequency
        for frequency, duration in zip(frequencies, durations):
            # Total number of samples for this tone
            total_samples = int(sample_rate * duration)

            # Calculate the phase increment per sample for the current frequency
            phase_increment = (2 * math.pi * frequency) / sample_rate

            # Generate samples for the current frequency, maintaining continuity
            for i in range(total_samples):
                # Calculate the sample value based on the phase
                sample_value = amplitude * math.sin(phase)
                # Increment the phase, wrapping around at 2 * pi to avoid overflow
                phase += phase_increment
                if phase > 2 * math.pi:
                    phase -= 2 * math.pi
                # Write the sample as a 16-bit signed integer
                wav_file.writeframes(struct.pack('<h', int(sample_value)))

    print(f"File saved as {downloads_path}")


# Function to play the audio file
def play_audio_file(filename):
    """
    Plays the specified .wav file from the Downloads folder.
    :param filename: Name of the .wav file to play
    """
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
    if os.path.exists(downloads_path):
        print(f"Playing {downloads_path}...")
        winsound.PlaySound(downloads_path, winsound.SND_FILENAME)
    else:
        print("File not found. Please generate the file first.")


# Main function to run the program
def main():
    # Specify the filenames for the frequencies and durations
    frequencies_filename = "frequencies.txt"
    durations_filename = "durations.txt"

    # Read frequencies and durations from files
    frequencies = read_values_from_file(frequencies_filename)
    durations = read_values_from_file(durations_filename)

    # Menu for user choice
    print("Select an option:")
    print("1. Generate audio file")
    print("2. Play audio file")
    choice = input("Enter your choice (1 or 2): ")

    filename = "tones_from_file.wav"

    if choice == '1':
        # Generate the audio file
        generate_variable_duration_tone_series(filename, frequencies, durations)
    elif choice == '2':
        # Play the audio file
        play_audio_file(filename)
    else:
        print("Invalid choice. Please enter 1 or 2.")


# Run the main function
if __name__ == "__main__":
    main()
