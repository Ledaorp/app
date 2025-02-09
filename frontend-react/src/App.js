import React, { useState, useEffect } from "react";
import "./App.css";

function App() {








    // usestate for setting a javascript
    // object for storing and using data
    const [data, setdata] = useState({
        m1: "",
        m2: "",
        m3: "",
        m4: "",
        m5: "",
    });
    const [m1_slider_value,setValue] = useState(0)

    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("/api/get/angles").then((res) =>
            res.json().then((data) => {
                // Setting a data from api
                setdata({
                    m1: data.m1,
                    m2: data.m2,
                    m3: data.m3,
                    m4: data.m4,
                    m5: data.m5,
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

    const onChange = (event) => {
        const m1_slider_value = event.target.value;
        setValue(m1_slider_value);
        console.log("state: ", m1_slider_value);

      };



    return (
        <div className="App">
            <header className="App-header">
                <h1>React and flask</h1>
                

            </header>
            {/* Calling a data from setdata for showing */}
            <div className="App">
                    <div class="cnm">
                        <div>
                            <h4>M1</h4>
                        </div>
                        <div>
                            <p>Angle: {data.m1}</p>
                        </div>
                        <div>
                            
                            <input type="range" min="0" max="360"  value={m1_slider_value} onChange={(e) => onChange(e)}/>
                            <label >{m1_slider_value}</label>
                        </div>
                    </div>
                    <div class="cnm">
                        <div>
                            <p>M2</p>
                            <p>enable</p>
                        </div>
                        <div>
                            <p>{data.m2}</p>
                        </div>
                        <div>
                            <p>pcdz2</p>
                        </div>
                    </div>
                </div>
        </div>
    );
}

export default App;