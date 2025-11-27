import React, { useEffect, useState } from "react";
import { Entity } from "resium";
import { Cartesian3, Color } from "cesium";

// שים לב: אנחנו מקבלים את tleData כפרמטר (Prop)
const SatelliteEntity = ({ tleData }) => {
  const [position, setPosition] = useState(null);

  useEffect(() => {
    // אם אין מידע, אל תעשה כלום
    if (!tleData) return;

    const fetchPosition = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/position", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(tleData), // שימוש במידע שהגיע מהאבא
        });

        const data = await response.json();

        const cesiumPosition = Cartesian3.fromDegrees(
          data.longitude,
          data.latitude,
          data.altitude_km * 1000
        );

        setPosition(cesiumPosition);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchPosition();
    const interval = setInterval(fetchPosition, 3000);

    return () => clearInterval(interval);
  }, [tleData]); // חשוב! הרץ מחדש את האפקט בכל פעם ש-tleData משתנה

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
