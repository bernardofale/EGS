## GestAccount

### To run this project you must configure a .env file in `/Notifications` directory with  [this structure](Notifications/readme.md)

**Important Notes:**

* **Security:**  Never store sensitive information like passwords directly in the `.env` file. Consider using a secure environment variable management solution in production environments.
* **Restart the service:** After creating or modifying the `.env` file, ensure you restart your service for the changes to take effect.


**Deploying  with Docker**

This guide outlines the steps to deploy your service using Docker containers. 

**Prerequisites:**

* Docker installed and running on your system. You can find installation instructions for your operating system on the official Docker website: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

**Deploy with docker compose**


```bash
   docker compose up -d
   ```
* `-d or --detach`: This option is to run in Detached mode: Run containers in the background.
* `--build	`: This option is to build images before starting containers

To stop de containers you must run:

```bash
   docker compose down
   ```
