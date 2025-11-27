import React, { useState } from "react";
import { Viewer } from "resium";
import SatelliteEntity from "./SatelliteEntity";
import SatelliteControls from "./SatelliteControls";

function App() {
  // זה הזיכרון המרכזי של האפליקציה. כברירת מחדל הוא ריק (null)
  const [currentTLE, setCurrentTLE] = useState(null);

  return (
    <div style={{ position: "relative", width: "100%", height: "100vh" }}>
      {/* 1. ממשק השליטה - מעדכן את הזיכרון */}
      <SatelliteControls onTrack={(data) => setCurrentTLE(data)} />

      {/* 2. הגלובוס - מציג את הזיכרון */}
      <Viewer full timeline={false} animation={false}>
        {/* נציג לוויין רק אם המשתמש הזין נתונים */}
        {currentTLE && <SatelliteEntity tleData={currentTLE} />}
      </Viewer>
    </div>
  );
}

export default App;
