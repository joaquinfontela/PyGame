import pygame
from model.data.ScoresManager import ScoresManager
from model.TextFormatter.TextFormatter import TextFormatter
from model.Config.configParser import CONFIGS
import time
import model.MainMenu

THEME = CONFIGS["current_theme"]
BACKGROUND_COLOR = CONFIGS["colors"][THEME]["background"]
LOGO_COLOR = CONFIGS["colors"][THEME]["logo"]
SELECTED_COLOR = CONFIGS["colors"][THEME]["selected_option"]
NON_SELECTED_COLOR = CONFIGS["colors"][THEME]["non_selected_option"]
FONT = CONFIGS["font"]

CHANGE_SELECTED_OPTION_SOUND_PATH = CONFIGS["sounds"]["change_selected_option"]
SELECT_OPTION_SOUND_PATH = CONFIGS["sounds"]["select_option"]
pygame.mixer.init()
CHANGE_SELECTED_OPTION_SOUND = pygame.mixer.Sound(
    CHANGE_SELECTED_OPTION_SOUND_PATH)
CHANGE_SELECTED_OPTION_SOUND.set_volume(0.5)
SELECT_OPTION_SOUND = pygame.mixer.Sound(
    SELECT_OPTION_SOUND_PATH)
SELECT_OPTION_SOUND.set_volume(0.5)

N_HIGH_SCORES_TO_SHOW = 5

COLOR_FOR_RANKING = {
    1: [255, 215, 0],
    2: [192, 192, 192],
    3: [205, 127, 50]
}


class HighScoresMenu:

    def __init__(self, window):
        self.window = window
        self.open = True
        self.levelSelected = 1
        self._displayTexts()
        self._loop()

    def _displayTexts(self):
        self.window.screen.fill(BACKGROUND_COLOR)
        title = TextFormatter().formatText("HIGHSCORES", FONT, 90, LOGO_COLOR)
        subtitle = TextFormatter().formatText("SELECT LEVEL:", FONT, 50, LOGO_COLOR)
        level1Title = TextFormatter().formatText("1", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 1 else NON_SELECTED_COLOR)
        level2Title = TextFormatter().formatText("2", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 2 else NON_SELECTED_COLOR)
        level3Title = TextFormatter().formatText("3", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 3 else NON_SELECTED_COLOR)
        level4Title = TextFormatter().formatText("4", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 4 else NON_SELECTED_COLOR)
        level5Title = TextFormatter().formatText("5", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 5 else NON_SELECTED_COLOR)
        level6Title = TextFormatter().formatText("6", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 6 else NON_SELECTED_COLOR)
        level7Title = TextFormatter().formatText("7", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 7 else NON_SELECTED_COLOR)
        level8Title = TextFormatter().formatText("8", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 8 else NON_SELECTED_COLOR)
        level9Title = TextFormatter().formatText("9", FONT, 60,
                                                 SELECTED_COLOR if self.levelSelected % 10 == 9 else NON_SELECTED_COLOR)
        level10Title = TextFormatter().formatText("10", FONT, 60,
                                                  SELECTED_COLOR if self.levelSelected % 10 == 0 else NON_SELECTED_COLOR)
        quitInfo = TextFormatter().formatText("PRESS 'Q' TO GO TO THE MAIN MENU", FONT, 35,
                                              LOGO_COLOR)
        screenWidth, _ = self.window.getDimensions()
        self.window.screen.blit(
            title, (screenWidth/2 - (title.get_rect()[2]/2), 10))
        self.window.screen.blit(
            subtitle, (screenWidth/2 - (subtitle.get_rect()[2]/2), 95))
        self.window.screen.blit(
            level1Title, (1.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level2Title, (2.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level3Title, (3.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level4Title, (4.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level5Title, (5.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level6Title, (6.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level7Title, (7.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level8Title, (8.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level9Title, (9.5 * screenWidth/12, 150))
        self.window.screen.blit(
            level10Title, (10.5 * screenWidth/12, 150))
        self._displayHighscores()
        self.window.screen.blit(
            quitInfo, (screenWidth/2 - (quitInfo.get_rect()[2]/2), 670))
        pygame.display.update()

    def _displayHighscores(self):
        level = self.levelSelected % 10 if self.levelSelected % 10 > 0 else 10
        highestScores = ScoresManager().get_n_HighestScores(level, N_HIGH_SCORES_TO_SHOW)
        for idx, score in enumerate(highestScores):
            scoreRanking = TextFormatter().formatText(
                f"{idx + 1}.", FONT, 70, COLOR_FOR_RANKING.get(
                    idx + 1, LOGO_COLOR)
            )
            id = TextFormatter().formatText(
                f"{score[0][:20]}", FONT, 70, COLOR_FOR_RANKING.get(
                    idx + 1, LOGO_COLOR)
            )
            score = TextFormatter().formatText(
                f"{score[1]}", FONT, 70, COLOR_FOR_RANKING.get(
                    idx + 1, LOGO_COLOR)
            )
            screenWidth, _ = self.window.getDimensions()
            self.window.screen.blit(
                scoreRanking, (screenWidth/6 - (scoreRanking.get_rect()[2]/2), 240 + idx * 85))
            self.window.screen.blit(
                id, (2 * screenWidth/5 - (id.get_rect()[2]/2), 240 + idx * 85))
            self.window.screen.blit(
                score, (3 * screenWidth/4 - (score.get_rect()[2]/2), 240 + idx * 85))

    def _loop(self):
        '''
        Executes the main loop of the main menu,
        which is in charge of identifying which option is selected
        and updating the information graphically in the correct moment.
        '''
        while self.open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self._changeLevelSelected(event.key)
                        self._displayTexts()
                    if event.key == pygame.K_q:
                        model.MainMenu.MainMenu(self.window)
                if event.type == pygame.QUIT:
                    pygame.mixer.Sound.play(SELECT_OPTION_SOUND)
                    time.sleep(0.2)
                    self.open = False
                    self.window.stopRunning()

    def _changeLevelSelected(self, eventKey):
        pygame.mixer.Sound.play(CHANGE_SELECTED_OPTION_SOUND)
        if eventKey == pygame.K_LEFT:
            self.levelSelected -= 1
        else:
            self.levelSelected += 1
