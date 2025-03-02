document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("username");
    const startGameButton = document.getElementById("startGame");
    const nextButton = document.getElementById("next");
    const challengeButton = document.getElementById("challenge");
    const clueElement = document.getElementById("clue");
    const choicesContainer = document.getElementById("choices");
    const feedbackElement = document.getElementById("feedback");
    const scoreElement = document.getElementById("userScore");
    let username = "";

    // Start Game
    startGameButton.addEventListener("click", function () {
        username = usernameInput.value.trim();
        if (!username) {
            alert("Please enter your name.");
            return;
        }
        fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username })
        }).then(() => {
            document.getElementById("game").style.display = "block";
            usernameInput.style.display = "none";
            startGameButton.style.display = "none";
            updateScore();
            loadQuestion();
        });
    });

    // Update Score
    function updateScore() {
        fetch(`/score/${username}`)
            .then(response => response.json())
            .then(data => {
                scoreElement.textContent = `Score: ${data.score || 0}`;
            });
    }

    // Load Question
    function loadQuestion() {
        fetch("/question")
            .then(response => response.json())
            .then(data => {
                clueElement.textContent = "Clues: " + data.clues.join(" | ");
                choicesContainer.innerHTML = "";
                
                // Store correct answer globally
                const correctAnswer = data.correct_answer;

                data.choices.forEach(choice => {
                    const button = document.createElement("button");
                    button.textContent = choice;
                    button.classList.add("choice-btn");
                    button.onclick = () => checkAnswer(choice, correctAnswer, data.fun_fact);
                    choicesContainer.appendChild(button);
                });

                // Clear previous feedback
                feedbackElement.innerHTML = "";
            });
    }

    // Check Answer
    function checkAnswer(userAnswer, correctAnswer, funFact) {
        if (userAnswer === correctAnswer) {
            feedbackElement.innerHTML = `🎉 Correct! ${funFact}`;
            confettiEffect();
    
            // Post correct answer and then update the score
            fetch("/answer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: username, answer: userAnswer })
            })
            .then(response => response.json())
            .then(data => {
                if (data.correct) {
                    setTimeout(updateScore, 500); // Delay to allow backend to update
                }
            });
    
        } else {
            feedbackElement.innerHTML = `😢 Wrong! ${funFact}`;
        }
    }
    
    // Challenge a Friend
    challengeButton.addEventListener("click", function () {
        fetch(`/challenge/${username}`)
            .then(response => response.json())
            .then(data => {
                if (data.link) {
                    const message = `Join me in the Globetrotter Game! My score: ${scoreElement.textContent}.\nPlay now: ${data.link}`;
                    window.open(`https://wa.me/?text=${encodeURIComponent(message)}`);
                } else {
                    alert("Error generating challenge link.");
                }
            });
    });
    

    // Load Next Question
    nextButton.addEventListener("click", loadQuestion);

    // Confetti Animation for Correct Answers
    function confettiEffect() {
        const confetti = document.createElement("div");
        confetti.classList.add("confetti");
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 2000);
    }
});

function generateImageAndShare() {
    html2canvas(document.getElementById("game")).then(canvas => {
        let image = canvas.toDataURL("image/png");
        let link = document.createElement("a");
        link.href = image;
        link.download = "globetrotter_challenge.png";
        link.click();
    });
}
