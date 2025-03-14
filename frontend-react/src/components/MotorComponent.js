import React from 'react';
const MotorControl = ({ id, angleValue, handleAngleChange, updateMotorData }) => {
    const [selectValue, setSelectValue] = React.useState("scrollbar");

    const onChange = (event) => {
        handleAngleChange(`${id}_value`, event.target.value);
    };

    const onSelect = (event) => {
        setSelectValue(event.target.value);
    };

    return (
        <div className="cnm">
            <div>
                <h4>{id.toUpperCase()}</h4>
            </div>
            <div>
                <p>Angle: {angleValue}</p>
            </div>
            <div>
                <select name={`${id}_select_value`} value={selectValue} onChange={onSelect}>
                    <option value="scrollbar">Scrollbar</option>
                    <option value="textfield">TextField</option>
                </select>
            </div>
            <div>
                {selectValue === "scrollbar" && (
                    <div>
                        <input
                            className="slider"
                            type="range"
                            min="0"
                            max="360"
                            value={angleValue}
                            onChange={onChange}
                        />
                        <label>{angleValue}</label>
                    </div>
                )}
                {selectValue === "textfield" && (
                    <input
                        type="number"
                        min="0"
                        max="360"
                        value={angleValue}
                        onChange={onChange}
                    />
                )}
            </div>
            <div>
                <button onClick={() => updateMotorData({ [id]: angleValue })}>Set angle</button>
            </div>
        </div>
    );
};

export default MotorControl;