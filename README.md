The Globetrotter Challenge – The Ultimate Travel Guessing Game!

Project Overview

Globetrotter is a full-stack web application where users receive cryptic clues about famous destinations and must guess which place it refers to. Upon answering, users unlock fun facts, trivia, and interactive animations based on their responses.

Core Features

1. Dataset & AI Integration

A starter dataset is provided.

AI tools (e.g., ChatGPT, OpenAI API, Web Scraping) are used to expand the dataset to 100+ destinations.

Each destination includes:

Clues

Fun facts

Trivia

2. Functional Web App

Displays 1–2 random clues for a destination.

Allows users to select from multiple-choice answers.

Provides immediate feedback:

Correct Answer: Confetti animation + fun fact reveal.

Incorrect Answer: Sad-face animation + fun fact reveal.

Includes ‘Play Again’ or ‘Next’ button for a new question.

Tracks and displays the total user score.

Ensures data security by storing and retrieving questions from the backend.

3. "Challenge a Friend" Feature

Users enter a unique username to register.

Clicking ‘Challenge a Friend’:

Generates a shareable invite link for WhatsApp.

Optionally includes a dynamic image with game details.

Invited friends can view the invitee’s score before playing.

Anyone with the invitation link can play the game.

Tech Stack

Frontend: HTML, CSS, JavaScript, AJAX

Backend: Python Flask, MySQL

AI/Automation: OpenAI API, Web Scraping

Database: MySQL for storing destinations, users, and scores

Project Structure

/Globetrotter  
│── /static  # Frontend assets (CSS, JS)  
│── /templates  # HTML templates  
│── /data  # JSON dataset  
│── app.py  # Flask backend  
│── database.sql  # MySQL schema  
│── README.md  # Project documentation  

Installation & Setup

Clone the repository:

git clone https://github.com/your-repo/globetrotter.git
cd globetrotter

Install dependencies:

pip install -r requirements.txt

Set up the MySQL database:

mysql -u root -p < database.sql

Run the Flask server:

python app.py

Open the app in the browser:

http://127.0.0.1:5000/

Future Improvements

Leaderboard for top-scoring players

User authentication for progress tracking

More interactive animations

Localization for different languages