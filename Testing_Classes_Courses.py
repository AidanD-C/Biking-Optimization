from Classes_Courses import *

"""
Template:

def test_...() -> None:
    '''Docstring'''

    def elefunc(x: float) -> float:
        return x**4
    
    def slopefunc(x: float) -> float:
        return x**4
    
    course = ...(5.0, elefunc, slopefunc)

    try:
        assert ... == ...
    except (AssertionError):
        print("test_... -- FAIL! --")
    else:
        print("test_... -- pass")

test_...()
"""

def test_Course_init() -> None:
    '''Testing Course.__init__ to make sure the course is set up correctly.'''

    def elefunc(x: float) -> float:
        return x**4
    
    def slopefunc(x: float) -> float:
        return x**4
    
    course = Course(5.0, elefunc, slopefunc)

    try:
        assert course.COURSE_LENGTH == 5.0
        assert course.dist_vs_ele == elefunc
        assert course.dist_vs_slope == slopefunc
    except (AssertionError):
        print("test_Course_init -- FAIL! --")
    else:
        print("test_Course_init -- pass")

test_Course_init()



def test_IdealCourse_elevation() -> None:
    """Testing IdealCourse.elevation on a simple function."""

    def elefunc(x: float) -> float:
        return x**4
    
    def slopefunc(x: float) -> float:
        return x**4
    
    course = IdealCourse(5.0, elefunc, slopefunc)

    try:
        assert course.dist_vs_ele(2.0) == 16.0
    except (AssertionError):
        print("test_IdealCourse_elevation -- FAIL! --")
    else:
        print("test_IdealCourse_elevation -- pass")

test_IdealCourse_elevation()



def test_IdealCourse_slope() -> None:
    """Testing IdealCourse.slope on a simple function."""
    
    def elefunc(x: float) -> float:
        return x**4
    
    def slopefunc(x: float) -> float:
        return x**4
    
    course = IdealCourse(5.0, elefunc, slopefunc)

    try:
        assert course.dist_vs_slope(2.0) == 16.0
    except (AssertionError):
        print("test_IdealCourse_slope -- FAIL! --")
    else:
        print("test_IdealCourse_slope -- pass")

test_IdealCourse_slope()



def test_QuadraticHill_init() -> None:
    '''Testing QuadraticHill.__init__ to make sure the course is set up correctly.'''
    
    course = QuadraticHill(10.0, 14.0)

    try:
        assert course.COURSE_LENGTH == 10.0
        assert course.END_PERCENTAGE == 14.0
        assert isinstance(course.dist_vs_ele, types.FunctionType)
        assert isinstance(course.dist_vs_slope, types.FunctionType)
    except (AssertionError):
        print("test_QuadraticHill_init -- FAIL! --")
    else:
        print("test_QuadraticHill_init -- pass")

test_QuadraticHill_init()



def test_QuadraticHill_dist_vs_ele() -> None:
    '''Testing QuadraticHill.dist_vs_ele to make sure it is set up correctly.'''
    
    course = QuadraticHill(10.0, 14.0)

    try:
        assert course.dist_vs_ele(0.0) == 0.0
        assert course.dist_vs_ele(10.0) == 0.7
        assert course.dist_vs_ele(5.0) == 0.175
    except (AssertionError):
        print("test_QuadraticHill_dist_vs_ele -- FAIL! --")
    else:
        print("test_QuadraticHill_dist_vs_ele -- pass")

test_QuadraticHill_dist_vs_ele()



def test_QuadraticHill_dist_vs_slope() -> None:
    '''Testing QuadraticHill.dist_vs_slope to make sure it is set up correctly.'''
    
    course = QuadraticHill(10.0, 14.0)

    try:
        assert course.dist_vs_slope(0.0) == 0.0
        assert course.dist_vs_slope(10.0) == 0.14
        assert course.dist_vs_slope(5.0) == 0.07
    except (AssertionError):
        print("test_QuadraticHill_dist_vs_slope -- FAIL! --")
    else:
        print("test_QuadraticHill_dist_vs_slope -- pass")

test_QuadraticHill_dist_vs_slope()