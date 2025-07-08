# GitHub Webhook Event Viewer

This project is a Flask-based web application that serves as a webhook receiver for GitHub events. It listens for `Push`, `Pull Request`, and `Merge` events from a specified GitHub repository, stores them in a MongoDB database, and displays them in real-time on a simple web interface.

---

## Features

- **Real-time Event Display:** The user interface polls the server every 15 seconds to display the latest events.
- **Handles Multiple Event Types:** Correctly parses and displays formatted messages for:
  - `Push` events
  - `Pull Request` (opened) events
  - `Merge` events (when a pull request is merged)
- **MongoDB Integration:** All incoming webhook events are stored in a MongoDB database.
- **Clean & Minimalist UI:** A simple, clean interface to view the event stream.

---

## Project Structure

This project requires two separate GitHub repositories to function as intended:

1.  **`webhook-repo` (This Repository):** Contains the Flask application code that receives and processes the webhooks.
2.  **`action-repo`:** A separate repository where you will perform `git` actions. The webhooks configured on this repository will point to the running `webhook-repo` application.

---

## Setup and Installation

To run this project locally, you will need Python, Pip, and MongoDB installed.

**1. Clone the Repository:**
```bash
git clone https://github.com/patiltejas189/webhook-repo.git
cd webhook-repo
```

**2. Install Dependencies:**
Create a virtual environment (optional but recommended) and install the required Python packages.
```bash
pip install -r requirements.txt
```

**3. Start the MongoDB Database:**
Open a terminal and start the MongoDB daemon, pointing it to a local data directory.
```bash
# Make sure the 'Data/db' directory exists or choose another path
mongod --dbpath ./Data/db
```
*Keep this terminal running.*

**4. Start the Flask Application:**
Open a second terminal and run the Flask application.
```bash
python app.py
```
The application will be running at `http://localhost:5000`. *Keep this terminal running.*

---

## Demonstration Workflow

To see the application in action, you need to expose your local server to the internet and configure a webhook on your `action-repo`.

**1. Expose Your Local Server:**
Use a tool like [ngrok](https://ngrok.com/download) to create a public URL for your local server. Open a third terminal and run:
```bash
ngrok http 5000
```
Copy the public "Forwarding" URL provided by ngrok (e.g., `https://random-string.ngrok-free.app`).

**2. Configure the GitHub Webhook:**
- Navigate to your `action-repo` on GitHub.
- Go to **Settings > Webhooks > Add webhook**.
- **Payload URL:** Paste your ngrok URL and append `/webhook`.
- **Content type:** Set to `application/json`.
- **Events:** Select "Send me everything" or choose "Pushes" and "Pull requests".
- Click **Add webhook**.

**3. Trigger Events:**
Perform `git` actions in your local `action-repo` folder.

- **To Trigger a Push:**
  ```bash
  git add .
  git commit -m "Test push"
  git push
  ```

- **To Trigger a Pull Request:**
  1. Create and push a new branch (`git checkout -b my-feature && git push origin my-feature`).
  2. Go to GitHub and open a new pull request.

- **To Trigger a Merge:**
  1. Go to the open pull request on GitHub.
  2. Click "Merge pull request".

**4. Observe the Results:**
Watch the events appear in real-time on your browser at `http://localhost:5000`.