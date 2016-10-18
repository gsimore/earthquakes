# Earthquake Epicenter Calculator

_'Earth is shaking'_

*Monty*   >> "OMG AN EARTHQUAKE"

*You*     >> "Duck!!"

_'House crashes down'_

*Monty*   >> "Where on earth did that come from?"

*You*     >> "I don't know yet Monty, but we'd better find out."

_'Synchronous evil laughter'_

### First, let's determine how far away the earthquake was.
  1. Obtain P- and S-wave arrival times from three locations.
  2. Calculate the difference between P- and S-wave arrival times at each location (seconds).
  3. Use the difference in arrival time to determine distance (in km) from the earthquake at each location.

### Let's also determine the earthquake's magnitude (Richter scale):
  4. Determine the amplitude of the strongest wave (mm).
  5. Use the difference in arrival time and the amplitude to determine the magnitude of the earthquake.

### Now, let's locate the epicenter:
  6. Draw radius around each location using the distance found in 3.
  7. Determine where the 3 circles intersect.

#### reminder, GPS N and E are +, S and W are negative(-)

Advanced option: write program that analyzes the seismograms for you.determines p- and s-wave arrival times and amplitude of strongest wave.

### Formula Variables
```
event = (p-arrival-time, s-arrival-time, max_amp)
station = ('location', coords)
coords = (lat, lon)  # lat, lon in degrees
```

```
d = distance to earthquake
tS = S-wave arrival time
tP = P-wave ""
vS = velocity of S-wave
vP = velocity of p-wave

d = (tS-tP/(1/vS-1/vP)
```
