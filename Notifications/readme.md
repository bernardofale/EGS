
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
