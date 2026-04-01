# SoFake - Fake News Detection & Evolution System

This is the official repository for the COMP3900 project: **SoFake**.
Our system integrates LLM-based agent networks with sophisticated deviation evaluation (FUSE).

## Team Information
- **Lead Tester**: Tom Sun (z5408739)
- **Sprint 1 Focus**: Unit Testing & Integration Verification

## Project Structure
- `frontend/`: React-based user interface.
- `Agent_network/`: Core logic for agent interactions (Gardner).
- `database/`: Persistence layer for storing news data (Yuchen).
- `FUSE/`: Multi-dimensional evaluation system (Tom/William).

## Setup & Installation
1. **Clone the repo**: `git clone <your-repo-url>`
2. **Install Python dependencies**:
   pip install -r requirements.txt


3. Install Frontend dependencies:
    cd frontend && npm install

Running Unit Tests
We have achieved 100% pass rate for Sprint 1 core modules:

1. Frontend Tests
cd frontend && npm test

2. Agent Network Tests
python -m pytest Agent_network/

3. Database Tests
python -m pytest database/

4. FUSE Evaluation Tests
python -m pytest FUSE/