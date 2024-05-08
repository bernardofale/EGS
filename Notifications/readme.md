
## Service Setup

This service requires specific environment variables to function properly. Please create a file named `.env` in the root directory of your project and set the following variables:

**Required Environment Variables:**

* `MAIL_USERNAME`: Your email username for sending emails through the service.
* `MAIL_PASSWORD`: The password associated with your `MAIL_USERNAME`.
* `MAIL_FROM`: The email address that will appear as the sender in outgoing emails.
* `MAIL_PORT`: The port number used by your email server for communication (e.g., 587 for TLS).
* `MAIL_SERVER`: The hostname or IP address of your email server.
* `MAIL_FROM_NAME`: The name that will be displayed as the sender of the email (e.g., "Your Service Name").
* `TOKEN`: A secret token used for Telegram messages

**Example .env File:**

```
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
MAIL_FROM=noreply@your-service.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
MAIL_FROM_NAME="Your Service Name"
TOKEN=your_secret_telegram_token
```

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

**Building the Image**

1. Navigate to the directory containing your service's code (where your Dockerfile resides).
2. Run the following command in your terminal to build a Docker image named `myimage` from the Dockerfile in the current directory:

   ```bash
   docker build -t myimage .
   ```

   * `docker build`: This command instructs Docker to build a new image.
   * `-t myimage`: This option specifies the tag name for the image you're building. Replace `myimage` with a more descriptive name if desired.
   * `.`: The dot (.) indicates that the Dockerfile to use is located in the current working directory.

**Running the Container**

1. After the image is built successfully, run the following command to start a container based on the `myimage` image and name it `mycontainer`:

   ```bash
   docker run --name mycontainer -p 80:8000 myimage
   ```

   * `docker run`: This command instructs Docker to run a container from an existing image.
   * `--name mycontainer`: This option assigns a name to the container. You can choose a more descriptive name if preferred.
   * `-p 80:8000`: This option maps the container's port 8000 (where your service is likely listening) to the host machine's port 80. This allows you to access your service by visiting `http://localhost` in your web browser (assuming the container is running on the same machine).
   * `myimage`: This specifies the name of the Docker image you want to use to create the container.


**Accessing Your Service**

Once the container is running, you should be able to access your service by opening a web browser and navigating to `http://localhost` (assuming port 80 was mapped correctly). 

**Additional Notes:**

* The provided commands assume your service listens on port 8000 internally within the container. If your service uses a different port, modify the `-p` option accordingly (e.g., `-p 5000:5000` for port 5000).
* By default, Docker containers run in the background. To keep the container running even after you close your terminal window, you can use the `-d` option with the `docker run` command (e.g., `docker run -d --name mycontainer -p 80:8000 myimage`). However, this is generally not recommended for development purposes. It's better to stop and restart the container as needed during development.
* To stop the running container, use the following command, replacing `mycontainer` with the actual name you assigned:

   ```bash
   docker stop mycontainer
   ```

* To remove the container after you've stopped it, use:

   ```bash
   docker rm mycontainer
   ```

* To remove the built image, use:

   ```bash
   docker image rm myimage
   ```
