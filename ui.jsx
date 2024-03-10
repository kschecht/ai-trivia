import React, { useState } from 'react';
import './App.css';

function App() {
  const [players, setPlayers] = useState([]);
  const [numGrades, setNumGrades] = useState(6);
  const [grades, setGrades] = useState([]);
  const [gameStarted, setGameStarted] = useState(false);

  const handlePlayersSubmit = (event) => {
    event.preventDefault();
    const playersArray = event.target.players.value.split(' ');
    setPlayers(playersArray);
    setGameStarted(true);
  };

  const handleNumGradesChange = (event) => {
    setNumGrades(event.target.value);
  };

  const handleGradesSubmit = (event) => {
    event.preventDefault();
    const gradesArray = event.target.grades.value.split(' ').map(grade => parseInt(grade));
    setGrades(gradesArray);
  };

  return (
    <div className="App">
      {!gameStarted ? (
        <div>
          <h1>Welcome to TrivAI Pursuit!</h1>
          <form onSubmit={handlePlayersSubmit}>
            <label>
              Enter all player names separated by spaces (ex: Alice Bob Carl):
              <input type="text" name="players" />
            </label>
            <button type="submit">Start Game</button>
          </form>
        </div>
      ) : (
        <div>
          <h2>Number of Grades: {numGrades}</h2>
          <form onSubmit={handleGradesSubmit}>
            <label>
              Enter the number of grades you'd like to complete:
              <input type="number" name="grades" value={numGrades} onChange={handleNumGradesChange} />
            </label>
            <button type="submit">Set Grades</button>
          </form>
          <h2>Grades</h2>
          {grades.length > 0 ? (
            <ul>
              {grades.map((grade, index) => (
                <li key={index}>Grade {index + 1}: {grade}</li>
              ))}
            </ul>
          ) : (
            <p>No grades set yet.</p>
          )}
          <h2>Players</h2>
          <ul>
            {players.map((player, index) => (
              <li key={index}>{player}</li>
            ))}
          </ul>
          {/* You can continue implementing the game logic and UI here */}
        </div>
      )}
    </div>
  );
}

export default App;
