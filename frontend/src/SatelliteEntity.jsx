import React, { useEffect, useState } from "react";
import { Entity, useCesium } from "resium"; // <-- הוספנו את useCesium
import { Cartesian3, Color } from "cesium";

const SatelliteEntity = ({ tleData }) => {
  const [position, setPosition] = useState(null);
  const { viewer } = useCesium(); // <-- גישה למנוע של Cesium

  useEffect(() => {
    if (!tleData) return;

    // דגל כדי לדעת אם זו הפעם הראשונה שאנחנו טוענים את הלוויין הזה
    let isFirstLoad = true;

    const fetchPosition = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/position", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(tleData),
        });

        const data = await response.json();

        const cesiumPosition = Cartesian3.fromDegrees(
          data.longitude,
          data.latitude,
          data.altitude_km * 1000
        );

        setPosition(cesiumPosition);

        // --- הוספת הטיסה האוטומטית ---
        if (isFirstLoad && viewer) {
          viewer.camera.flyTo({
            destination: Cartesian3.fromDegrees(
              data.longitude,
              data.latitude,
              15000000 // גובה המצלמה (15,000 ק"מ) - כדי לראות את כל כדור הארץ
            ),
            duration: 2, // משך הטיסה בשניות
          });
          isFirstLoad = false; // כדי שלא יקפיץ את המצלמה בכל רענון של 3 שניות
        }
        // ---------------------------
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchPosition();
    const interval = setInterval(fetchPosition, 3000);

    return () => clearInterval(interval);
  }, [tleData, viewer]); // הוספנו את viewer לתלויות

  if (!position) return null;

  return (
    <Entity
      position={position}
      name={tleData.sat_name}
      point={{ pixelSize: 10, color: Color.RED }}
      description={tleData.sat_name}
    />
  );
};

export default SatelliteEntity;
