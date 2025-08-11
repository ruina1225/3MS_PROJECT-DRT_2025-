AI Optimized Route DRT Project

Project Overview
This project was developed as part of the SKKU SAY 1st Cohort Education Program and linked with the KDT Hackathon.
It focuses on an AI-driven Demand Responsive Transport (DRT) system under the theme:
"Connecting sea, land, and hospitals via AI-optimized DRT: Voice-based and face recognition enabled mobility for seniors."

This repository contains the backend API and the admin web page implementation.

#Key Features
User login and authentication via face recognition

Voice-command enabled DRT reservation and AI-powered optimal route recommendation

Admin web interface for managing users, hospital data, and visit logs

Robust data management through Oracle DB integration

Scalable RESTful API architecture

#Tech Stack
Component	Technologies & Tools
Backend	Python, FastAPI
Database	Oracle DB
Frontend	React (React Admin)
Deployment	Docker
Authentication	Face Recognition (e.g., DeepFace)
Others	Voice recognition, REST API

Installation & Running
1. Clone the repository
#bash
git clone https://github.com/ruina1225/3MS_PROJECT-DRT_2025-.git
cd 3MS_PROJECT-DRT_2025-
2. Setup and run backend
Install required Python packages:
#bash
pip install -r requirements.txt
Create a .env file and configure Oracle DB connection details

#Run the FastAPI server:
#bash
uvicorn app.main:app --reload --port 3434

3. Run Admin Web Page
#bash
cd frontend/react_admin
yarn install
yarn start

#Project Structure
app/ - FastAPI backend source code
frontend/react_admin/ - Admin web page source code
scripts/ - Data processing and batch scripts
uploads/ - User face images and uploaded files storage

#Contributing
Fork this repository
Create a feature branch (feature/your-feature)
Commit your changes (git commit -m "Add feature")
Push to your branch and open a Pull Request

License
This project is licensed under the MIT License. See the LICENSE file for details.
