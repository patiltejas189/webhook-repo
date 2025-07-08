# GitHub Webhook Event Viewer

This application listens for GitHub webhooks, stores the events in a MongoDB database, and displays them on a web interface.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- MongoDB

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required Python packages:**

    Open your terminal or command prompt and run the following command in the project directory:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start your MongoDB server.**

    Make sure your MongoDB instance is running on `localhost:27017`.

2.  **Run the Flask application:**

    In your terminal or command prompt, run the following command:

    ```bash
    python app.py
    ```

3.  **View the application in your browser:**

    Open your web browser and navigate to the following URL:

    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Webhook Configuration

To receive events from a GitHub repository, you need to configure a webhook:

1.  Go to your GitHub repository's **Settings** page.
2.  Click on **Webhooks** in the left sidebar.
3.  Click the **Add webhook** button.
4.  In the **Payload URL** field, enter the URL of your running application's webhook endpoint (e.g., `http://<your-public-ip>:5000/webhook`).
5.  For **Content type**, select `application/json`.
6.  Under **Which events would you like to trigger this webhook?**, select **Send me everything** or choose individual events (`Pushes`, `Pull requests`).
7.  Click **Add webhook**.

<!-- Project Running process -->


Step 1: Create a new branch and make a change.
Run these commands in your terminal, inside your action-repo folder.

# Command 1: Create a new branch called "feature-branch" and switch to it
git checkout -b feature-branch

# Command 2: Create a new file
echo "This is a new feature for the pull request" > feature-file.txt

# Command 3: Add and commit the new file
git add .
git commit -m "Adding a new feature"

# Command 4: Push the new branch to GitHub
git push origin feature-branch

bash


Step 2: Create the Pull Request on GitHub.

Go to your action-repo on GitHub: https://github.com/patiltejas189/action-repo
You will see a message saying "feature-branch had recent pushes". Click the "Compare & pull request" button.
On the next page, click the green "Create pull request" button.
This action triggers the "Pull Request" webhook. You will see the new event on http://localhost:5000.
How to Trigger a MERGE Event
Step 3: Merge the Pull Request on GitHub.

After creating the pull request, stay on that page on GitHub.
Click the green "Merge pull request" button.
Click the "Confirm merge" button.
This action triggers the "Merge" webhook. You will see the "merged branch" event appear on http://localhost:5000.