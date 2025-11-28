# 1. Base Image: שימוש בגרסה קלה של Node.js
FROM node:20-alpine

# 2. הגדרת תיקיית עבודה
WORKDIR /app

# 3. העתקת קבצי התלות והתקנה
# (כמו שעשינו ב-Python, כדי לנצל את ה-Caching)
COPY package.json package-lock.json ./
RUN npm install

# 4. העתקת שאר הקוד
COPY . .

# 5. חשיפת הפורט של Vite
EXPOSE 5173

# 6. הרצת השרת
# שים לב: --host הוא קריטי! בלעדיו הקונטיינר לא יהיה נגיש מבחוץ
CMD ["npm", "run", "dev", "--", "--host"]