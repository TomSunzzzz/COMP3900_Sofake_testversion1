# SoFake - Fake News Detection & Evolution System

This is the official repository for the COMP3900 project: **SoFake**.
Our system integrates LLM-based agent networks with sophisticated deviation evaluation (FUSE).

## Repo member Information
- **Tester**: Tom Sun (z5408739)
- **Focus**: Unit Testing & Integration Verification

## Project Structure
- `frontend/`: React-based user interface(Devin).
- `Agent_network/`: Core logic for agent interactions (Gardner).
- `database/`: Persistence layer for storing news data (Yuchen).
- `FUSE/`: Multi-dimensional evaluation system (Tom/William).

## Setup & Installation
1. **Clone the repo**: `git clone <your-repo-url>`
2. **Install Python dependencies**:
   `pip install -r requirements.txt`


3. Install Frontend dependencies:
    `cd Frontend\soFake && npm install`

Running Unit Tests
We have achieved 100% pass rate for Sprint 1 core modules:

1. Frontend Tests
`cd Frontend\soFake\src && npm test`

2. Agent Network Tests
`cd Agent_network && python -m pytest`

3. Database Tests
`cd DB\comp3900_project_SoFake\backend && python -m pytest`

4. FUSE Evaluation Tests
`cd Fuse_Eval\fake_news_project\FUSE && python -m pytest`