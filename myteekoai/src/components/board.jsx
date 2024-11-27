import React, { useEffect } from 'react';
import '../App.css'; // Add styling

const Board = ({ board, onCellClick, dropPhase }) => {
    useEffect(() => {
        console.log('Board updated:', board);
    }, [board]);

    return (
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="row">
                    {row.map((cell, colIndex) => (
                        <div
                            key={colIndex}
                            className={`cell`}
                            onClick={() => onCellClick(rowIndex, colIndex)}
                        >
                            {cell === 'b' && <div className="piece blue"></div>}
                            {cell === 'r' && <div className="piece red"></div>}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default Board;
