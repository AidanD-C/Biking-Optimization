import torch
import Class_NeuralNetwork as NN
import Class_RiderState as RS
import random


def modified_print(model_format_state: torch.tensor, collapse_future_slopes: bool = True) -> None:

    if collapse_future_slopes is True:
        print("System Model State:\n-------------------\n" + f"distance: {model_format_state[0].item()}\n" + f"velocity: {model_format_state[1].item()}\n" + f"last force: {model_format_state[2].item()}\n" + f"an_energy: {model_format_state[3].item()}\n" + f"current slope: {model_format_state[4].item()}\n" + f"future slopes: ...\n" + f"max jerk: {model_format_state[15].item()}\n" + f"time step: {model_format_state[16].item()}\n" + "-------------------\n")
    else:
        print("System Model State:\n-------------------\n" + f"distance: {model_format_state[0].item()}\n" + f"velocity: {model_format_state[1].item()}\n" + f"last force: {model_format_state[2].item()}\n" + f"an_energy: {model_format_state[3].item()}\n" + f"current slope: {model_format_state[4].item()}\n" + f"slope in 10m: {model_format_state[5].item()}\n" + f"slope in 20m: {model_format_state[6].item()}\n" + f"slope in 30m: {model_format_state[7].item()}\n" + f"slope in 40m: {model_format_state[8].item()}\n" + f"slope in 50m: {model_format_state[9].item()}\n" + f"slope in 60m: {model_format_state[10].item()}\n" + f"slope in 70m: {model_format_state[11].item()}\n" + f"slope in 80m: {model_format_state[12].item()}\n" + f"slope in 90m: {model_format_state[13].item()}\n" + f"slope in 100m: {model_format_state[14].item()}\n" + f"max jerk: {model_format_state[15].item()}\n" + f"time step: {model_format_state[16].item()}\n" + "-------------------\n")


def epsilon_greedy_action(Q_network: NN.NeuralNetwork, model_state: torch.tensor, epsilon: float) -> int:
    """
    Returns an action selected by the epsilon greedy policy and the output of Q_network from model_state as the input. Smaller epsilon means smaller chance for a random action.

    Preconditions:
    - 0.0 <= epsilon <= 1.0
    - model_state is same size as input of Q_network
    """
    roll = random.random()

    if roll > epsilon:
        output = Q_network(model_state)
        return torch.argmax(output).item() - 11
    else:
        return random.randrange(-10, 10, 1)


def count_multiples(start: float, end: float, num: float) -> int:
    """Returns the number of multiples of num which lie in between start and end."""

    multiples_in_start = int(start / num)
    multiples_in_end = int(end / num)

    diff_of_multiples = multiples_in_end - multiples_in_start

    return diff_of_multiples


def random_sublist_plus_last(lst: list[any], size: int) -> list[any]:
    """Returns a random subset of elements from from lst without repetition and includes the final element."""

    sublst = random.sample(lst, size)

    final_element = lst[-1]

    if not final_element in sublst:
        sublst.pop(-1)
        sublst.append(final_element)

    return sublst


def Q_learning_loss(
    Q_network: NN.NeuralNetwork,
    T_network: NN.NeuralNetwork,
    batch: list[torch.tensor],
    loss_function: torch.nn.modules.loss,
    gamma: float,
) -> torch.tensor:
    """
    Returns the loss of the batch according to the loss calculation steps for a Q_learning model. Uses loss_function as the final loss function.
    the tensors in batch should already be on the gpu.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"

    batch_size = batch[0].size(dim=0)

    start_states = batch[0]
    actions = batch[1]
    rewards = batch[2]
    result_states = batch[3]

    all_Q_network_Q_values = Q_network(start_states)

    # i need to change how i define the actions because i just minus 11 then add 11 later
    action_indices = actions + 11

    chosen_Q_network_Q_values = []
    # choosing the q values that correspond to the action indices
    for data_point in range(batch_size):
        action_index = action_indices[data_point].item()
        Q_value = all_Q_network_Q_values[data_point][action_index]
        chosen_Q_network_Q_values.append(Q_value)

    chosen_Q_network_Q_values = torch.stack(chosen_Q_network_Q_values).to(device)

    all_training_network_Q_values = T_network(result_states)

    chosen_training_network_Q_values = []
    # choosing only the max q values
    for data_point in range(batch_size):
        Q_value = torch.max(all_training_network_Q_values[data_point])
        chosen_training_network_Q_values.append(Q_value)

    chosen_training_network_Q_values = torch.stack(chosen_training_network_Q_values).to(device)

    target_Q_values = rewards + gamma * chosen_training_network_Q_values

    return loss_function(chosen_Q_network_Q_values, target_Q_values)


def m_per_s(velocity: float) -> float:
    """converts km/h to m/s"""
    return velocity * 1000.0 / 3600.0
