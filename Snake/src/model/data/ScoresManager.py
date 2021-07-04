import json
import time

SCORES_PATH = "model/data/scores.json"


class ScoresManager:

    def save(self, id, score, level):
        with open(SCORES_PATH, "r") as scoresFile:
            scores = json.load(scoresFile)
            currentTime = time.gmtime()
            data = {
                "score": score,
                "date_time": f"{currentTime.tm_year}/{currentTime.tm_mon}/{currentTime.tm_mday}"
            }
            scores["level"][str(level)][str(id)] = data
        with open(SCORES_PATH, "w") as scoresFile:
            json.dump(scores, scoresFile)

    def get_n_HighestScores(self, level, n):
        with open(SCORES_PATH, "r") as scoresFile:
            scores = json.load(scoresFile)
            levelScores = scores["level"][str(level)]
            levelScores = levelScores.items()
            levelScores = list(map(lambda x: [x[0], x[1]["score"],
                                              x[1]["date_time"]], list(levelScores)))
            return self.getNHighestScoresOfLevel(levelScores, n)

    def getNHighestScoresOfLevel(self, scores, n):
        largestScores = []
        for i in range(n):
            if not scores:
                break
            largestScore = max(scores, key=lambda x: x[1])
            scores.remove(largestScore)
            largestScores.append(largestScore)
        return largestScores

#     def resetScores(self):
#         scores = {"level": {}}
#         for level in range(1, 10+1):
#             scores["level"][str(level)] = {}
#         with open(SCORES_PATH, "w") as scoresFile:
#             json.dump(scores, scoresFile)


# ScoresManager().resetScores()
