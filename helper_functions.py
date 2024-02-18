import pyautogui

action_to_keyboard_mapping = {
    "play" : ["space"],
    "pause" : ["space"],
    "next song" : ["ctrl", "right"],
    "previous song" : ["ctrl", "left"],
}

def command_to_action(command):
    if command not in action_to_keyboard_mapping.keys():
        return "Invalid Command"
    pyautogui.hotkey(action_to_keyboard_mapping[command])
    return "Command executed successfully"