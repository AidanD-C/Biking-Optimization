from Class_Rider import *

"""
Template:

def test_...() -> None:
    '''Docstring'''
    
    rider = Rider(WEIGHT = 80.0, BIKE_WEIGHT = 7.0, CROSS_AREA = 0.4, DRAG_COEF = 0.7)

    try:
        assert ... == ...
    except (AssertionError):
        print("test_... -- FAIL! --")
    else:
        print("test_... -- pass")

test_...()
"""


def test_Rider_init() -> None:
    """Testing Rider.__init__ to make sure the rider is set up correctly."""

    initial_state = RiderState(1.0, 3.0, 5.0, 7.0)

    rider = Rider(
        initial_state,
        weight=80.0,
        bike_weight=10.0,
        cross_area=0.4,
        drag_coef=0.7,
        max_force=1000.0,
    )

    try:
        assert rider.state == initial_state
        assert rider.last_state == RiderState()
        assert rider.INITIAL_STATE == initial_state
        assert rider.WEIGHT == 80.0
        assert rider.BIKE_WEIGHT == 10.0
        assert rider.CROSS_AREA == 0.4
        assert rider.DRAG_COEF == 0.7
        assert rider.ENERGY_BUDGET == 7.0
        assert rider.MAX_FORCE == 1000.0
    except AssertionError:
        print("test_Rider_init -- FAIL! --")
    else:
        print("test_Rider_init -- pass")


test_Rider_init()
