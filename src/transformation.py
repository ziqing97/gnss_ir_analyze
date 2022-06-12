'''
This script provides several function to do the
transformation between differennt coordinate
systems
'''

# pylint: disable=invalid-name
import math
SEMIMAJOR_AXIS = 6.3781370e6
ECCENTRICITY = 0.011068213498220

def xyz2latlon(x,y,z):
    '''
    Transformation from xyz system
    into lat, lon, h
    Args:
        x,y,z: coordinates in xyz system
    '''

    h_threshold = 0.001
    phi_threshold = math.pi / (3600 * 180)
    lon = math.atan2(y,x)
    p = math.sqrt(x**2 + y**2)
    h0 = 0
    phi0 = math.atan2(z, (p * (1 - ECCENTRICITY**2)))
    n0 = SEMIMAJOR_AXIS / (1 - (ECCENTRICITY**2) * (math.sin(phi0)**2))
    h1 = p / math.cos(phi0) - n0
    phi1 = math.atan2(z * (n0+h1), (p * (n0 * (1-ECCENTRICITY**2) + h1)))
    while (abs(h1-h0) > h_threshold) | (abs(phi1-phi0) > phi_threshold):
        phi0 = phi1
        h0 = h1
        n0 = SEMIMAJOR_AXIS / math.sqrt(1 - ECCENTRICITY**2 * (math.sin(phi0)**2))
        h1 = p / math.cos(phi0) - n0
        phi1 = math.atan2(z * (n0 + h1), (p * (n0 * (1 - ECCENTRICITY**2) + h1)))
    lat = phi1
    height = h1
    return (lat, lon, height)
