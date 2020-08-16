class DinoAgent:
    def __init__(self, game):
        self.dinoGame = game
        self.jump()    # 처음에 게임 시작하기 위해 점프

    def is_running(self):
        return self.dinoGame.get_crashed()

    def jump(self):
        self.dinoGame.press_up()

    def duck(self):
        self.dinoGame.press_down()

    def Donothing(self):
        self.dinoGame.press_right()



