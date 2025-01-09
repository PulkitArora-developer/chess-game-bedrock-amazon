# AI-Powered Chess Game (AWS)

This project is a modern chess platform where players can compete against an AI-powered opponent. The AI, powered by **Antrophic Claude 3.5 Sonnet** (Available on Amazon Bedrock), generates real-time moves using **FEN (Forsyth-Edwards Notation)** to understand the current game state. Built with a scalable and serverless architecture on AWS, the game delivers a smooth and responsive user experience while providing an intelligent (but imperfect) opponent.

## Inspiration

Chess has been a source of intellectual challenge for centuries. With the rise of AI and cloud technologies, we saw an opportunity to enhance the chess-playing experience using modern tools like **Claude 3.5** and **Amazon Q Developer**. Our goal was to create a fast, accessible, and intelligent chess platform, combining the beauty of the game with cutting-edge AI and cloud infrastructure.

## Features

- **AI-Powered Gameplay**: Play against an AI opponent powered by Claude 3.5 Sonnet, which makes intelligent (though sometimes imperfect) decisions.
- **FEN Support**: The AI understands and uses FEN (Forsyth-Edwards Notation) to interpret the current chessboard state, including piece positions, castling rights, en passant opportunities, and move history.
- **Seamless Backend**: The backend is built using **AWS Lambda** and **API Gateway** in a serverless architecture, ensuring scalability and low-latency interactions.
- **Responsive UI**: The frontend is built with **Angular** for an intuitive, responsive user interface that works across devices.
- **AI Customization**: Custom prompts and tuning have been applied to Claude 3.5 to optimize move generation and improve gameplay.

## Architecture

- **Frontend**: Developed using **Angular**, providing a user-friendly interface to interact with the chessboard, view moves, and play against the AI.
- **Backend**: The backend is serverless, powered by **AWS Lambda** and **API Gateway**, ensuring scalability and minimal server management.
- **AI Integration**: **Claude 3.5 Sonnet** (available through **Amazon Bedrock**) powers the AI decision-making, processing game states in real-time using FEN.
- **Hosting**: The frontend is deployed on **AWS S3** and served globally via **CloudFront** for secure, reliable hosting.

## Challenges

- **Prompt Tuning**: Customizing Claude 3.5 to generate accurate and timely chess moves was challenging, especially in handling complex chess positions and edge cases like castling, en passant, and pawn promotion.
- **AI Decision-Making**: While Claude 3.5 is quite intelligent, there are occasional mistakes or suboptimal moves, especially in non-standard game situations.
- **Real-Time Performance**: Achieving low-latency performance while balancing AI response times and serverless backend workflows was a key challenge.

## Technologies Used

- **AWS Lambda** – Serverless compute for handling backend logic and AI interactions.
- **API Gateway** – Scalable API management for handling requests between the frontend and backend.
- **Claude 3.5 Sonnet** – AI-powered chess logic provided through Amazon Bedrock.
- **Angular** – Frontend framework for building a responsive, interactive user interface.
- **FEN (Forsyth-Edwards Notation)** – Standard chessboard representation used by the AI to interpret the current state of the game.
- **Amazon Q Developer** – Used for code completion, development, and ensuring robust, secure backend code.

## Acknowledgments

We would like to thank **Amazon Q Developer** for helping us with code completion, development, and vulnerability fixes. Its support allowed us to focus on creating a seamless user experience while ensuring the backend code was secure and reliable.

A special thanks to **Amazon Bedrock** for providing the platform to integrate **Claude 3.5 Sonnet** into our system, powering intelligent chess decisions. The integration of these AI models was essential in building an engaging, dynamic chess experience.

## What’s Next?

- **Improved AI Logic**: We plan to enhance the AI’s decision-making process to reduce errors and improve performance in complex game situations.
- **Multiplayer Mode**: We are exploring adding multiplayer functionality to allow users to challenge friends or other online players.
- **Mobile App**: A mobile version is in development to make the game accessible on smartphones and tablets.
- **Analytics**: We aim to integrate features that provide players with performance insights, including move accuracy, win rates, and more.

## How to Run the Project Locally

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/PulkitArora-developer/chess-game-bedrock-amazon.git
   cd chess-game-bedrock-amazon
   ```

2. Install dependencies for the frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Run the frontend app:
   ```bash
   ng serve
   ```

4. Make sure the backend (AWS Lambda & API Gateway) is properly set up in AWS, and configure the necessary environment variables for the AI model and FEN processing.

5. Open the app in your browser at `http://localhost:4200`.

