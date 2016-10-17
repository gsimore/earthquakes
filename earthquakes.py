"""
'Earth is shaking'

Monty   >> "OMG AN EARTHQUAKE"
You     >> "Duck!!"

'House crashes down'

Monty   >> "Where on earth did that come from?"
You     >> "I don't know yet Monty, but we'd better find out."

'Synchronous evil laughter'

First, let's determine how far away the earthquake was.
    1. Obtain P- and S-wave arrival times from three locations.
    2. Calculate the difference between P- and S-wave arrival times at each location (seconds).
    3. Use the difference in arrival time to determine distance (in km) from the earthquake at each location.

Let's also determine the earthquake's magnitude (Richter scale):
    4. Determine the amplitude of the strongest wave (mm).
    5. Use the difference in arrival time and the amplitude to determine the magnitude of the earthquake.

Now, let's locate the epicenter:
    6. Draw radius around each location using the distance found in 3.
    7. Determine where the 3 circles intersect.

** reminder, GPS N and E are +, S and W are -
*** advanced option: write program that analyzes the seismograms for you,
    determines p- and s-wave arrival times and amplitude of strongest wave.

event = (p-arrival-time, s-arrival-time, max_amp)
station = ('location', coords)
coords = (lat, lon)  # lat, lon in degrees

>>> eureka = SeismicStation('Eureka, CA', (40.8021, -124.1637))
>>> elko = SeismicStation('Elko, NV', (40.8324, -115.7631))
>>> vegas = SeismicStation('Las Vegas, NV', (36.1699, -115.1398))

>>> event1 = StationEvent("08:00:00", "08:00:49", 250)
>>> event2 = StationEvent("08:00:00", "08:01:12", 50)
>>> event3 = StationEvent("08:00:00", "08:01:04", 100)

>>> event1.calc_distance()
>>> event2.calc_distance()
>>> event3.calc_distance()

>>> eureka.add_event(event1)
>>> elko.add_event(event2)
>>> vegas.add_event(event3)

>>> the_great_san_antonio_eq = Earthquake(eureka, elko, vegas)
>>> the_great_san_antonio_eq.calc_epicenter()


where
d = distance to earthquake
tS = S-wave arrival time
tP = P-wave ""
vS = velocity of S-wave
vP = velocity of p-wave

d = (tS-tP/(1/vS-1/vP)

"""


from datetime import datetime
from math import log, sin, cos, atan2, asin, degrees, radians, sqrt, pow
import numpy

earthR = 6371  # kilometers


def haversine(point1, point2):
    """
    Calculates the distance between two points on the earth.
    >>> haversine((52.2296756, 21.0122287), (52.406374, 16.9251681))
    278.4581750754194
    """
    lat1, lat2 = radians(point1[0]), radians(point2[0])
    lon1, lon2 = radians(point1[1]), radians(point2[1])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = (sin(delta_lat/2)**2) + (cos(lat1)*cos(lat2)*sin(delta_lon/2)**2)
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = earthR * c
    return distance


class SeismicStation:

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.latitude = coords[0]
        self.longitude = coords[1]
        self.events = list()

    def add_event(self, event):
        """
        Adds a single event to the events list.
        """
        self.events.append(event)
        return self

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class StationEvent:
    """
    An object pertaining to a single seismic event at a single seismic recording
    station.
    """
    VS = float(3.67)  # avg velocity of s-waves in CA crustal rocks (km/sec)
    VP = float(6.34)  # avg velocity of p-waves in CA crustal rocks (km/sec)
    # Your conversion factor from arrival time difference (sec) to distance km
    Vsp = (VS * VP)/(VP - VS)
    
    def __init__(self, p_arrival_time, s_arrival_time, max_amplitude):
        p_time = datetime.strptime(p_arrival_time, "%H:%M:%S")
        s_time = datetime.strptime(s_arrival_time, "%H:%M:%S")
        delta = s_time - p_time

        self.p_arrival_time = p_time
        self.s_arrival_time = s_time
        self.delta_sec = delta.seconds
        self.max_amplitude = max_amplitude  # in millimeters
        self.Vsp = Vsp
        # Method resolution order below
        self.dist_to_eq = None
        self.magnitude = None
        self.seismic_moment = None
        self.energy = None

    def __str__(self):
        message = "{} | Tsp(s): {}, Amp(mm): {}"
        return message.format(self.p_arrival_time, self.delta_sec, self.max_amplitude)

    def __repr__(self):
        message = "{} | Tsp(s): {}, Amp(mm): {}"
        return message.format(self.p_arrival_time, self.delta_sec, self.max_amplitude)

    def calc_distance(self):
        """
        Calculates the distance from the epicenter of the earthquake from
        one seismic station. Using assumption of average velocity in California
        crustal rocks for Vsp. (adaptable for location of stations or earthquake)
        """
        self.dist_to_eq = float(self.delta_sec * self.Vsp) # distance in km
        return self.dist_to_eq


    def calc_magnitude(self):
        """
        Calculates the magnitude of the Earthquake on the Richter Scale.
        source: http://crack.seismo.unr.edu/ftp/pub/louie/class/100/magnitude.html
        """
        result = log(self.max_amplitude) + (3*log(8*self.delta_sec)-2.92)
        self.magnitude = result
        return self.magnitude # richter scale 1 - 5

    def calc_seismic_moment(self):
        """
        Calculates the seismic moment (dyne-cm) of the earthquake based upon relationship
        with Magnitude. source: https://goo.gl/lLpS9x
        """
        result = 10 ** ((3/2)*(self.magnitude+16))
        self.seismic_moment = result
        return self.seismic_moment # in units of dyne-cm

    def calc_seismic_energy(self, method='moment'):
        """
        Calculates the amount of Energy (ergs) released by the earthquake, based on
        either the magnitude or the seismic moment.
        """
        if method == 'magnitude':
            """ E = 10 ^ (11.8 + (1.5 * Magnitude)) """
            result = 10 ** (11.8+(1.5*self.magnitude))

        elif method == 'moment':
            """ E = Moment / 20,000 """
            result = self.seismic_moment / 20000

        else:
            print("Error, available methods are 'moment' or 'magnitude'.")
            result = None

        self.energy = result
        return self.energy

    def print_report(self):
        """
        Prints out the results. :)
        """
        message = 'The difference between p- and s-wave arrival times was: {} seconds.\
                   \nThe distance to the earthquake is {} kilometers.'
        print(message.format(self.delta_sec, self.dist_to_eq))


class Earthquake:
    """
    Compiles data from at least three seismic station events to determine
    the epicenter of the earthquake.
    """

    def __init__(self, *args):
        self.station1 = args[0]
        self.station2 = args[1]
        self.station3 = args[2]
        self.epicenter = None

    def calc_epicenter(self):
        # assumes elevation = 0, TODO: incorporate elevation of seismic stations
        LatA = radians(self.station1.coords[0])  # lat in radians
        LonA = radians(self.station1.coords[1])  # lon in radians
        rA = self.station1.events[0].dist_to_eq  # get the circle radius
        LatB = radians(self.station2.coords[0])
        LonB = radians(self.station2.coords[1])
        rB = self.station2.events[0].dist_to_eq
        LatC = radians(self.station3.coords[0])
        LonC = radians(self.station3.coords[1])
        rC = self.station3.events[0].dist_to_eq

        # using authalic sphere, if considering ellipsoid, this step is slightly different
        # Convert geodetic Lat/Long to ECEF xyz
        #   Convert Lat/Long(radians) to ECEF
        xA = earthR *(cos(LatA) * cos(LonA))
        yA = earthR *(cos(LatA) * sin(LonA))
        zA = earthR *(sin(LatA))

        xB = earthR *(cos(LatB) * cos(LonB))
        yB = earthR *(cos(LatB) * sin(LonB))
        zB = earthR *(sin(LatB))

        xC = earthR *(cos(LatC) * cos(LonC))
        yC = earthR *(cos(LatC) * sin(LonC))
        zC = earthR *(sin(LatC))

        P1 = numpy.array([xA, yA, zA])
        P2 = numpy.array([xB, yB, zB])
        P3 = numpy.array([xC, yC, zC])

        #from wikipedia
        #transform to get circle 1 at origin
        #transform to get circle 2 on x axis
        ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
        i = numpy.dot(ex, P3 - P1)
        ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
        ez = numpy.cross(ex,ey)
        d = float(numpy.linalg.norm(P2 - P1))
        j = numpy.dot(ey, P3 - P1)

        #from wikipedia
        #plug and chug using above values
        x = (pow(rA,2) - pow(rB,2) + pow(d,2))/(2*d)
        y = ((pow(rA,2) - pow(rC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

        # only one case shown here
        z = numpy.sqrt(pow(rA,2) - pow(x,2) - pow(y,2))
        #triPt is an array with ECEF x,y,z of trilateration point
        triPt = P1 + x*ex + y*ey + z*ez

        #convert back to lat/long from ECEF
        #convert to degrees
        lat = degrees(asin(triPt[2] / earthR))
        lon = degrees(atan2(triPt[1],triPt[0]))
        epicenter = (lat, lon)

        self.epicenter = epicenter
        return self.epicenter
