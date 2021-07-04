import json
CONFIG_PATH = "model/Config/config.json"

with open(CONFIG_PATH) as configFile:
    CONFIGS = json.load(configFile)


def updateColorTheme(colorTheme):
    with open(CONFIG_PATH, "r") as configFile:
        CONFIGS = json.load(configFile)
        CONFIGS["current_theme"] = colorTheme
    with open(CONFIG_PATH, "w") as configFile:
        json.dump(CONFIGS, configFile)


def updateSpeed(speed):
    with open(CONFIG_PATH, "r") as configFile:
        CONFIGS = json.load(configFile)
        CONFIGS["speed_diameters_per_second"] = speed
    with open(CONFIG_PATH, "w") as configFile:
        json.dump(CONFIGS, configFile)
