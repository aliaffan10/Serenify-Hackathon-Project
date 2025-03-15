# Serenify

Serenify is a modern mental health support web application that includes an AI-powered chatbot, sentiment analysis, suicidal risk assessment, journaling, and a resource hub to help users manage their mental well-being.

## 📌 Table of Contents
- [📖 Overview](#-overview)
- [⚙️ Prerequisites](#️-prerequisites)
- [⬇️ Downloading the Project](#️-downloading-the-project)
- [📦 Installation & Setup](#-installation--setup)
    - [🚀 Node.js Server Setup](#-nodejs-server-setup)
    - [🐍 Python Flask App Setup](#-python-flask-app-setup)
- [▶️ Running the Project](#-running-the-project)
- [🌐 Accessing the Application](#-accessing-the-application)
- [🛠️ Troubleshooting](#-troubleshooting)
- [📜 License](#-license)

---

## 📖 Overview

Serenify operates using a **two-server architecture**:

1. **Node.js Server (`server.js`)** - Handles AI chatbot functionality using the Google Generative AI API.
    - Forwards user input to the AI and returns responses.

2. **Python Flask App (`app.py`)** - Manages sentiment analysis, emotion detection, and suicidal risk assessment.
    - Utilizes machine learning models for accurate insights.

The front-end (`index.html`) interacts with these backend servers through API calls.

---

## ⚙️ Prerequisites

Before proceeding, ensure your system has the following installed:

✅ **[Node.js](https://nodejs.org/) (v14 or later) with npm** ✅ **[Python](https://www.python.org/downloads/) (v3.8 or later) with pip** ✅ **Git (optional, if cloning from a repository)** ---

## ⬇️ Downloading the Project

### 🔹 Option 1: Clone from GitHub

1. Open a terminal or command prompt.
2. Run the following command to clone the repository:

    ```bash
    git clone <repository-url>
    cd Serenify
    ```
    Replace `<repository-url>` with the actual GitHub repository URL.

### 🔹 Option 2: Download as ZIP

1. Visit the GitHub repository.
2. Click the **Code** button and select **Download ZIP**.
3. Extract the ZIP file and navigate into the extracted folder.

## 📦 Installation & Setup

### 🚀 Node.js Server Setup

1. Open a terminal and navigate to the project folder:

    ```bash
    cd Serenify
    ```

2. Install the required Node.js dependencies:

    ```bash
    npm install express cors axios @google/generative-ai
    ```

3. Update the API Key:

    - Open `server.js`.
    - Locate the API key line:

        ```javascript
        const genAI = new GoogleGenerativeAI("YOUR_ACTUAL_API_KEY");
        ```

    - Replace `"YOUR_ACTUAL_API_KEY"` with your Google Generative AI API Key.

### 🐍 Python Flask App Setup

1. Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install required Python packages:

    ```bash
    pip install Flask pandas numpy seaborn matplotlib scikit-learn xgboost
    ```

3. Ensure the following CSV files are present in the project directory:

    - `text_emotion.csv` (for emotion detection)
    - `Suicide_Detection.csv` (for suicidal risk assessment)
    - `master.csv` (for heatmap visualization)

## ▶️ Running the Project

### 🟢 Start the Python Flask App

1. Ensure your virtual environment is activated.
2. Run the following command:

    ```bash
    python app.py
    ```

    The Flask server will start on port 5000.

### 🔵 Start the Node.js Server

1. Open a new terminal and navigate to the project folder:

    ```bash
    cd Serenify
    ```

2. Run the Node.js server:

    ```bash
    node server.js
    ```

    The Node.js server will start on port 4000.

## 🌐 Accessing the Application

Once both servers are running:

- **If using Flask:** Open your browser and go to:
    - `http://127.0.0.1:5000`

- **If opening `index.html` directly:**
    - Ensure that the JavaScript API endpoints in your scripts are correctly pointing to:
        - `http://127.0.0.1:4000` (Node.js server)
        - `http://127.0.0.1:5000` (Flask server)

## 🛠️ Troubleshooting

### ❌ Port Conflicts

- Ensure ports 4000 (Node.js) and 5000 (Flask) are free.
- Modify the port numbers in `server.js` and `app.py` if needed.

### ❌ Missing Dependencies

- Run `npm install` (for Node.js) or
    ```bash
    pip install -r requirements.txt
    ```
    (for Python) to install required dependencies.

### ❌ Invalid API Key

- Verify that you have replaced the placeholder API key in `server.js` with a valid one.

### ❌ File Not Found Errors

- Ensure the CSV files (`text_emotion.csv`, `Suicide_Detection.csv`, `master.csv`) are placed correctly in the project directory.

## 📜 License

This project is open-source. Add your license details here (e.g., MIT License).

🚀 You’re now ready to run Serenify! If you encounter issues, check the Troubleshooting section or reach out to the project maintainers. 🎉