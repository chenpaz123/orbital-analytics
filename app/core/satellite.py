from skyfield.api import EarthSatellite, load, wgs84
from app.schemas.satellite_models import SatellitePosition
from datetime import datetime


class SatelliteManager:
    def __init__(self):
        # טעינת נתונים אסטרונומיים (Caching של קבצים כבדים)
        self.ts = load.timescale()

    def calculate_position(
        self, tle_line1: str, tle_line2: str, name: str
    ) -> SatellitePosition:
        """
        מחשב מיקום לוויין בזמן אמת ומחזיר אובייקט מאומת.
        """
        try:
            # 1. יצירת אובייקט לוויין של Skyfield
            satellite = EarthSatellite(tle_line1, tle_line2, name, self.ts)

            # 2. קביעת הזמן הנוכחי
            t = self.ts.now()

            # 3. חישוב המיקום בחלל (Geocentric)
            geocentric = satellite.at(t)
            # 4. המרת המיקום לקואורדינטות גאוגרפיות
            subpoint = wgs84.subpoint(geocentric)
            lat = subpoint.latitude
            lon = subpoint.longitude
            height = subpoint.elevation

            # החזרת המידע דרך המודל של Pydantic (וזה מבצע ולידציה אוטומטית!)
            return SatellitePosition(
                sat_name=name,
                latitude=lat.degrees,  # וודא שאתה שולף את המעלות ולא את האובייקט
                longitude=lon.degrees,
                altitude_km=height.km,
                timestamp=t.utc_datetime(),
            )

        except Exception as e:
            # ב-Production נרצה לרשום את זה ל-Logger
            raise ValueError(f"Failed to calculate orbit: {str(e)}")


# דוגמה לבדיקה עצמית (כשתריץ את הקובץ ישירות)
if __name__ == "__main__":
    # TLE של תחנת החלל הבינלאומית (ISS) - זה משתנה כל הזמן, אבל זה טוב לבדיקה
    L1 = "1 25544U 98067A   24028.56385799  .00014603  00000+0  26359-3 0  9997"
    L2 = "2 25544  51.6401 199.6483 0004951 281.4287 186.2238 15.49815049436856"

    manager = SatelliteManager()
    pos = manager.calculate_position(L1, L2, "ISS")
    print(pos)
    # הפלט צריך להיות משהו כמו: sat_name='ISS' latitude=... longitude=...
