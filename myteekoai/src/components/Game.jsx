import React, { useEffect, useState } from 'react';
import Board from './board';
import Controls from './controls';
import { getGameState, aiMove, opponentMove, resetGame } from '../api';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import '../App.css';

const Game = () => {
    const [board, setBoard] = useState([]);
    const [turn, setTurn] = useState('');
    const [gameStatus, setGameStatus] = useState('');
    const [selectedCell, setSelectedCell] = useState(null);
    const [opponentPiece, setOpponentPiece] = useState('');
    const [winner, setWinner] = React.useState(null); // Null if no winner yet
    const navigate = useNavigate(); // Initialize navigate hook

    const fetchGameState = async () => {
        try {
            const data = await getGameState();
            console.log('Fetched game state:', data);
            setBoard(data.board);
            setTurn(data.turn);
            setGameStatus(data.game_status);
            setOpponentPiece(data.opponent_piece);
            setWinner(data.winner);
            setSelectedCell(null);
        } catch (error) {
            alert('Failed to fetch game state.');
        }
    };

    useEffect(() => {
        fetchGameState();
    }, []);

    const handleCellClick = async (row, col) => {
        if (gameStatus === 'over') {
            alert('Game is over.');
            return;
        }

        if (turn !== 'Opponent') {
            alert("It's AI's turn!");
            return;
        }

        // Calculate if it's the drop phase
        const totalPieces = board.flat().filter(cell => cell !== ' ' && cell !== '').length;
        const dropPhase = totalPieces < 8;

        if (dropPhase) {
            // Handle drop phase: Single cell selection
            const move = [[row, col]];

            try {
                const data = await opponentMove(move);
                setBoard(data.board);
                setGameStatus(data.game_status);
                setTurn(data.turn);
                setWinner(data.winner);
            } catch (error) {
                alert(error.response?.data?.detail || 'Invalid move.');
            }
        } else {
            // Handle move phase: Two cell selection
            if (!selectedCell) {
                // Validate that the selected cell contains the opponent's piece
                if (board[row][col] !== opponentPiece) {
                    alert('You must select one of your pieces to move.');
                    return;
                }
                setSelectedCell([row, col]);
                console.log('Selected Source Cell:', [row, col]);
            } else {
                const move = [[row, col], selectedCell];

                try {
                    const data = await opponentMove(move);
                    setBoard(data.board);
                    setGameStatus(data.game_status);
                    setTurn(data.turn);
                    setWinner(data.winner);
                } catch (error) {
                    alert(error.response?.data?.detail || 'Invalid move.');
                } finally {
                    setSelectedCell(null); // Clear the selected cell
                }
            }
        }
    };

    const handleAIMove = async () => {
        if (gameStatus === 'over') {
            alert('Game is over.');
            return;
        }

        if (turn !== 'AI') {
            alert("It's not AI's turn!");
            return;
        }

        try {
            const data = await aiMove();
            setBoard(data.board);
            setGameStatus(data.game_status);
            setTurn(data.turn);
            setWinner(data.winner);
        } catch (error) {
            alert('Failed to process AI move.');
        }
    };

    const handleReset = async () => {
        try {
            await resetGame();
            navigate('/'); // Redirect to the home page
        } catch (error) {
            alert('Failed to reset game.');
        }
    };

    return (
        <div className="App">
            <h1 className="App-title">Teeko Game</h1>
            <h2>Turn: {turn}</h2>
            {gameStatus === 'over' && (
                <h2 className="App-status">
                    {winner === 'AI'
                        ? 'AI Wins!'
                        : winner === 'Opponent'
                            ? 'You Win!'
                            : 'It\'s a Draw!'}
                </h2>
            )}
            <Board
                board={board}
                onCellClick={handleCellClick}
                dropPhase={board.flat().filter(cell => cell !== '').length < 8}
            />
            <Controls onAIMove={handleAIMove} onReset={handleReset} />
        </div>
    );
};

export default Game;
