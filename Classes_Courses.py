import types


class Course:
    """A class representing a cycling course on a given day. This is an Abstract Class and should not be instantiated.

    Attributes:
    - COURSE_LENGTH: The length of the course in meters.
    - dist_vs_ele: The function which defines the course. If you input distance "along the x axis" it will output the elevaiton.
    - dist_vs_slope: The function which defines the slope of the course. If you input distance "along the x axis" it will output the slope.
    """

    COURSE_LENGTH: float
    dist_vs_ele: types.FunctionType | list[list] | None
    dist_vs_slope: types.FunctionType | None

    def __init__(
        self,
        course_length: float,
        dist_vs_ele: types.FunctionType | list[list] | None = None,
        dist_vs_slope: types.FunctionType | None = None,
    ) -> None:
        """Initializing the course."""
        self.COURSE_LENGTH = course_length
        self.dist_vs_ele = dist_vs_ele
        self.dist_vs_slope = dist_vs_slope

    def elevtion(self, distance: float) -> float:
        return NotImplementedError

    def slope(self, distance: float) -> float:
        raise NotImplementedError


class IdealCourse(Course):
    """An idealized course which is based on the graph of a mathematical function R -> R. self.dist_vs_ele is of type callable."""

    def elevation(self, distance: float) -> float:
        """Returns elevation at distance based on the self.dist_vs_ele function."""
        return self.dist_vs_ele(distance)

    def slope(self, distance: float) -> float:
        """
        If slope function is avalable, will return slope at distance.
        If not (if self.dist_vs_slope is None) then should be able to find derivative approximation.
        """
        if self.dist_vs_slope is not None:
            return self.dist_vs_slope(distance)
        else:
            raise NotImplementedError


class PointwiseCourse(Course):
    """A course which is defined by many different points individual points instead of continuously. self.dist_vs_ele is of type list[list]."""

    pass


class QuadraticHill(IdealCourse):
    """An idealized hill which starts flat, ends with a percentage of END_PERCENTAGE and transitions quadratically"""

    END_PERCENTAGE: float

    def __init__(self, course_length: float, end_percentage: float) -> None:
        """
        Initializing the quadratic hill ideal course."""

        Course.__init__(self, course_length)

        self.END_PERCENTAGE = end_percentage

        def elevation(distance: float) -> float:
            return self.END_PERCENTAGE * distance**2 / (200 * self.COURSE_LENGTH)

        self.dist_vs_ele = elevation

        def slope(distance: float) -> float:
            return self.END_PERCENTAGE * distance / (100 * self.COURSE_LENGTH)

        self.dist_vs_slope = slope
