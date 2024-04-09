# Authentication API

### User Registration

- **Endpoint:** `POST /register`
- **Description:** Create a new user account.

### User Login

- **Endpoint:** `POST /login`
- **Description:** Authenticate and generate access tokens.

### Token Refresh

- **Endpoint:** `POST /refresh-token`
- **Description:** Obtain a new access token using a refresh token.

### User Profile

- **Endpoint:** `GET /profile`
- **Description:** Retrieve user information (requires authentication).

## Password Reset

### Initiate Password Reset

- **Endpoint:** `POST /forgot-password`
- **Description:** Initiate the password reset process.

### Complete Password Reset

- **Endpoint:** `POST /reset-password`
- **Description:** Complete the password reset with a token.

## Logout

- **Endpoint:** `POST /logout`
- **Description:** Invalidate tokens to log out.

## Change Password

- **Endpoint:** `PATCH /change-password`
- **Description:** Allow users to change their password (requires authentication).

## User Deactivation

- **Endpoint:** `DELETE /deactivate-account`
- **Description:** Deactivate or delete a user account (requires authentication).

## Email Verification

### Send Verification Email

- **Endpoint:** `POST /send-verification-email`
- **Description:** Send an email with a verification link.

### Verify Email

- **Endpoint:** `POST /verify-email`
- **Description:** Verify the user's email address.

## User Listing (Admin)

- **Endpoint:** `GET /users`
- **Description:** Retrieve a list of users (requires admin privileges).

## GitHub OAuth2 Callback (still working)

- **Endpoint:** `GET /login/callback`
- **Description:** Handle GitHub OAuth2 callback.
  - **Query Parameters:**
    - `code`: Authorization code
    - `state`: State parameter (optional)
