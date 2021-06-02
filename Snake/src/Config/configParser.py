import json

with open("Config/config.json") as configFile:
    CONFIGS = json.load(configFile)


def updateColorTheme(colorTheme):
    with open("Config/config.json", "r") as configFile:
        CONFIGS = json.load(configFile)
        CONFIGS["current_theme"] = colorTheme
    with open("Config/config.json", "w") as configFile:
        json.dump(CONFIGS, configFile)


def updateSpeed(speed):
    with open("Config/config.json", "r") as configFile:
        CONFIGS = json.load(configFile)
        CONFIGS["speed_diameters_per_second"] = speed
    with open("Config/config.json", "w") as configFile:
        json.dump(CONFIGS, configFile)
