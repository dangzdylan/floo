import './App.css';
import React, { useState } from 'react';
import InterviewSelection from './components/InterviewSelection';
import Onboarding from './components/Onboarding';
function App() {

  const [onboardingVisible, setOnboardingVisible] = useState(true)
  const [interviewSelectionVisible, setInterviewSelectionVisible] = useState(false)

  const afterOnBoardHandler = () => {
    setOnboardingVisible(false)
    setInterviewSelectionVisible(true)
  }

  return (
    <div className="App">
      {onboardingVisible && (<Onboarding afterOnboarding={() => afterOnBoardHandler()}/>)}
      {interviewSelectionVisible && (<InterviewSelection />)}
    </div>
  );
}

export default App;
