import React, { useState } from "react";
import "./Onboarding.css";
import { upload } from "@testing-library/user-event/dist/upload";

const Onboarding = () => {
 
  const [selectedFile, setSelectedFile] = useState(null);
  //const [startButtonVisible, setStartButtonVisible] = useState(false);

  const handleFileUpload = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log(selectedFile)
    //setStartButtonVisible(true);
  };

  const uploadHandler = () => {
    alert(selectedFile.name)
  }

  return (
    <div className="onboardingContainer">
      <div className="welcomeText">Welcome to FLOO!</div>
      <div className="buttonsContainer">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          className="resumeButton"
        />
        {selectedFile && <p>Selected file: {selectedFile.name}</p>}
        <button
        className="gettingStartedButton"
        onClick={uploadHandler}
        >
        Get Started
        </button>
      </div>
    </div>
  );
};

export default Onboarding;