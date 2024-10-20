import React, { useState } from 'react';
import './InterviewSelection.css'; // Make sure this path is correct
import axios from 'axios';

function InterviewSelection(props) {
    const [interviewLength, setInterviewLength] = useState('');

    const handleSelect = (length) => {
        setInterviewLength(length);
    };

    const handleContinue = async() => {
        let thisLength = 5
        if (interviewLength === "demo"){
            thisLength = 2
        }
        const jsonPayload = {
            "length": thisLength, // Sending the 'length' value as JSON
        };
        try {
            const response = await axios.post('http://localhost:5000/resumeParser', jsonPayload, {
              headers: {
                'Content-Type': 'application/json',
              },
            });
            console.log('JSON sent successfully:', response.data);
        } catch (error) {
            console.error('Error sending JSON:', error);
        }
        props.afterSelection(thisLength)
    };

    return (
        <div className="interview-selection">
            <div className="questionText">What type of Interview?</div>
            <div className="button-container">
                <button 
                    className={`length-button ${interviewLength === 'demo' ? 'selected' : ''}`}
                    onClick={() => handleSelect('demo')}
                >
                    Demo (2-3 min)
                </button>
                <button 
                    className={`length-button ${interviewLength === 'normal' ? 'selected' : ''}`}
                    onClick={() => handleSelect('normal')}
                >
                    Normal (10-15 min)
                </button>
            </div>
            <button 
                className="continue-button" 
                onClick={handleContinue} 
                disabled={!interviewLength} // Disable if no option is selected
            >
                Continue
            </button>
        </div>
    );
}

export default InterviewSelection;
