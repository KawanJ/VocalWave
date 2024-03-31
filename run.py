import argparse
import Audio_Mode.audio as audio

# Command Line Arguments
parser = argparse.ArgumentParser(description='VocalWave')
parser.add_argument('--no-activation', action='store_true', help='Flag to disable activation keyword in audiomode')
args = parser.parse_args()

if args.no_activation:
    audio.start_audio_mode_without_activation()
else:
    audio.start_audio_mode()
