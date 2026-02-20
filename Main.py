import Class_RiderState as RS
import Class_Rider as R
import Classes_Courses as C
import Class_RiderCourseSystem as RCS
import Class_NeuralNetwork as NN
import Helper_Functions as HF
import Class_ExperienceReplay as ER
import Classes_Rewards_Penalties as RP
import copy
import torch
import matplotlib.pyplot as plt
import numpy as np
import time

device = "cuda" if torch.cuda.is_available() else "cpu"

START_EPSILON = 0.8
EPOCHS = 10000
EPOCHS_BETWEEN_T_NET_UPDATES = 100
# EPSILON_CHANGE_EPOCH_1 = 3700
# EPSILON_CHANGE_EPOCH_2 = 4700


# Setting up the physical system:
initial_state = RS.RiderState(distance=0.0, velocity=7.0, force=100.0, an_energy=50000.0)

rider = R.Rider(
    initial_state,
    weight=87.0,
    bike_weight=7.0,
    cross_area=0.4,
    drag_coef=0.7,
    max_force=1000.0,
    max_jerk=1.0,
    avg_velocity=HF.m_per_s(25.0),
    avg_velocity_on_flat=HF.m_per_s(27.0),
)

course = C.QuadraticHill(course_length=500.0, end_percentage=11.0)

system = RCS.RiderCourseSystem(rider, course)


# Setting up the neural networks:

Q_network = NN.NeuralNetwork(
    input_size=17,
    hidden1_size=18,
    hidden2_size=19,
    hidden3_size=20,
    hidden4_size=21,
    output_size=21,
)

Q_network.to(torch.float64)
Q_network.to(device)

T_network = copy.deepcopy(Q_network)

loss_function = torch.nn.MSELoss()

optimizer = torch.optim.SGD(Q_network.parameters(), lr=0.001)


# Setting up the reward system. Note: at the moment there is only one blanket penalty value for a severe mistake.
reward1 = RP.EvenMilestones(system, base_reward=3.0, spacing=10.0)
reward2 = RP.CompletionReward(system, completion_reward=0.0)
reward3 = RP.UnderMinForceViolation(system, min_force=-100.0)  # severe penalty
reward4 = RP.TimeViolation(system, cutoff_time=500.0)  # severe penalty
reward5 = RP.ForceBoundsPenalty(system, scaling=50.0)
reward6 = RP.UnderZeroEnergyPenalty(system, scaling=2.0)
reward7 = RP.FinalTimeReward(system, expected_time=200.0)
reward8 = RP.UnderMinEnergyViolation(system, min_energy=-2000.0)  # severe penalty
reward9 = RP.GoingBackwardsViolation(system)  # severe penalty

reward_bundle = RP.RewardBundle(
    [reward1, reward2, reward3, reward4, reward5, reward6, reward7, reward8, reward9],
    severe_mistake_penalty=-100.0,
)


# Creating the experience replay

experience_replay = ER.ExperienceReplay(system, Q_network, reward_bundle, epsilon=START_EPSILON)

losses = []

start_time = time.time()

for epoch in range(EPOCHS):

    experience_replay.build()

    # getting a batch from the expertience replay and making sure the batch size is valid.
    batch_size = 30

    if len(experience_replay.experience_library) < batch_size:
        batch_size = len(experience_replay.experience_library)

    batch = experience_replay.random_batch_plus_last(batch_size=batch_size)

    loss = HF.Q_learning_loss(Q_network, T_network, batch, loss_function, gamma=0.1)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if epoch % EPOCHS_BETWEEN_T_NET_UPDATES == 0:
        T_network = copy.deepcopy(Q_network)

    # Changing the epsilon greedy value as the training progresses:
    experience_replay.EPSILON = START_EPSILON * (1.0 - epoch / EPOCHS)

    # printing stuff:
    # print(loss.item())

    # losses.append(loss.item())

    if epoch % EPOCHS_BETWEEN_T_NET_UPDATES == 0:
        print(f"Epoch: {epoch}. Current Loss: {loss.item()} Updating training network.")
        losses.append(loss.item())
        reward4.CUTOFF_TIME += 50

    if epoch % 100 == 0:
        plt.close()
        experience_replay.plot()

print(f"Time taken: {time.time()-start_time} seconds")


fig, ax = plt.subplots()
ax.plot(np.array(losses))
plt.show()
