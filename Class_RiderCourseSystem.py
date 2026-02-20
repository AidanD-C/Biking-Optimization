import Class_RiderState as RS
import Class_Rider as R
import Classes_Courses as C
import Helper_Functions as HF
import torch
import copy

device = "cuda" if torch.cuda.is_available() else "cpu"


class RiderCourseSystem:
    """
    The full physical system of the rider and the course.
    note that the energy does not increase if the rider travels backwards or if the force is negative

    Attributes:
    - rider: The rider in the system.
    - course: The course of the system.
    - time: Current time of the system in seconds. Initialized to zero.
    - DT: The time step for each update of the system in seconds. Default is 0.1s
    - AIR_DENSITY: Density of air in kilograms/(meters cubed). Default is 1.2 kg/m^3
    """

    rider: R.Rider
    course: C.Course
    time: float

    DT: float
    AIR_DENSITY: float

    def __init__(
        self,
        rider: R.Rider,
        course: C.Course,
        dt: float = 0.1,
        air_density: float = 1.2,
    ) -> None:
        """Initializing the system."""
        self.course = course
        self.rider = rider
        self.time = 0.0
        self.DT = dt
        self.AIR_DENSITY = air_density

    def euler_step_forward(self) -> None:
        """Steps forward the system."""

        self.time += self.DT

        c = self.course
        r = self.rider
        rs = self.rider.state
        r.last_state = copy.copy(rs)

        weight = r.BIKE_WEIGHT + r.WEIGHT

        try:
            rs.distance += rs.velocity * self.DT
            air_term = 1.0 / 2.0 * r.DRAG_COEF * r.CROSS_AREA * self.AIR_DENSITY * rs.velocity**2
            gravity_term = weight * 9.8 * c.slope(r.last_state.distance)
            rs.velocity += 1.0 / weight * (rs.force - air_term - gravity_term) * self.DT

            if rs.distance > r.last_state.distance and rs.force > 0:
                rs.an_energy -= rs.force * (rs.distance - r.last_state.distance)

        except OverflowError:
            print("Over flow error in euler step forward. Last state:")
            print(rs)

    def model_format_curr_state(self) -> torch.tensor:
        """
        Returns a tensor representation of all the information needed by the machine learing model aobut the current state of the full system.

        Not sure if I need to set requires_grad to True or False, setting False for now.
        """

        r = self.rider
        rs = self.rider.state
        c = self.course

        distance = (rs.distance - 0.5 * c.COURSE_LENGTH) / (0.5 * c.COURSE_LENGTH)
        velocity = (rs.velocity - r.AVG_VELOCITY) / HF.m_per_s(100.0)
        last_force = (r.last_state.force - r.AVG_FORCE) / r.MAX_FORCE
        an_energy = (rs.an_energy - 0.5 * r.ENERGY_BUDGET) / (0.5 * r.ENERGY_BUDGET)

        state = [
            distance,
            velocity,
            last_force,
            an_energy,
            c.slope(rs.distance),
            c.slope(rs.distance + 10.0),
            c.slope(rs.distance + 20.0),
            c.slope(rs.distance + 30.0),
            c.slope(rs.distance + 40.0),
            c.slope(rs.distance + 50.0),
            c.slope(rs.distance + 60.0),
            c.slope(rs.distance + 70.0),
            c.slope(rs.distance + 80.0),
            c.slope(rs.distance + 90.0),
            c.slope(rs.distance + 100.0),
            r.MAX_JERK,
            self.DT,
        ]

        return torch.tensor(data=state, dtype=float, device=device, requires_grad=False)

    def reset(self) -> None:
        """Resets the system to its initial state."""

        self.time = 0.0
        self.rider.state = copy.copy(self.rider.INITIAL_STATE)
        self.rider.last_state = RS.RiderState()
        self.rider.last_state.force = self.rider.INITIAL_STATE.force
