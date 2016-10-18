import unittest


class TestSeismicCalculations(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.eureka = SeismicStation('Eureka, CA', (40.8021, -124.1637))
        self.elko = SeismicStation('Elko, NV', (40.8324, -115.7631))
        self.vegas = SeismicStation('Las Vegas, NV', (36.1699, -115.1398))

        self.event1 = StationEvent("08:00:00", "08:00:49", 250)
        self.event2 = StationEvent("08:00:00", "08:01:12", 50)
        self.event3 = StationEvent("08:00:00", "08:01:04", 100)

        self.eureka.add_event(self.event1)
        self.elko.add_event(self.event2)
        self.vegas.add_event(self.event3)

        self.eq = Earthquake(self.eureka, self.elko, self.vegas)

    def test_haversine(self):
        pass

    def test_parse_station_time(self):
        pass

    def test_calculate_epicenter(self):
        """
        """
        self.assertEqual(self.eq.calc_epicenter(), (35.72362494709903, -121.68306381403882))
        self.eq.print_report()
