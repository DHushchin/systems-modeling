import random
import math

class Generator:
    """
    A class that generates random values according to different distributions.
    """

    @staticmethod
    def exp(time_mean):
        """
        Generates a random value according to an exponential distribution.
        
        Args:
            time_mean (float): The mean value of the distribution.
        
        Returns:
            float: A random value according to an exponential distribution.
        """
        a = 0
        while a == 0:
            a = random.random()
        a = -time_mean * math.log(a)
        return a

    @staticmethod
    def unif(time_min, time_max):
        """
        Generates a random value according to a uniform distribution.

        Args:
            time_min (float): The minimum value of the random value.
            time_max (float): The maximum value of the random value.

        Returns:
            float: A random value according to a uniform distribution.
        """
        a = 0
        while a == 0:
            a = random.random()
        a = time_min + a * (time_max - time_min)
        return a

    @staticmethod
    def norm(time_mean, time_deviation):
        """
        Generates a random value according to a normal (Gaussian) distribution.

        Args:
            time_mean (float): The mean of the random value.
            time_deviation (float): The standard deviation of the random value.

        Returns:
            float: A random value according to a normal (Gaussian) distribution.
        """
        return time_mean + time_deviation * random.gauss(0, 1)

    @staticmethod
    def empiric(x, y):
        """
        Generates a random value according to an empirical distribution determined by a sequence of points (xi, yi),
        where yi are from the interval (0, 1).

        Args:
            x (list): The array of x-coordinates of points.
            y (list): The array of y-coordinates of points.

        Returns:
            float: A random value according to an empirical distribution.
        
        Raises:
            Exception: If the maximum value in the y array is not 1.0, indicating an illegal array of points.
        """
        n = len(x)
        if y[-1] != 1.0:
            raise Exception("Illegal array of points for empiric distribution")
        r = random.random()

        for i in range(1, n - 1):
            if y[i - 1] < r <= y[i]:
                a = x[i - 1] + (r - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1])
                return a

        a = x[n - 2] + (r - y[n - 2]) * (x[n - 1] - x[n - 2]) / (y[n - 1] - y[n - 2])
        return a
