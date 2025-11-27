from app.core.satellite import SatelliteManager


def test_calculate_position():
    manager = SatelliteManager()
    sat_name= "ISS (ZARYA)"
    tle_line1= "1 25544U 98067A   24028.56385799  .00014603  00000+0  26359-3 0  9997"
    tle_line2= "2 25544  51.6401 199.6483 0004951 281.4287 186.2238 15.49815049436856"
    position = manager.calculate_position(tle_line1, tle_line2, sat_name) 
    assert position.sat_name == sat_name
    assert -90 <= position.latitude <= 90
    assert -180 <= position.longitude <= 180
    assert position.altitude_km > 100
    assert position.timestamp is not None