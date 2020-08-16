import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self):

        self.number_of_actions = 3
        self.gamma = 0.99   # 할인율
        self.final_epsilon = 0.0001
        self.initial_epsilon = 0.1
        self.replay_memory = 50000
        self.minibatch_size = 32
        self.observation = 100  # 훈련전에 관찰할 timesteps
        self.number_of_iterations = 5000000
        self.learning_rate = 1e-4

        super(DQN, self).__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(4, 32, 8, 4),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 4, 2),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, 1),
            nn.ReLU(inplace=True)
        )
        self.fc_layer = nn.Sequential(
            nn.Linear(3136, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, self.number_of_actions)  # output의 크기는 할 수 있는 액션의 갯수
        )

    def forward(self, x):
        out = self.layer(x)
        out = out.view(out.size()[0], -1)
        out = self.fc_layer(out)
        return out


# https://eda-ai-lab.tistory.com/404
# http://www.gisdeveloper.co.kr/?p=8443
def init_weights(m):
    if type(m) == nn.Conv2d or type(m) == nn.Linear:
        torch.nn.init.uniform(m.weight, -0.01, 0.01)
        m.bias.data.fill_(0.01) # 편차를 0.01로 초기화
