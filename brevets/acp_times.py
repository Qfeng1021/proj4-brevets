"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
min_speed = [15, 15, 11.428]
max_speed = [34, 32, 30, 28]
dist = [200, 400, 600, 1000]
min_first_dist = max_speed[0] *min_speed[0] / (max_speed[0] - min_speed[0])
#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#
def calculator(control_dist_km, brevet_dist_km, brevet_start_time, speed):
    start = arrow.get(brevet_start_time, 'YYYY-MM-DD HH:mm')
    i = 1
    cost = 0
    if control_dist_km > 200:
        while min_first_dist <= control_dist_km <= brevet_dist_km:
            if control_dist_km - dist[i] > 0:
                cost = cost + round(((dist[i] - dist[i-1]) / speed[i]) * 60)
                i = i + 1
            else:
                cost = cost + round(((control_dist_km - dist[i-1]) / speed[i]) * 60)
                control_time = start.shift(minutes =+ cost).isoformat(sep = 'T')
                return control_time
    else:
        cost = round((control_dist_km / speed[i-1]) * 60)
        control_time = start.shift(minutes =+ cost).isoformat(sep = 'T')
        return control_time


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    start = arrow.get(brevet_start_time, 'YYYY-MM-DD HH:mm')
    if control_dist_km == 0:
        return start.isoformat(sep = 'T')
    else:
        return calculator(control_dist_km, brevet_dist_km, brevet_start_time, max_speed)




def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    start = arrow.get(brevet_start_time, 'YYYY-MM-DD HH:mm')
    if control_dist_km == 0:
        return start.shift(hours =+ 1).isoformat(sep = 'T')
    elif control_dist_km == 200:
        return start.shift(minutes =+ 13 * 60 + 30).isoformat(sep = 'T')
    else:
        return calculator(control_dist_km, brevet_dist_km, brevet_start_time, min_speed)
