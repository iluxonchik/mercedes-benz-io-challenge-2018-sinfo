"""API endpoints."""

class Endpoint(object):
    API_PREFIX = '/api/'
    VEHICLES = API_PREFIX + 'vehicles/'  # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ

    DEALERS_CLOSEST_LIST = API_PREFIX + 'dealers/' # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ?latitude=LLL?longitude=OOO
    DEALER_CLOSEST = API_PREFIX + 'dealers/closest/' # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ?latitude=LLL?longitude=OOO
    DEALERS_IN_POLYGON = API_PREFIX + 'dealers/polygon/'

    BOOKINGS_CREATE = API_PREFIX + 'bookings/create/' # {first_name, last_name, vehicle_id, pickup_date}
    BOOKINGS_CANCEL = API_PREFIX + 'bookings/cancel/' # {booking_id, reason}
