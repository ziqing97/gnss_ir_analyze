'''
This script provides several function to do the
transformation between differennt coordinate
systems

Author: Ziqing Yu
Last edited on 10/06/2022
'''

# pylint: disable=invalid-name
# pylint: disable=unused-variable
import numpy

A_WGS84 = 6378137.0
B_WGS84 = 6356752.3142
F_WGS84 = 1/298.257223563
E_WGS84 = numpy.sqrt((A_WGS84*A_WGS84-B_WGS84*B_WGS84)/(A_WGS84*A_WGS84))

def xyz2latlon(x_ecef,y_ecef,z_ecef):
    '''
    Transformation from xyz system
    into lat, lon, h
    Args:
        x,y,z: coordinates in xyz system
    '''

    itera_lat = 10

    lon_ECEF = numpy.arctan(y_ecef/x_ecef)
    p_ECEF = numpy.sqrt(x_ecef*x_ecef+y_ecef*y_ecef)
    lat_ECEF = numpy.arctan((z_ecef/p_ECEF)*((1-E_WGS84*E_WGS84)**(-1)))

    for i in range(itera_lat):
        bajo = numpy.sqrt((A_WGS84*A_WGS84*(numpy.cos(lat_ECEF))**2)\
            + (B_WGS84*B_WGS84*(numpy.sin(lat_ECEF))**2))
        N_ECEF = (A_WGS84*A_WGS84)/bajo
        h_ECEF = (p_ECEF/numpy.cos(lat_ECEF))-N_ECEF
        lat_ECEF = numpy.arctan((z_ecef/p_ECEF) \
            * (1-(E_WGS84*E_WGS84)*(N_ECEF/(N_ECEF+h_ECEF)))**(-1))
    return(lat_ECEF,lon_ECEF,h_ECEF)
