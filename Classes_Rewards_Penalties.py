import Class_RiderCourseSystem as RCS
import Helper_Functions as HF
import math


class RewardPolicy:
    """
    A geral policy of assigning a reward to how an agent (not necessarily a Q_network) interacts with a system.
    This is an Abstract Class and should not be instantiated.

    Attributes:
    - system: The system which the agent in interacting with.
    """

    system: RCS.RiderCourseSystem

    def __init__(self, system: RCS.RiderCourseSystem) -> None:
        self.system = system

    def reward(self) -> float:
        """The reward assignment function."""
        raise NotImplementedError


class EvenMilestones(RewardPolicy):
    """
    A reward policy where a constant reward is given for each time the agent moves a certain number of meters toward the end of the course.
    One can say that ever SPACING meters there is a "milestone" where the agent recieves a reward.

    Attrbutes:
    - BASE_REWARD
    - SPACING
    """

    BASE_REWARD: float
    SPACING: float

    def __init__(
        self,
        system: RCS.RiderCourseSystem,
        base_reward: float,
        spacing: float,
    ):
        RewardPolicy.__init__(self, system)
        self.BASE_REWARD = base_reward
        self.SPACING = spacing

    def reward(self) -> float:
        """
        Checks if a milestone has been passed. If so, returns BASE_REWARD for every milestone passed.
        Otherwise, returns 0.0.
        """

        curr_dist = self.system.rider.state.distance
        last_dist = self.system.rider.last_state.distance

        milestones_passed = HF.count_multiples(start=last_dist, end=curr_dist, num=self.SPACING)

        if milestones_passed > 0:
            return self.BASE_REWARD * milestones_passed

        return 0.0


class SeverePenalty(RewardPolicy):
    """
    This is the worst possible penalty. Either no reward is given,
    or a SeverMistakeError is raised which will end the experience replay build for example.
    This is an abstract class and should not be instantiated.
    """

    def penalty_conditions(self) -> bool:
        raise NotImplementedError

    def reward(self) -> float:
        if self.penalty_conditions():
            raise SevereMistakeError
        else:
            return 0.0


class RiderAbilitiesViolation(SeverePenalty):
    """
    A severe penalty which is triggered by violating the abilities of the rider.
    """

    def penalty_conditions(self) -> bool:
        """Returns true if the rider's an_energy goes below zero or if the rider's force exceeds their max force."""

        state = self.system.rider.state

        if state.an_energy < 0.0 or state.force > self.system.rider.MAX_FORCE:
            # print("RIDER ABILITIES VIOLATION!")
            return True
        else:
            return False


class TimeViolation(SeverePenalty):
    """
    A severe penalty which is triggered by the cut off time being violatied.
    """

    CUTOFF_TIME: float

    def __init__(self, system: RCS.RiderCourseSystem, cutoff_time: float):
        super().__init__(system)
        self.CUTOFF_TIME = cutoff_time

    def penalty_conditions(self) -> bool:
        "returns true if the time is greater than self.CUTOFF_TIME."

        if self.system.time > self.CUTOFF_TIME:
            print("CUTOFF TIME VIOLATION!")
            return True
        else:
            return False


class UnderMinForceViolation(SeverePenalty):
    """A severe penalty that is triggered by the rider's force going less that MIN_FORCE."""

    MIN_FORCE: float

    def __init__(self, system: RCS.RiderCourseSystem, min_force: float) -> None:
        super().__init__(system)
        self.MIN_FORCE = min_force

    def penalty_conditions(self) -> bool:
        """Returns True is the rider's force is less than self.MIN_FORCE."""

        if self.system.rider.state.force < self.MIN_FORCE:
            print("LESS THAN MIN FORCE VIOLATION!")
            return True
        else:
            return False


class UnderMinEnergyViolation(SeverePenalty):
    """A severe penalty that is triggered by the rider's energy going less that MIN_ENERGY."""

    MIN_ENERGY: float

    def __init__(self, system: RCS.RiderCourseSystem, min_energy: float) -> None:
        super().__init__(system)
        self.MIN_ENERGY = min_energy

    def penalty_conditions(self) -> bool:
        """Returns True is the rider's force is less than self.MIN_FORCE."""

        if self.system.rider.state.an_energy < self.MIN_ENERGY:
            print("LESS THAN MIN ENERGY VIOLATION!")
            return True
        else:
            return False


class GoingBackwardsViolation(SeverePenalty):
    """A severe penalty that is triggered by the rider moving backwards."""

    def penalty_conditions(self) -> bool:
        """Returns True if the riders distance has decreased since their last state."""

        if self.system.rider.state.distance < self.system.rider.last_state.distance:
            print("GOING BACKWARDS VIOLATION!")
            return True
        else:
            return False


class ForceBoundsPenalty(RewardPolicy):
    """
    A penalty reward policy which gives a penalty if the
    rider goes over the max force or under zero.
    This is a softer version of the severe penalty for force violation above.
    """

    scaling: float

    def __init__(self, system: RCS.RiderCourseSystem, scaling: float) -> None:
        super().__init__(system)
        self.scaling = scaling

    def reward(self) -> float:
        current_force = self.system.rider.state.force
        max_force = self.system.rider.MAX_FORCE

        if current_force > max_force:
            x = current_force - max_force
            return -self.scaling * x**2
        elif current_force < 0:
            x = abs(current_force)
            # print(-self.scaling * x**2)
            return -self.scaling * x**2
        else:
            return 0.0


class UnderZeroEnergyPenalty(RewardPolicy):
    """
    A penalty reward policy which gives a penalty if the
    rider's energy drops below zero. The penalty scales linearly with slope self.scaling
    This is a softer version of the severe penalty for energy violation above.
    """

    scaling: float

    def __init__(self, system: RCS.RiderCourseSystem, scaling: float) -> None:
        super().__init__(system)
        self.scaling = scaling

    def reward(self) -> float:
        if self.system.rider.state.an_energy < 0:
            x = abs(self.system.rider.state.an_energy)
            return -self.scaling * x**2
        else:
            return 0.0


class CompletionReward(RewardPolicy):
    """
    A reward policy which delivers a reward at the end of the course.
    """

    completion_reward: float

    def __init__(self, system: RCS.RiderCourseSystem, completion_reward: float) -> None:
        super().__init__(system)
        self.completion_reward = completion_reward

    def reward(self):
        if self.system.rider.state.distance > self.system.course.COURSE_LENGTH:
            return self.completion_reward
        else:
            return 0.0


class FinalTimeReward(RewardPolicy):
    """
    A reward policy which delivers a reward at the end of the course which is higher
    if the rider completes the course in less time than expected.
    For the future: could make the scaling non linear so being further under the expected time is even better.
    """

    expected_time: float

    def __init__(self, system: RCS.RiderCourseSystem, expected_time: float) -> None:
        super().__init__(system)
        self.expected_time = expected_time

    def reward(self):
        if self.system.rider.state.distance > self.system.course.COURSE_LENGTH:
            # print(self.expected_time - self.system.time)
            return self.expected_time - self.system.time
        else:
            return 0.0


class RewardBundle:
    """A collection of reward and penalty policies which all together decide
    the full policy for how the agent will be rewarded or penalized for its interactions with the system.
    """

    bundle: list[RewardPolicy]
    SEVERE_MISTAKE_PENALTY: float

    def __init__(self, bundle: list[RewardPolicy], severe_mistake_penalty: float) -> None:
        self.bundle = bundle
        self.SEVERE_MISTAKE_PENALTY = severe_mistake_penalty

    def reward(self) -> float:
        """Returns the full reward based on all the policies included in the bundle.
        This is called a reward but should be thought of as both rewards and penalties combined into one.
        Reward is just a conventional name."""

        reward = 0.0

        for policy in self.bundle:
            reward += policy.reward()

        return reward


class SevereMistakeError(Exception):
    pass
