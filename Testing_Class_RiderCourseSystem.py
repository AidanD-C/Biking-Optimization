from Class_RiderCourseSystem import *
from Class_Rider import *
from Classes_Courses import *
from Class_RiderState import *


def test_euler_step_forward():
    """Testing RiderCourseSystem.euler_step_forward on some random input values."""

    initial_state = RiderState(distance=10.0, velocity=7.0, force=100.0, an_energy=3000.0)

    rider = Rider(
        initial_state,
        weight=70.0,
        bike_weight=10.0,
        cross_area=0.4,
        drag_coef=0.7,
        max_force=1000.0,
    )

    course = QuadraticHill(course_length=1000.0, end_percentage=14.0)

    system = RiderCourseSystem(rider, course)

    expected = RiderState(distance=10.7, velocity=7.113338, force=100.0, an_energy=2930.0)

    system.euler_step_forward()

    actual = system.rider.state

    try:
        assert actual == expected
        assert system.time == 0.1
        assert system.rider.last_state.force == system.rider.state.force
    except AssertionError:
        print("test_euler_step_forward -- FAIL! --")
    else:
        print("test_euler_step_forward -- pass")


test_euler_step_forward()
