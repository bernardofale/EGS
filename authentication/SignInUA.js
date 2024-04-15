// SignInUA.js
import React from 'react';
import { useHistory } from 'react-router-dom';

function SignInUA() {
  const history = useHistory();

  const handleClick = () => {
    history.push('/signin/ua'); // Redirects to /signin/ua
  };

  return (
    <div>
      <h2>Sign In with UA</h2>
      <button onClick={handleClick}>Sign In</button>
    </div>
  );
}

export default SignInUA;
