import Class_RiderCourseSystem as RCS
import Class_NeuralNetwork as NN
import Helper_Functions as HF
import Classes_Rewards_Penalties as RP
import matplotlib.pyplot as plt
import numpy as np
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


class DataPoint:
    """The data points that will be in the experience replay.

    Attributes:
    - start_state: The state which the system starts in. Will take an action from here.
    - action: An integer between -10 and 10. This is proportional to the change in force from state to state by:
              new force = last force + (rider weight) * (rider max jerk) * (system DT) * 1/10 * action
    - reward: The reward for achieving the result state.
    - result_state: The state resulting from being in state start_state and taking action action.
    """

    start_state: torch.tensor
    action: int
    reward: float
    result_state: torch.tensor

    def __init__(
        self,
        start_state: torch.tensor,
        action: int,
        reward: float,
        result_state: torch.tensor,
    ) -> None:
        """Initialize the data point."""
        self.start_state = start_state
        self.action = action
        self.reward = reward
        self.result_state = result_state


class ExperienceReplay:
    """
    A collection of data points collected from the Q_network interacting with the physical system.

    Attributes:
    - experience_library: The collection of data points.
    """

    experience_library: list[DataPoint]
    system: RCS.RiderCourseSystem
    Q_network: NN.NeuralNetwork
    reward_bundle: RP.RewardBundle
    EPSILON: float

    def __init__(
        self,
        system: RCS.RiderCourseSystem,
        Q_network: NN.NeuralNetwork,
        reward_bundle: RP.RewardBundle,
        epsilon: float,
    ) -> None:
        self.experience_library = []
        self.system = system
        self.Q_network = Q_network
        self.reward_bundle = reward_bundle
        self.EPSILON = epsilon

    def build(self) -> None:
        """
        Builds the experience_library by having the Q_Network interact with the system.
        Important Note: need to be able to go a little past the finish line of the course because of the while loop structure.
        The build is stopped when the rider passes the finish line, or when the cutoff time is passed, or when the rider abilities are violated.
        """

        self.experience_library = []

        system = self.system

        weight = system.rider.BIKE_WEIGHT + system.rider.WEIGHT
        MIN_FORCE_CHANGE = weight * system.rider.MAX_JERK * system.DT * 1.0 / 10.0

        system.reset()

        while system.rider.state.distance < system.course.COURSE_LENGTH:
            start_state = system.model_format_curr_state()  # FIXME repeating this for each iteration as well as the result_state = system.model_format_curr_state() line is redundant.

            if system.time == 0.0:  # FIXME This is just a quick fix that is needed because otherwise, the force applied going from the first state to the second state is not the initial force.
                action = 0
            else:
                action = HF.epsilon_greedy_action(self.Q_network, start_state, epsilon=self.EPSILON)

            last_force = (start_state[2].item() * system.rider.MAX_FORCE) + system.rider.AVG_FORCE

            force_from_action = last_force + MIN_FORCE_CHANGE * action

            system.rider.state.force = force_from_action

            system.euler_step_forward()
            # the state of the system has changed!

            result_state = system.model_format_curr_state()

            try:
                reward = self.reward_bundle.reward()
            except RP.SevereMistakeError:
                reward = self.reward_bundle.SEVERE_MISTAKE_PENALTY
                data_point = DataPoint(start_state, action, reward, result_state)
                self.experience_library.append(data_point)
                break

            data_point = DataPoint(start_state, action, reward, result_state)
            self.experience_library.append(data_point)

    def plot(self) -> None:
        """
        Plots the force and energy as funcs of distance.
        Specifically this prints the start states of the experience_library and the last_force from the resulting state.
        """

        r = self.system.rider
        rs = self.system.rider.state
        c = self.system.course

        distance_array = np.array([])
        force_array = np.array([])
        energy_array = np.array([])

        for data_point in self.experience_library:
            distance = data_point.start_state[0].item()
            force = data_point.result_state[2].item()
            an_energy = data_point.start_state[3].item()

            # undoing the model state format as found in class ridercoursesystem
            distance = distance * (0.5 * c.COURSE_LENGTH) + (0.5 * c.COURSE_LENGTH)
            force = (force * r.MAX_FORCE) + r.AVG_FORCE
            an_energy = an_energy * (0.5 * r.ENERGY_BUDGET) + (0.5 * r.ENERGY_BUDGET)

            distance_array = np.append(distance_array, distance)
            force_array = np.append(force_array, force)
            energy_array = np.append(energy_array, an_energy)

        fig, axs = plt.subplots(2)

        axs[0].plot(distance_array, force_array)
        axs[0].set_title("force vs distance")

        axs[1].plot(distance_array, energy_array)
        axs[1].set_title("energy vs distance")

        fig.suptitle("Full Q_network Rollout:")
        fig.tight_layout()

        plt.show(block=False)
        plt.pause(0.001)

    def random_batch_plus_last(self, batch_size) -> list[torch.tensor]:
        """
        Returns a random batch of size batch_size of datapoints from self.experience_library plus the last data point.
        But the return is not a list of data points but it a list of tensors such that at some given index in each tensor,
        each element at that index in each tensor corresponds to the same data point.
        """

        sublst = HF.random_sublist_plus_last(self.experience_library, size=batch_size)

        output = []

        sublst_starts = []
        sublst_actions = []
        sublst_rewards = []
        sublst_results = []
        for data_point in sublst:
            sublst_starts.append(data_point.start_state)
            sublst_actions.append(torch.tensor(data_point.action))
            sublst_rewards.append(torch.tensor(data_point.reward))
            sublst_results.append(data_point.result_state)

        output.extend(
            [
                torch.stack(sublst_starts).to(device),
                torch.stack(sublst_actions).to(device),
                torch.stack(sublst_rewards).to(device),
                torch.stack(sublst_results).to(device),
            ]
        )

        return output
