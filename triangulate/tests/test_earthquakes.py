import unittest
from triangulate.earthquakes import StationEvent, SeismicStation, Earthquake


class TestSeismicCalculations(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.eureka = SeismicStation('Eureka, CA', (40.8021, -124.1637))
        self.elko = SeismicStation('Elko, NV', (40.8324, -115.7631))
        self.vegas = SeismicStation('Las Vegas, NV', (36.1699, -115.1398))

        self.event1 = StationEvent("00:00:00", "00:00:49", 250)
        self.event2 = StationEvent("00:00:00", "00:01:12", 50)
        self.event3 = StationEvent("00:00:00", "00:01:04", 100)

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
        # self.eq.print_report()

    def test_geocoded_data(self):
        eureka = SeismicStation('Eureka, CA, USA', (40.8020712, -124.1636729))
        elko = SeismicStation('Elko, NV 89801, USA', (40.8324211, -115.7631232))
        vegas = SeismicStation('Las Vegas, NV, USA', (36.1699412, -115.1398296))

        event1 = StationEvent("00:00:00", "00:00:49", 250.00)
        event2 = StationEvent("00:00:00", "00:01:12", 50.00)
        event3 = StationEvent("00:00:00", "00:01:04", 100.00)

        eureka.add_event(event1)
        elko.add_event(event2)
        vegas.add_event(event3)

        eq = Earthquake(eureka, elko, vegas)
        result = eq.calc_epicenter()
        self.assertEqual(result, (35.7237783153985, -121.68303250512152))
