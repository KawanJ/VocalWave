import pyautogui

action_to_keyboard_mapping = {
    "play" : ["space"],
    "pause" : ["space"],
    "stop" : ["space"],
    "next" : ["ctrl", "right"],
    "previous" : ["ctrl", "left", "ctrl", "left"],
    "restart" : ["ctrl", "left"],
    "raise" : ["ctrl", "up"],
    "increase" : ["ctrl", "up"],
    "lower" : ["ctrl", "down"],
    "decrease" : ["ctrl", "down"],
    "like" : ["alt", "shift", "b"],
    "shuffle" : ["ctrl", "s"],
    "repeat" : ["ctrl", "r"],
}

def command_to_action(command):
    if command not in action_to_keyboard_mapping.keys():
        return "Invalid Command"
    pyautogui.hotkey(action_to_keyboard_mapping[command])
    return "Command executed successfully"