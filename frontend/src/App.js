import './App.css';
import React, { useState } from 'react';
import InterviewSelection from './components/InterviewSelection';
import Onboarding from './components/Onboarding';
import InterviewScreen from './components/InterviewScreen';
import SynopsisScreen from './components/SynopsisScreen';
//import AudioRecorder from './components/AudioRecorder';
function App() {

  const [onboardingVisible, setOnboardingVisible] = useState(true)
  const [interviewSelectionVisible, setInterviewSelectionVisible] = useState(false)
  const [interviewScreenVisible, setInterviewScreenVisible] = useState(false)
  const [interviewLength, setInterviewLength] = useState(0);
  const [synopsisScreenVisible, setSynopsisScreenVisible] = useState(false)

  const afterOnBoardHandler = () => {
    setOnboardingVisible(false)
    setInterviewSelectionVisible(true)
  }

  const afterSelectionHandler = (length) => {
    setInterviewLength(length)
    setInterviewSelectionVisible(false)
    setInterviewScreenVisible(true)
  }

  const afterInterviewHandler = () => {
    setInterviewScreenVisible(false)
    setSynopsisScreenVisible(true)
  }

  const afterSynopsisHandler = () => {
    setSynopsisScreenVisible(false)
    setOnboardingVisible(true)
  }

  return (
    <div className="App">
      {onboardingVisible && (<Onboarding afterOnboarding={() => afterOnBoardHandler()}/>)}
      {interviewSelectionVisible && (<InterviewSelection afterSelection={(length) => afterSelectionHandler(length)}/>)}
      {interviewScreenVisible && (<InterviewScreen length={interviewLength} afterInterview={afterInterviewHandler}/>)}
      {synopsisScreenVisible && (<SynopsisScreen afterSynopsis={afterSynopsisHandler}/>)}
    </div>
  );
}

export default App;
