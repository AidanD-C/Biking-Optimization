import Class_RiderState as RS
import copy


class Rider:
    """
    A class representing a bicycle rider.

    Attributes:
    - state: Current state of the rider.
    - last_state: Last state of the rider. This is initialized to all zero except the force is the same as the initial state.
    - INITIAL_STATE: The initial state of the rider. The distance attribute of INITIAL_STATE should be zero.
    - WEIGHT: weight of the rider in kilograms.
    - BIKE_WEIGHT: weight of the rider's bike in kilograms.
    - CROSS_AREA: rough crossectional area of the rider and bike combined in meters squared.
    - DRAG_COEF: coefficient of drag of the rider.
    - ENERGY_BUDGET: Total amount of energy avalable to the rider over the course of the ride in joules.
    - MAX_FORCE: Maximum possible force the rider can put out in Newtons.
    - MAX_JERK: Maximum possible change in acceleration the cyclist can achieve in one second in meters/second^3.
    - AVG_VELOCITY: Roughly the average velocity of the rider in meters/second.
    - AVG_VELOCTIY_ON_FLAT: Roughly the average velocity the rider can achieve on flat terrain in meters/second
    - AVG_FORCE: Roughly the average velocity output of the rider in Newtons.
    """

    state: RS.RiderState
    last_state: RS.RiderState

    INITIAL_STATE: RS.RiderState
    WEIGHT: float
    BIKE_WEIGHT: float
    CROSS_AREA: float
    DRAG_COEF: float
    ENERGY_BUDGET: float
    MAX_FORCE: float
    MAX_JERK: float
    AVG_VELOCITY: float
    AVG_VELOCITY_ON_FLAT: float
    AVG_FORCE: float

    def __init__(
        self,
        initial_state: RS.RiderState,
        weight: float,
        bike_weight: float,
        cross_area: float,
        drag_coef: float,
        max_force: float,
        max_jerk: float,
        avg_velocity: float,
        avg_velocity_on_flat: float,
    ) -> None:
        """Initialize a new Rider"""

        self.WEIGHT = weight
        self.BIKE_WEIGHT = bike_weight
        self.CROSS_AREA = cross_area
        self.DRAG_COEF = drag_coef
        self.ENERGY_BUDGET = initial_state.an_energy
        self.MAX_FORCE = max_force
        self.INITIAL_STATE = initial_state
        self.state = copy.copy(initial_state)
        self.last_state = RS.RiderState()
        self.last_state.force = self.INITIAL_STATE.force
        self.MAX_JERK = max_jerk
        self.AVG_VELOCITY = avg_velocity
        self.AVG_VELOCITY_ON_FLAT = avg_velocity_on_flat
        # 1.2 is just a rough average air density
        # self.AVG_FORCE = 0.5 * 1.2 * drag_coef * cross_area * avg_velocity_on_flat**2
        self.AVG_FORCE = 100.0
