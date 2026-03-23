from enum import Enum


class COORD(Enum):
    """Class to represent the type of coordinates"""
    LONLAT = 'LONLAT'
    UTM = 'UTM'
    WorldMercator = 'WorldMercator'


def get_params_coords(coord_type):
    if coord_type == COORD.UTM:
        var_x = 'xmin'
        var_y = 'ymin'
        var_dx = 'dx'
        var_dy = 'dy'
        var_nx = 'nx'
        var_ny = 'ny'
    else:
        var_x = 'lonmin'
        var_y = 'latmin'
        var_dx = 'dlon'
        var_dy = 'dlat'
        var_nx = 'nlon'
        var_ny = 'nlat'

    return var_x, var_y, var_dx, var_dy, var_nx, var_ny