import React, { useEffect, useState } from "react";
import { Entity, PolylineGraphics } from "resium";
import { Cartesian3, Color } from "cesium";

const OrbitPath = ({ tleData }) => {
  // כאן נשמור את רשימת הנקודות המומרות לפורמט של Cesium
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    if (!tleData) return;

    const fetchPath = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/orbit", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(tleData),
        });

        const data = await response.json();

        // המרת המידע הגולמי (Lat/Lon) לרשימה של Cartesian3
        const cesiumPositions = data.coordinates.map((point) =>
          Cartesian3.fromDegrees(
            point.longitude,
            point.latitude,
            point.altitude_km * 1000
          )
        );

        setPositions(cesiumPositions);
      } catch (error) {
        console.error("Error fetching orbit path:", error);
      }
    };

    fetchPath();
    // הערה: כאן אנחנו לא עושים setInterval כי המסלול לא משתנה כל שניה,
    // הוא משתנה רק אם בחרנו לוויין אחר.
  }, [tleData]); // רץ מחדש רק כשהלוויין משתנה

  if (positions.length === 0) return null;

  return (
    <Entity>
      <PolylineGraphics
        positions={positions}
        width={3} // עובי הקו
        material={Color.YELLOW} // צבע בולט
      />
    </Entity>
  );
};

export default OrbitPath;
