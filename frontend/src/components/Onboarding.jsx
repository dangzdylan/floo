import React, { useState } from "react";
import "./Onboarding.css";
import axios from "axios";

const Onboarding = () => {
 
  const [selectedFile, setSelectedFile] = useState(null);

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