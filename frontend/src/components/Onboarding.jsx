import React, { useState } from "react";
import "./Onboarding.css";
import axios from "axios";

const Onboarding = (props) => {
 
  const [selectedFile, setSelectedFile] = useState(null);
  //const [startButtonVisible, setStartButtonVisible] = useState(false);

  const handleFileUpload = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log(selectedFile)
  };

  const uploadHandler = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile); // append the PDF to FormData
    try {
      const response = await axios.post('http://localhost:5000/resumeParser', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully:', response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
    props.afterOnboarding()
  }

  return (
    <div className="thebody">
      <header>
        <div className="headerContainer">
          <p className="companyName">FLOO</p>
        </div>
      </header>
      <div className="onboardingContainer">
        <div className="welcomeText">Ace the behavioral interview</div>
        <div className="welcomeText2">AI curated coaching driven by your accomplishments</div>
        <div className="buttonsContainer">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="resumeButton"
            id="resumeButton"
          />
          
          {/* Conditional rendering: display an image if a file is selected */}
          {selectedFile ? (
            <div>
              <img
                src="resume.png" // Replace with your placeholder image path
                alt="Uploaded Resume"
                className="resumeImage" // Add a class for styling if needed
              />
              {selectedFile && <p>{selectedFile.name.replace('.pdf', '')}</p>}
              <button
                className="gettingStartedButton"
                onClick={uploadHandler}
              >
                Get Started
              </button>
            </div>
          ) : (
            <label htmlFor="resumeButton" className="customFileUpload">
              Upload your resume
            </label>
          )}
        </div>
      </div> 
    </div>
  );
};

export default Onboarding;