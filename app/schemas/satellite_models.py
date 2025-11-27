from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime

# --- Input Model (הבקשה שהמשתמש שולח) ---
class SatelliteTLERequest(BaseModel):
    """
    המידע שהלקוח חייב לשלוח כדי לקבל חישוב.
    """
    sat_name: str = Field(..., min_length=1, description="Satellite Name")
    tle_line1: str = Field(..., pattern=r"^1 \d{5}[UWC] .*", description="First line of TLE")
    tle_line2: str = Field(..., pattern=r"^2 \d{5} .*", description="Second line of TLE")

model_config = ConfigDict(
       json_schema_extra = {
            "example": {
                "sat_name": "ISS (ZARYA)",
                "tle_line1": "1 25544U 98067A   24028.56385799  .00014603  00000+0  26359-3 0  9997",
                "tle_line2": "2 25544  51.6401 199.6483 0004951 281.4287 186.2238 15.49815049436856"
            }
        })

# --- Output Model (התשובה שאנחנו מחזירים) ---
class SatellitePosition(BaseModel):
    """
    Data Contract: מגדיר בדיוק איך נראה מיקום לוויין.
    """
    sat_name: str = Field(..., description="The name of the satellite")
    latitude: float = Field(..., ge=-90, le=90, description="Degrees (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Degrees (-180 to 180)")
    altitude_km: float = Field(..., gt=0, description="Height above WGS84 ellipsoid in km")
    timestamp: datetime = Field(..., description="Calculation time (UTC)")

    class Config:
        json_schema_extra = {
            "example": {
                "sat_name": "ISS (ZARYA)",
                "latitude": 32.0853,
                "longitude": 34.7818,
                "altitude_km": 420.5,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }