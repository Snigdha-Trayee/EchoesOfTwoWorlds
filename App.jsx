import { useState } from "react";
import "./App.css";

export default function App() {
  const [screen, setScreen] = useState("title");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [player, setPlayer] = useState("");
  const [clueIndex, setClueIndex] = useState(0);
  const [activeQuiz, setActiveQuiz] = useState("moon");
  const [quizQuestion, setQuizQuestion] = useState(0);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizFinished, setQuizFinished] = useState(false);

  const moonQuestions = [
    {
      question: "What does the Moon Rune's message say?",
      options: [
        "Light defeats all darkness.",
        "The moon remembers what the sun forgets.",
        "Stars guide the lost.",
        "The sun controls the moon.",
      ],
      correctAnswer: 1,
    },
    {
      question: "When can the Moon be visible in the sky?",
      options: [
        "Only at midnight.",
        "Only at sunrise.",
        "At different times, depending on its phase.",
        "Only at noon.",
      ],
      correctAnswer: 2,
    },
    {
      question: "What might the Moon Rune's mystery suggest?",
      options: [
        "Look beyond the darkness to discover hidden memories.",
        "The sun hides every secret.",
        "The stars have disappeared.",
        "The portal must remain closed.",
      ],
      correctAnswer: 0,
    },
  ];

  const sunQuestions = [
    {
      question: "What does the Sun Rune's message say?",
      options: [
        "The moon remembers everything.",
        "Light reveals what memory hides.",
        "Stars control the portal.",
        "Darkness lasts forever.",
      ],
      correctAnswer: 1,
    },
    {
      question: "What does sunlight help us do?",
      options: [
        "See things more clearly.",
        "Erase every memory.",
        "Stop time.",
        "Make the stars disappear.",
      ],
      correctAnswer: 0,
    },
    {
      question: "What might the Sun Rune teach the player?",
      options: [
        "Never explore the unknown.",
        "The portal should stay closed.",
        "Truth can be revealed by looking beyond appearances.",
        "The Moon Rune has no meaning.",
      ],
      correctAnswer: 2,
    },
  ];

  const starQuestions = [
    {
      question: "What does the Star Rune's message say?",
      options: [
        "The moon remembers the past.",
        "Light reveals hidden memories.",
        "The star reveals the path.",
        "The sun controls the stars.",
      ],
      correctAnswer: 2,
    },
    {
      question: "What do stars help travelers do at night?",
      options: [
        "Navigate and find directions.",
        "Stop the passage of time.",
        "Make the Moon disappear.",
        "Close every portal.",
      ],
      correctAnswer: 0,
    },
    {
      question: "What might the Star Rune represent?",
      options: [
        "Forgetting every clue.",
        "Finding guidance when the way is unclear.",
        "Avoiding every challenge.",
        "Returning to the beginning.",
      ],
      correctAnswer: 1,
    },
  ];

  const clues = [
    {
      name: "Moon Rune",
      image: "/clues1.png",
      description: "The moon remembers what the sun forgets.",
    },
    {
      name: "Sun Rune",
      image: "/clues2.png",
      description: "Light reveals what memory hides.",
    },
    {
      name: "Star Rune",
      image: "/clues3.png",
      description: "The star reveals the path.",
    },
  ];

  const currentQuestions =
    activeQuiz === "moon"
      ? moonQuestions
      : activeQuiz === "sun"
      ? sunQuestions
      : starQuestions;

  const quizTitle =
    activeQuiz === "moon"
      ? "🌙 Moon Rune Challenge"
      : activeQuiz === "sun"
      ? "☀️ Sun Rune Challenge"
      : "⭐ Star Rune Challenge";

  function beginGame() {
    setScreen("login");
    setError("");
  }

  function handleLogin(event) {
    event.preventDefault();

    if (username.trim().length < 3) {
      setError("Your adventurer name must have at least 3 characters.");
      return;
    }
    if (password.length < 4) {
      setError("Your password must have at least 4 characters.");
      return;
    }

    setPlayer(username.trim());
    setError("");
    setScreen("welcome");
  }

  function returnToTitle() {
    setScreen("title");
    setUsername("");
    setPassword("");
    setError("");
  }

  function openPortal() {
    setClueIndex(0);
    setScreen("portal");
  }

  function openCurrentQuiz() {
    const quizForClue = ["moon", "sun", "star"][clueIndex];
    setActiveQuiz(quizForClue);
    setQuizQuestion(0);
    setQuizAnswers({});
    setQuizFinished(false);
    setScreen("quiz");
  }

  function continueClue() {
    // The clue screen's Continue button opens the quiz for the visible rune.
    if (clueIndex >= 0 && clueIndex < clues.length) {
      openCurrentQuiz();
    }
  }

 

function finishCurrentQuiz() {
  if (clueIndex < clues.length - 1) {
    const nextClueIndex = clueIndex + 1;

    setClueIndex(nextClueIndex);
    setQuizQuestion(0);
    setQuizAnswers({});
    setQuizFinished(false);
    setActiveQuiz(
      nextClueIndex === 1
        ? "sun"
        : "star"
    );
    setScreen("clue");
  } else {
    setScreen("restored");
  }
}



  function startCluesFromPortal() {
    setClueIndex(0);
    setScreen("clue");
  }

  const score = currentQuestions.filter(
    (question, index) => quizAnswers[index] === question.correctAnswer
  ).length;

  return (
    <main className="game-screen">
      {screen === "title" && (
        <section className="title-screen">
          <div className="game-menu">
            <p className="menu-eyebrow">YOUR DESTINY AWAITS</p>
            <button className="magic-button" onClick={beginGame}>
              <span>BEGIN THE GAME</span>
            </button>
            <p className="menu-footer">Explore · Solve · Uncover</p>
          </div>
        </section>
      )}

      {screen === "login" && (
        <section className="login-screen">
          <button className="back-button" onClick={returnToTitle}>
            ← BACK
          </button>
          <form className="login-card" onSubmit={handleLogin}>
            <p className="form-eyebrow">THE ADVENTURE BEGINS</p>
            <h2>Enter Your Realm</h2>
            <p className="form-description">Identify yourself, adventurer.</p>
            <label htmlFor="username">Adventurer Name</label>
            <input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
              required
            />
            <label htmlFor="password">Secret Passphrase</label>
            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              required
            />
            {error && <p className="error-message">{error}</p>}
            <button className="magic-button submit-button" type="submit">
              <span>ENTER THE WORLD</span>
            </button>
          </form>
        </section>
      )}

      {screen === "welcome" && (
        <section className="welcome-screen">
          <p className="form-eyebrow">THE PORTAL IS OPEN</p>
          <h2>WELCOME, {player.toUpperCase()}</h2>
          <p>Your journey through the two worlds awaits.</p>
          <button className="magic-button" onClick={openPortal}>
            <span>CONTINUE →</span>
          </button>
          <button className="magic-button" onClick={returnToTitle}>
            <span>RETURN TO TITLE</span>
          </button>
        </section>
      )}

      {screen === "portal" && (
        <section className="portal-screen">
          <img
  src="/portal.png"
  alt="The Portal Is Open"
  className="portal-art"
/>
          <button
            className="portal-enter-button"
            aria-label="Enter Portal"
            title="Enter Portal"
            onClick={startCluesFromPortal}
          />
        </section>
      )}

      {screen === "clue" && (
        <section className="clue-screen">
          <img
  src={clues[clueIndex].image}
  alt={clues[clueIndex].name}
  className="clue-art"
/>
          <button
            type="button"
            className="clue-continue-button"
            aria-label={`Continue to ${clues[clueIndex].name} quiz`}
            title="Continue"
            onClick={continueClue}
          />
        </section>
      )}

      {screen === "quiz" && (
        <section className="quiz-screen">
          <div className="quiz-card">
            <p className="quiz-eyebrow">ECHOES OF TWO WORLDS</p>
            <h1>{quizTitle}</h1>

            {!quizFinished ? (
              <>
                <p className="quiz-progress">
                  Question {quizQuestion + 1} of {currentQuestions.length}
                </p>
                <h2>{currentQuestions[quizQuestion].question}</h2>
                <div className="quiz-options">
                  {currentQuestions[quizQuestion].options.map((option, index) => (
                    <button
                      type="button"
                      key={option}
                      className={`quiz-option ${
                        quizAnswers[quizQuestion] === index ? "selected" : ""
                      }`}
                      onClick={() =>
                        setQuizAnswers((previous) => ({
                          ...previous,
                          [quizQuestion]: index,
                        }))
                      }
                    >
                      {String.fromCharCode(65 + index)}. {option}
                    </button>
                  ))}
                </div>
                <button
                  type="button"
                  className="magic-button quiz-next"
                  disabled={quizAnswers[quizQuestion] === undefined}
                  onClick={() => {
                    if (quizQuestion < currentQuestions.length - 1) {
                      setQuizQuestion((previous) => previous + 1);
                    } else {
                      setQuizFinished(true);
                    }
                  }}
                >
                  {quizQuestion === currentQuestions.length - 1
                    ? "FINISH QUIZ"
                    : "NEXT QUESTION"}
                </button>
              </>
            ) : (
              <>
                <h2>{activeQuiz === "moon" ? "Moon" : activeQuiz === "sun" ? "Sun" : "Star"} Rune Complete!</h2>
                <p>
                  Your score: {score} / {currentQuestions.length}
                </p>
                <button type="button" className="magic-button" onClick={finishCurrentQuiz}>
                  {clueIndex < clues.length - 1
                    ? `CONTINUE TO ${clues[clueIndex + 1].name.toUpperCase()}`
                    : "RESTORE THE MEMORY SEAL"}
                </button>
              </>
            )}
          </div>
        </section>
      )}

{screen === "restored" && (
  <section className="portal-screen">
    <img
      src="/portal.png"
      alt="Memory Seal Restored — The Portal Is Open"
      className="portal-art"
    />
    <button
      type="button"
      className="portal-enter-button"
      aria-label="Enter Portal"
      title="Enter Portal"
      onClick={() => {
        // Stay on the final portal screen.
        // Backend integration can be added here later.
      }}
    />
  </section>
)}
      
    </main>
  );
}
