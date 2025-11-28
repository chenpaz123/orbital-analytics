from skyfield.api import EarthSatellite, load, wgs84
from app.schemas.satellite_models import SatellitePosition, OrbitPath
from datetime import timedelta
import numpy as np


class SatelliteManager:
    def __init__(self):
        # טעינת נתונים אסטרונומיים (Caching של קבצים כבדים)
        self.ts = load.timescale()

    def calculate_orbit_path(
        self, tle_line1: str, tle_line2: str, name: str, duration_minutes: int = 90
    ) -> OrbitPath:
        """
        מחשב את המסלול העתידי של הלוויין ל-X דקות הקרובות.
        """
        satellite = EarthSatellite(tle_line1, tle_line2, name, self.ts)

        # 1. קביעת נקודת ההתחלה והסיום
        # אנחנו רוצים לראות קצת אחורה (עבר) ובעיקר קדימה (עתיד)
        t0 = self.ts.now()
        start_time = t0.utc_datetime() - timedelta(minutes=45)  # 45 דקות אחורה

        # 2. יצירת סדרת זמנים (Vectorization)
        # ניצור מערך של זמנים: כל דקה, למשך 90 דקות (סה"כ מסלול הקפה מלא בערך)
        minutes = np.arange(0, duration_minutes)
        time_array = self.ts.utc(
            start_time.year,
            start_time.month,
            start_time.day,
            start_time.hour,
            start_time.minute + minutes,
        )

        # 3. חישוב כל המיקומים בפעולה אחת מהירה!
        geocentric = satellite.at(time_array)
        subpoints = wgs84.subpoint(geocentric)

        # 4. המרת התוצאות לרשימה של אובייקטים
        positions = []

        # כאן אנחנו עוברים על התוצאות ומכניסים לרשימה
        # שים לב ש-subpoints.latitude.degrees עכשיו מחזיר מערך של מספרים, לא מספר בודד
        for i in range(len(minutes)):
            pos = SatellitePosition(
                sat_name=name,
                latitude=subpoints.latitude.degrees[i],
                longitude=subpoints.longitude.degrees[i],
                altitude_km=subpoints.elevation.km[i],
                timestamp=time_array[i].utc_datetime(),
            )
            positions.append(pos)

        return OrbitPath(sat_name=name, coordinates=positions)

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

    def calculate_orbit_path(
        self, tle_line1: str, tle_line2: str, name: str, duration_minutes: int = 120
    ) -> OrbitPath:
        """
        מחשב את המסלול העתידי של הלוויין ל-X דקות הקרובות.
        """
        satellite = EarthSatellite(tle_line1, tle_line2, name, self.ts)

        # 1. קביעת נקודת ההתחלה והסיום
        # אנחנו רוצים לראות קצת אחורה (עבר) ובעיקר קדימה (עתיד)
        t0 = self.ts.now()
        start_time = t0.utc_datetime() - timedelta(minutes=45)  # 45 דקות אחורה

        # 2. יצירת סדרת זמנים (Vectorization)
        # ניצור מערך של זמנים: כל דקה, למשך 90 דקות (סה"כ מסלול הקפה מלא בערך)
        minutes = np.arange(0, duration_minutes)
        time_array = self.ts.utc(
            start_time.year,
            start_time.month,
            start_time.day,
            start_time.hour,
            start_time.minute + minutes,
        )

        # 3. חישוב כל המיקומים בפעולה אחת מהירה!
        geocentric = satellite.at(time_array)
        subpoints = wgs84.subpoint(geocentric)

        # 4. המרת התוצאות לרשימה של אובייקטים
        positions = []

        # כאן אנחנו עוברים על התוצאות ומכניסים לרשימה
        # שים לב ש-subpoints.latitude.degrees עכשיו מחזיר מערך של מספרים, לא מספר בודד
        for i in range(len(minutes)):
            pos = SatellitePosition(
                sat_name=name,
                latitude=subpoints.latitude.degrees[i],
                longitude=subpoints.longitude.degrees[i],
                altitude_km=subpoints.elevation.km[i],
                timestamp=time_array[i].utc_datetime(),
            )
            positions.append(pos)

        return OrbitPath(sat_name=name, coordinates=positions)


# דוגמה לבדיקה עצמית (כשתריץ את הקובץ ישירות)
if __name__ == "__main__":
    # TLE של תחנת החלל הבינלאומית (ISS) - זה משתנה כל הזמן, אבל זה טוב לבדיקה
    L1 = "1 25544U 98067A   24028.56385799  .00014603  00000+0  26359-3 0  9997"
    L2 = "2 25544  51.6401 199.6483 0004951 281.4287 186.2238 15.49815049436856"

    manager = SatelliteManager()
    pos = manager.calculate_position(L1, L2, "ISS")
    print(pos)
    # הפלט צריך להיות משהו כמו: sat_name='ISS' latitude=... longitude=...
