from fastapi import APIRouter, HTTPException, status
from app.core.satellite import SatelliteManager
from app.schemas.satellite_models import SatelliteTLERequest, SatellitePosition

router = APIRouter()

# אתחול המנוע פעם אחת (Singleton) ברמת המודול
# ב-Production מערכות מורכבות יותר משתמשים ב-Dependency Injection, אבל זה מספיק כרגע.
manager = SatelliteManager()

@router.post("/position", response_model=SatellitePosition)
async def get_satellite_position(request: SatelliteTLERequest):
    """
    מקבל TLE ומחזיר את המיקום הנוכחי בזמן אמת.
    """
    try:
        # הקריאה למנוע הפיזיקלי שבנינו בשלב הקודם
        position = manager.calculate_position(
            tle_line1=request.tle_line1,
            tle_line2=request.tle_line2,
            name=request.sat_name
        )
        return position
    
    except ValueError as e:
        # תרגום שגיאת לוגיקה לשגיאת HTTP תקינה (400 Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # שגיאה לא צפויה בשרת (500 Internal Server Error)
        print(f"CRITICAL ERROR: {e}") # כאן נחבר בעתיד לוגר אמיתי
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Calculation Error"
        )