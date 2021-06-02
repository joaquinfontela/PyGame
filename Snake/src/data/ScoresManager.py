import json
import time


class ScoresManager:

    def save(self, id, score, level):
        with open("data/scores.json", "r") as scoresFile:
            scores = json.load(scoresFile)
            currentTime = time.gmtime()
            data = {
                "score": score,
                "date_time": f"{currentTime.tm_year}/{currentTime.tm_mon}/{currentTime.tm_mday}"
            }
            scores["level"][str(level)][str(id)] = data
        with open("data/scores.json", "w") as scoresFile:
            json.dump(scores, scoresFile)
