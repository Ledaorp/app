import React from 'react';
const PositionControl = ({ angleValues, handlePositionChange, updatePositionData }) => {
    return (
        <div className="cnm">
            <h4>Ovládání ramena</h4>
            <div class="xyzinput">
                <p>X:</p>
                <input
                    type="number"
                    name={'x_value'}
                    value={angleValues.x_value}
                    onChange={(e) => handlePositionChange('x_value', e.target.value)}
                />
            </div>
            <div class="xyzinput">
                <button onClick={() => { updatePositionData({ "x": angleValues.x_value })}}>Set position</button>
            </div>
            <div class="xyzinput">
                <p>Y:</p>
                <input
                    type="number"
                    name={'y_value'}
                    value={angleValues.y_value}
                    onChange={(e) => handlePositionChange('y_value', e.target.value)}
                />
            </div>
            <div class="xyzinput">
                <button onClick={() => { updatePositionData({ "y": angleValues.y_value })}}>Set position</button>
            </div>
            <div class="xyzinput">
                <p>Z:</p>
                <input
                    type="number"
                    name={'z_value'}
                    value={angleValues.z_value}
                    onChange={(e) => handlePositionChange('z_value', e.target.value)}
                />
            </div>
            <div class="xyzinput">
                <button onClick={() => { updatePositionData({ "z": angleValues.z_value })}}>Set position</button>
            </div>
        </div>
    );
};

export default PositionControl;