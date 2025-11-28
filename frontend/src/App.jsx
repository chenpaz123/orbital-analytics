import React, { useState } from "react";
import { Viewer } from "resium";
import SatelliteEntity from "./SatelliteEntity";
import SatelliteControls from "./SatelliteControls";
import OrbitPath from "./OrbitPath";

function App() {
  const [currentTLE, setCurrentTLE] = useState(null);

  return (
    <div style={{ position: "relative", width: "100%", height: "100vh" }}>
      <SatelliteControls onTrack={(data) => setCurrentTLE(data)} />

      <Viewer full timeline={false} animation={false}>
        {/* אם יש מידע, הצג גם את הלוויין וגם את המסלול שלו */}
        {currentTLE && (
          <>
            <OrbitPath tleData={currentTLE} />
            <SatelliteEntity tleData={currentTLE} />
          </>
        )}
      </Viewer>
    </div>
  );
}

export default App;
