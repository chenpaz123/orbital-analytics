from skyfield.api import load
# שימוש ב-Loader של Skyfield כדי לוודא גישה לרשת והורדת נתונים
ts = load.timescale()
print(f"✅ Environment Secured & Ready. Current Time: {ts.now()}")