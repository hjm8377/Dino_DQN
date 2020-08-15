from DinoGame.Agent import Game, DinoAgent

game = Game()
dino = DinoAgent(game)
for i in range(3):
    dino.jump()