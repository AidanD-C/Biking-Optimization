import torch


class NeuralNetwork(torch.nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden1_size: int,
        hidden2_size: int,
        hidden3_size: int,
        hidden4_size: int,
        output_size: int,
    ):
        super(NeuralNetwork, self).__init__()
        self.layer_1 = torch.nn.Linear(
            in_features=input_size, out_features=hidden1_size
        )
        self.layer_2 = torch.nn.Linear(
            in_features=hidden1_size, out_features=hidden2_size
        )
        self.layer_3 = torch.nn.Linear(
            in_features=hidden2_size, out_features=hidden3_size
        )
        self.layer_4 = torch.nn.Linear(
            in_features=hidden3_size, out_features=hidden4_size
        )
        self.layer_5 = torch.nn.Linear(
            in_features=hidden4_size, out_features=output_size
        )
        self.relu = torch.nn.ReLU()

    def forward(self, input: torch.tensor):
        return self.layer_5(
            self.relu(
                self.layer_4(
                    self.relu(
                        self.layer_3(
                            self.relu(self.layer_2(self.relu(self.layer_1(input))))
                        )
                    )
                )
            )
        )
