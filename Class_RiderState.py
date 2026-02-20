class RiderState:
    """
    The current state of a rider.

    Attributes:
    - distance: Distance from the start point "along the x axis" (this is not the arclength distance) in meters. Default is zero.
    - elevation: Elevation of the rider in meters. Default is zero.
    - velocity: Current velocity of the rider in the direction of the course (tangentially to the curve) in meters per second. Default is zero.
    - force: Force being output by the rider along the direction of the course (tangentially to the curve) in Newtons. Default is zero.
    - an_energy: Anarobic energy of the rider. Default is zero.
    """

    distance: float
    velocity: float
    force: float
    an_energy: float

    def __init__(
        self,
        distance: float = 0.0,
        velocity: float = 0.0,
        force: float = 0.0,
        an_energy: float = 0.0,
    ) -> None:
        """Initialize a State."""

        self.distance = distance
        self.velocity = velocity
        self.force = force
        self.an_energy = an_energy

    def __str__(self) -> str:
        """printing the state"""

        return f"Rider State: [distance: {self.distance}, velocity: {self.velocity}, force: {self.force}, an_energy: {self.an_energy}]"

    def __eq__(self, value):
        """Return True if the the two states have the same attributes."""
        return (
            self.distance == value.distance
            and self.velocity == value.velocity
            and self.force == value.force
            and self.an_energy == value.an_energy
        )
