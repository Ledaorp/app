import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
    // usestate for setting a javascript
    // object for storing and using data
    const [data, setdata] = useState({
        m1: 0,
        m2: 0,
        m3: 0,
        m4: 0,
        m5: 0,
    });
    const [e_data, e_setdata] = useState({
        m1: 0,
        m2: 0,
        m3: 0,
        m4: 0,
        m5: 0,
    });
    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("/api/get/data").then((res) =>
            res.json().then((data) => {
                // Setting a data from api
                setdata({
                    m1: data.angles.m1,
                    m2: data.angles.m2,
                    m3: data.angles.m3,
                    m4: data.angles.m4,
                    m5: data.angles.m5,
                });
            })
        );
    }, []);

    /*useEffect(() => {
        const evsData = new EvenrSource('/api/get/angles');
        function handleEvent(data){
            setdata(data)
        }
        evsData.onmessage = e=>{handleEvent(e.data)}

    });*/
    
    const fetchEncoderData = async () => {
        try {
          const response = await fetch('http://192.168.1.101:5000/motor');
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const e_data = await response.json();
          e_setdata({
            m1: data.angles.m1,
            m2: data.angles.m2,
            m3: data.angles.m3,
            m4: data.angles.m4,
            m5: data.angles.m5,
        });
        } catch (error) {
          console.error("Could not fetch data:", error);
          // Handle the error (e.g., display an error message to the user)
        }
      };

    const fetchData = async () => {
        try {
          const response = await fetch('http://localhost:5000/api/get/data');
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setdata({
            m1: data.angles.m1,
            m2: data.angles.m2,
            m3: data.angles.m3,
            m4: data.angles.m4,
            m5: data.angles.m5,
        });
        } catch (error) {
          console.error("Could not fetch data:", error);
          // Handle the error (e.g., display an error message to the user)
        }
      };

    const updateData = async () => {
        try {
          // Example:  Modify the data (you would get this from user input)
          const newData = {     "angles": {
                                    "m1":angle_values.m1_value,
                                    "m2":angle_values.m2_value,
                                    "m3":angle_values.m3_value,
                                    "m4":angle_values.m4_value,
                                    "m5":angle_values.m5_value
                                },
                                "position":{
                                    "x": "0",
                                    "y": "0",
                                    "z": "0"
                                }};
    
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
          fetchData();
          fetchData();
        } catch (error) {
          console.error("Could not update data:", error);
        }
      };



    //values of sliders
    const initial_angle_values={m1_value:data.m1,m2_value:data.m2,m3_value:data.m3,m4_value:data.m4,m5_value:data.m5};

    const [angle_values,setValue] = useState(initial_angle_values);
    const onChange = (event) => {
        setValue({ ...angle_values,[event.target.name]: event.target.value});
      };

    const initial_select_values={m1_select_value:"scrollbar",m2_select_value:"scrollbar",m3_select_value:"scrollbar",m4_select_value:"scrollbar",m5_select_value:"scrollbar"}
    const [select_values,setSelected] = useState(initial_select_values);
    const onSelect = (event) =>{
      setSelected({...select_values,[event.target.name]: event.target.value});
    };
    //values of sliders
    //ids for all the motors (after dynamicly rendered)
    const identifiers = ['m1', 'm2', 'm3', 'm4', 'm5'];

    return (
        <div className="App">
            {/*<header className="App-header">
            </header>*/}
            <div>
            <div>
            {identifiers.map(id => (
                <div className="cnm" key={id}>
                    <div>
                        <h4>{id.toUpperCase()}</h4>
                    </div>
                    <div>
                        <p>Angle: {data[id]}</p>
                    </div>
                    <div>
                        <p>Angle: {e_data[id]}</p>
                    </div>
                    <div>
                        <select name={`${id}_select_value`} value={select_values[`${id}_select_value`]} onChange={onSelect}>
                            <option value="scrollbar">Scrollbar</option>
                            <option value="textfield">TextField</option>
                        </select>
                    </div>
                    <div>
                        {select_values[`${id}_select_value`] === "scrollbar" && (
                            <div>
                                <input
                                    type="range"
                                    min="0"
                                    max="360"
                                    name={`${id}_value`}
                                    value={angle_values[`${id}_value`]}
                                    onChange={onChange}
                                />
                                <label>{angle_values[`${id}_value`]}</label>
                            </div>
                        )}
                        {select_values[`${id}_select_value`] === "textfield" && (
                            <input
                                type="number"
                                min="0"
                                max="360"
                                name={`${id}_value`}
                                value={angle_values[`${id}_value`]}
                                onChange={onChange}
                            />
                        )}
                    </div>
                    <div>
                        <button onClick={updateData}>Set angle</button>
                    </div>
                </div>
            ))}
        </div>



              </div>
            <div>
            <div class="cnm">
                        <div>
                            <h4>Ovládání ramena</h4>
                        </div>
                        <div>
                            <p>X: {"nedostupné"}</p>
                        </div>
                        <div>
                            <p>Y: {"nedostupné"}</p>
                        </div>
                        <div>
                            <p>Z: {"nedostupné"}</p>
                        </div>
                        <div>

                        </div>
                    </div>
                    
            </div>
        </div>
    );
}

export default App;