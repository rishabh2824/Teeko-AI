Welcome to Teeko AI, a web-based implementation of the strategic game Teeko with an AI-powered opponent. This application allows users to play against a challenging AI that adapts to different difficulty levels. It is built with React for the frontend and FastAPI for the backend, and deployed using Netlify and Render.

## Features

**Play Teeko Online:** Interactive gameplay with intuitive controls.

**AI Opponent:** Play against an AI with varying levels of difficulty.
  
  Beginner: Depth 3
  
  Expert: Depth 4
  
**Responsive Design:** Optimized for desktop and mobile users.

**Game Rules:** Adheres to the official Teeko rules.

**Reset and Replay:** Restart the game at any time.
  
**User-Friendly UI:** Easy navigation and instructions for new players.
  
**Ad Integration:** Google AdSense for monetization.

## Tech Stack

**Frontend**

  React: JavaScript library for building the user interface.
    
  React Router: For navigation between the home page and the game page.
    
  CSS: Custom styles for an engaging UI/UX.
    
**Backend**
  
  FastAPI: High-performance Python web framework.
  
  Teeko AI Logic: Built using a minimax algorithm with depth-based evaluation. The AI generates all possible successor state and uses a heuristic function to evaluate the best state.
  
## Deployment

  **Frontend:** Hosted on Netlify.
  
  **Backend:** Hosted on Render.

  Try out the game here: https://teekoai.netlify.app/
