import React from 'react';
import { useNavigate } from 'react-router-dom';
import { setDifficulty } from '../api';
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate();

    const handleDifficultyClick = async (difficulty) => {
        try {
            await setDifficulty(difficulty);
            navigate('/game');
        } catch (error) {
            alert('Failed to set difficulty.');
        }
    };

    return (
        <div className="home-page">
            <h1 className="home-title">Welcome to Rishabh's Teeko AI</h1>
            <img
                src={require('./teekoboard.jpg')}
                alt="Teeko Board"
                className="teeko-image"
            />
            <h2 className="home-subtitle">Select the difficulty level:</h2>
            <div className="button-container">
                <button
                    className="difficulty-button"
                    onClick={() => handleDifficultyClick('beginner')}
                >
                    Beginner
                </button>
                <button
                    className="difficulty-button"
                    onClick={() => handleDifficultyClick('intermediate')}
                >
                    Intermediate
                </button>
                <button
                    className="difficulty-button"
                    onClick={() => handleDifficultyClick('expert')}
                >
                    Expert
                </button>
            </div>
            <p className="refresher-text">
                Need a refresher on how to play Teeko? <br />
                <a
                    href="https://en.wikipedia.org/wiki/Teeko"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="refresher-link"
                >
                    Learn here
                </a>
            </p>
        </div>
    );
};

export default HomePage;
