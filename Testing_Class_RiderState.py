from Class_RiderState import *

"""
Template:

def test_...() -> None:
    '''Docstring'''
    
    state = RiderState(distance = 5000.0, velocity = 7.5, force = 300.0, an_energy = 3000.0)

    try:
        assert ... == ...
    except (AssertionError):
        print("test_... -- FAIL! --")
    else:
        print("test_... -- pass")

test_...()
"""


def test_RiderState_init() -> None:
    """Testing RiderState.__init__ to make sure the rider state is set up correctly."""

    state = RiderState(distance=5000.0, velocity=7.5, force=300.0, an_energy=3000.0)

    try:
        assert state.distance == 5000.0
        assert state.velocity == 7.5
        assert state.force == 300.0
        assert state.an_energy == 3000.0
    except AssertionError:
        print("test_RiderState_init -- FAIL! --")
    else:
        print("test_RiderState_init -- pass")


test_RiderState_init()


def test_RiderState_str() -> None:
    """Testing RiderState.__str__ to make sure the printed representation of the state is correct."""

    state = RiderState(distance=5000.0, velocity=7.5, force=300.0, an_energy=3000.0)

    try:
        assert (
            state.__str__()
            == "Rider State: [distance: 5000.0, velocity: 7.5, force: 300.0, an_energy: 3000.0]"
        )
    except AssertionError:
        print("test_RiderState_str -- FAIL! --")
    else:
        print("test_RiderState_str -- pass")


test_RiderState_str()
