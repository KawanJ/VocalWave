import argparse
import Audio_Mode.audio as audio
import Gesture_Mode.gesture as gesture

# Create the parser
parser = argparse.ArgumentParser(description='Process some modes.')

# Add arguments
parser.add_argument('mode', choices=['gesture', 'audio'], help='Select the mode (gesture or audio)')
parser.add_argument('--activation_keyword', help='Activation keyword for audio mode')

# Parse the arguments
args = parser.parse_args()

if args.mode == 'gesture':
    gesture.start_gesture_mode()
elif args.mode == 'audio':
    if args.activation_keyword:
        audio.start_audio_mode()
    else:
        audio.start_audio_mode_without_activation()