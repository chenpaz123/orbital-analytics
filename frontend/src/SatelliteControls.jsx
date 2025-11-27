import React, { useState } from "react";

const SatelliteControls = ({ onTrack }) => {
  // ניהול הטופס המקומי
  const [name, setName] = useState("ISS (ZARYA)");
  const [line1, setLine1] = useState(
    "1 25544U 98067A   24028.56385799  .00014603  00000+0  26359-3 0  9997"
  );
  const [line2, setLine2] = useState(
    "2 25544  51.6401 199.6483 0004951 281.4287 186.2238 15.49815049436856"
  );

  const handleSubmit = (e) => {
    e.preventDefault(); // מניעת ריענון הדף
    // שליחת הנתונים למעלה (לאבא)
    onTrack({ sat_name: name, tle_line1: line1, tle_line2: line2 });
  };

  return (
    <div
      style={{
        position: "absolute", // צף מעל הכל
        top: 10,
        left: 10,
        zIndex: 100, // שכבה עליונה
        backgroundColor: "rgba(0, 0, 0, 0.7)", // רקע חצי שקוף
        padding: "20px",
        color: "white",
        borderRadius: "8px",
        fontFamily: "monospace",
      }}
    >
      <h3>🛰️ Orbital Ops</h3>
      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "10px" }}
      >
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Satellite Name"
          style={{ padding: "5px" }}
        />
        <input
          value={line1}
          onChange={(e) => setLine1(e.target.value)}
          placeholder="TLE Line 1"
          style={{ padding: "5px", width: "300px" }}
        />
        <input
          value={line2}
          onChange={(e) => setLine2(e.target.value)}
          placeholder="TLE Line 2"
          style={{ padding: "5px", width: "300px" }}
        />
        <button
          type="submit"
          style={{
            padding: "10px",
            backgroundColor: "#00d2ff",
            border: "none",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          TRACK TARGET
        </button>
      </form>
    </div>
  );
};

export default SatelliteControls;
