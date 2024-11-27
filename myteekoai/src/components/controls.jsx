import React from 'react';

const Controls = ({ onAIMove, onReset }) => (
    <div>
        <button className="ai-move" onClick={onAIMove}>
            AI Move
        </button>
        <button className="reset" onClick={onReset}>
            Reset Game
        </button>
    </div>
);

export default Controls;
