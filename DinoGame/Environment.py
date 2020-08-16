from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from DinoGame.Utils import Util

chromebrowser_path = "D:\\Git\\Baram Project\\2020_2\\resource\\chromedriver.exe"
init_script = "document.getElementsByClassName('runner-canvas')[0].id = 'runner-canvas'"


class Game:
    def __init__(self, custom_config=True):
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--mute-audio")
        self.browser = webdriver.Chrome(executable_path=chromebrowser_path, options=chrome_options)
        self.browser.set_window_position(x=-10, y=0)
        self.browser.get('chrome://dino')
        self.browser.execute_script("Runner.config.ACCELERATION=0")
        self.browser.execute_script(init_script)
        self.browser.implicitly_wait(30)
        self.browser.maximize_window()

    def get_crashed(self):
        return self.browser.execute_script("return Runner.instance_.crashed")

    def get_playing(self):
        return self.browser.execute_script("return Runner.instance_.playing")

    def restart(self):
        self.browser.execute_script("Runner.instance_.restart()")

    def press_up(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)

    def press_down(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)

    def press_right(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)

    def get_score(self):
        score_array = self.browser.execute_script("return Runner.instance_.distanceMeter.digits")
        score = ''.join(score_array)
        return int(score)

    def get_highscore(self):
        score_array = self.browser.execute_script("return Runner.instance_.distanceMeter.highScore")
        i = 0
        for i in range(len(score_array)):
            if score_array[i] == '':
                break
        score_array = score_array[i:]
        score = ''.join(score_array)
        return int(score)

    def pause(self):
        return self.browser.execute_script("return Runner.instance_.stop()")

    def resume(self):
        return self.browser.execute_script("return Runner.instance_.play()")

    def end(self):
        self.browser.close()


class Game_state:
    def __init__(self, agent, game, generation_score):
        self.util = Util()
        self._agent = agent
        self.dinoGame = game
        self._display = self.util.show_img()
        self._display.__next__()
        self.generation_score = generation_score

    def get_state(self, actions):
        score = self.dinoGame.get_score()
        high_score = self.dinoGame.get_highscore()

        reward = 0.1
        is_over = False
        if actions[0] == 1:
            self._agent.jump()
        elif actions[1] == 1:
            self._agent.duck()
        elif actions[2] == 1:
            self._agent.DoNothing()

        image = self.util.screenshot(self.dinoGame.browser)
        self._display.send(image)

        if self._agent.is_crashed():
            self.generation_score.append(score)
            time.sleep(0.1)
            self.dinoGame.restart()
            reward = -1
            is_over = True

        image = self.util.image_to_tensor(image)
        return image, reward, is_over, score, high_score