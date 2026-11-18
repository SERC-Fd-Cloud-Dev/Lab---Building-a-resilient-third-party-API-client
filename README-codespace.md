# Using your Cloud Development Codespace

This guide explains the tools built into the lab development environment. **For the lab tasks themselves, follow the exercise instructions in [README.md](README.md) and the linked exercise files.**

## 1. Open your Codespace

1. Open your **own lab repository** on GitHub.
2. Select **Code → Codespaces**, then create or reopen your Codespace.
3. Wait for VS Code to load. Open **Terminal → New Terminal** for commands shown in the lab.

The container uses the lab's configured development image. When first created, it runs an environment check for tools such as Python, Git, Docker and database utilities. A warning about a database that has not been started does not necessarily mean the Codespace is broken.

## 2. Ask the Cloud Dev Tutor

1. Open **GitHub Copilot Chat** in VS Code.
2. Choose **Cloud Dev Tutor** from the agent selector.
3. Describe what you are trying to do, what you have tried and any error message. Include relevant code or *redacted* logs when useful.

The tutor automatically draws on skills such as FastAPI, Git, databases, Postman, testing and deployment. You do not need to select a separate topic agent.

**Useful questions:**
- “My FastAPI request returns 422. What should I inspect?”
- “Why does this PostgreSQL connection fail?”
- “Generate tests for the endpoint I have already written and explain each assertion.”
- “Explain this Git merge conflict without changing my code.”

The tutor can **explain, troubleshoot and generate tests**. It may help with a separate, student-owned project README. It **must not write application implementations or edit the lab's existing Markdown instructions**, including the lab README, exercises and homework. Review anything it suggests; custom instructions do not guarantee compliance.

## 3. Start services with Services Manager

Some practicals need a database or another background service; other practicals do not.

1. Look for the **Services Manager** view in the VS Code sidebar (or open it from the VS Code views/Command Palette if available).
2. Select the service required by the current lab and use the available **Start** control.
3. Check its reported status. If it fails, look for any service output/logs and review the lab's setup instructions.
4. Use **Stop** when you have finished with a service you no longer need. **Restart** may help after configuration changes, if the extension offers it.

Start only the services required for the exercise. Stopping a service is different from deleting its data; do not use reset/remove actions unless the lab explicitly asks you to.

**Can't find Services Manager?** Check the **Extensions** view to see whether it is installed and enabled. The template currently supplies a Services Manager setting but does **not explicitly install the extension** in `.devcontainer/devcontainer.json`; it may be provided by the container image or another setup step. Ask your lecturer if it is missing. The exact buttons may vary by extension version.

## 4. Connect to databases with SQLTools

The container config provides SQLTools and drivers for multiple databases. In VS Code:

1. Start the required database service, if applicable.
2. Open the **SQLTools** view and choose an available connection.
3. Connect and explore the database; use the lab's instructions before creating or changing data.

The template defines connection profiles for **MariaDB (3306)**, **PostgreSQL (5432)** and **SQL Server (1433)** using the container's local network. A **SQLite** driver is also included for file-based databases. A saved connection does not mean its server is already running.

If a connection fails, first check the service status, selected connection and whether the exercise requires any setup. Use lab-only credentials; never copy real passwords or tokens into Copilot Chat or commits.

## 5. Run and view your API

Run your application using the **terminal command provided in the lab**. The Codespace is configured to forward **port 8000** (labelled *FastAPI*).

- Open the **Ports** panel in VS Code to see forwarded services.
- Use the action to **Open in Browser** for port 8000 once the API is running.
- For a FastAPI application, try `/docs` on its running address to view Swagger UI.

Port 8000 is configured as **private**. Do not make it public unless your lecturer explicitly instructs you to.

## 6. Other useful VS Code features

| Feature | What to use it for |
| --- | --- |
| **Postman extension** | Send API requests, change headers/body, inspect responses and organise tests. |
| **Source Control (Git)** | Check changed files, create commits, manage branches and push your work to GitHub. |
| **GitHub Actions extension** | Inspect workflow runs and failure logs when the exercise uses CI/CD. |
| **Terminal** | Run the lab's Python, Git, testing and other commands in the container. |
| **Extensions view** | Check whether the tools needed for your lab are installed/enabled. |

**Save your work:** commit and push the files you want to keep. You can stop and reopen a Codespace, but deleting it is not the same as closing the editor. Avoid rebuilding or deleting it as a first troubleshooting step.

If a tool or service is unavailable, compare what you see with the current lab instructions and ask your lecturer for help.
