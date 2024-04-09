// SignInGitHub.js
import React from 'react';
import { useHistory } from 'react-router-dom';

function SignInGitHub() {
  const history = useHistory();

  const handleClick = () => {
    history.push('/signin/github'); // Redirects to /signin/github
  };

  return (
    <div>
      <h2>Sign In with GitHub</h2>
      <button onClick={handleClick}>Sign In</button>
    </div>
  );
}

export default SignInGitHub;
