import React, { useState, useEffect } from "react";
import "./App.css";
import MotorControl from "./components/MotorComponent";
import PositionControl from "./components/PositionComponent";

function App() {
    const [data, setData] = useState({
        m1: 0,
        m2: 0,
        m3: 0,
        m4: 0,
        m5: 0
    });

    const [angleValues, setAngleValues] = useState({ m1_value: 0, m2_value: 0, m3_value: 0, m4_value: 0, m5_value: 0, x_value: 0, y_value: 0, z_value: 0 });
    
    const identifiers = ['m1', 'm2', 'm3', 'm4', 'm5'];

    useEffect(() => {
      fetchData('http://192.168.1.101:5000/motors/setAngles');
      const ini = setInterval(() => {fetchData('http://192.168.1.101:5000/motors/setAngles');}, 5000); 
      return () => clearInterval(ini);
    },[]);

    const fetchData = async (url) => {
      try {
          const response = await fetch(url);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setData(data);
      } catch (error) {
          console.error("Could not fetch data:", error);
      }
  };
  const updateData = async (type,id,value) => {
    try {
      const newData = {     [type]: {
                                [id]:value
                            }
                        };

      const response = await fetch('http://192.168.1.101:5000/api/set/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log("Data updated successfully!");
    } catch (error) {
      console.error("Could not update data:", error);
    }
  };

    const handleAngleChange = (name, value) => {
        setAngleValues({ ...angleValues, [name]: value });
    };

    const updateMotorData = async (motorData) => {
        const id = Object.keys(motorData)[0];
        const value = motorData[id];
        updateData("angles",id,value);
        //await fetchData('http://192.168.1.101:5000/motors/setAngles');
    };
    const updatePositionData = async (positionData) => {
      const id = Object.keys(positionData)[0];
      const value = positionData[id];
      updateData("positions",id,value);
      await fetchData('http://192.168.1.101:5000/motors/position');
  };

    return (
        <div className="App">
            <div className="App-scrollable">
                {identifiers.map((id) => (
                    <MotorControl
                        key={id}
                        id={id}
                        data={data}
                        angleValue={angleValues[`${id}_value`]}
                        handleAngleChange={handleAngleChange}
                        updateMotorData={updateMotorData}
                    />
                ))}
            </div>
            <PositionControl
                angleValues={angleValues}
                handlePositionChange={handleAngleChange}
                updatePositionData={updatePositionData}
            />
        </div>
    );
}

export default App;