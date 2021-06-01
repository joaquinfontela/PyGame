import json

with open("Config/config.json") as configFile:
    CONFIGS = json.load(configFile)


def updateColorTheme(colorTheme):
    with open("Config/config.json") as configFile:
        CONFIGS = json.load(configFile)
        CONFIGS["theme"] = colorTheme
        json.dump(CONFIGS)
