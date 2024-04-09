import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import SignInUA from './SignInUA';
import SignInGitHub from './SignInGithub';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/signin/ua">Sign In with UA</Link>
            </li>
            <li>
              <Link to="/signin/github">Sign In with GitHub</Link>
            </li>
          </ul>
        </nav>

        <Route path="/signin/ua" component={SignInUA} />
        <Route path="/signin/github" component={SignInGitHub} />
      </div>
    </Router>
  );
}

export default App;
