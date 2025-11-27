# 1. Base Image: שימוש בגרסה רזה של פייתון (Linux Based)
FROM python:3.11-slim

# 2. הגדרת משתני סביבה לאופטימיזציה של פייתון
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. יצירת תיקיית עבודה בתוך הקונטיינר
WORKDIR /app

# 4. התקנת תלויות (Dependencies)
# אנחנו מעתיקים *רק* את ה-requirements קודם.
# למה? כדי שדוקר ישמור את השלב הזה ב-Cache.
# אם תשנה רק את הקוד שלך ולא את הספריות, הוא לא יצטרך להתקין הכל מחדש.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. העתקת שאר הקוד
COPY . .

# 6. חשיפת הפורט (דוקומנטציה בלבד, לא פותח בפועל)
EXPOSE 8000

# 7. פקודת ההרצה
# שים לב: --host 0.0.0.0 הוא קריטי!
# בלי זה, הקונטיינר יקשיב רק לעצמו ולא נוכל לגשת אליו מבחוץ.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]