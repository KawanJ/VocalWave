import pyautogui

action_to_keyboard_mapping = {
    "play" : ["space"],
    "pause" : ["space"],
    "next song" : ["alt", "right"],
    "previous song" : ["alt", "left"],
    "raise volume" : ["alt", "up"],
    "lower volume" : ["alt", "down"],
    "like" : ["alt", "shift", "b"],
    "shuffle" : ["alt", "s"],
    "repeat" : ["alt", "r"]
}

def command_to_action(command):
    if command not in action_to_keyboard_mapping.keys():
        return "Invalid Command"
    pyautogui.hotkey(action_to_keyboard_mapping[command])
    return "Command executed successfully"