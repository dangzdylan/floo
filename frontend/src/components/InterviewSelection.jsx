import React, { useState } from 'react';
import './InterviewSelection.css'; // Make sure this path is correct

function InterviewSelection() {
    const [interviewLength, setInterviewLength] = useState('');

    const handleSelect = (length) => {
        setInterviewLength(length);
    };

    const handleContinue = () => {
        alert(`You selected: ${interviewLength}`);
    };

    return (
        <div className="interview-selection">
            <div className="questionText">What type of Interview?</div>
            <div className="button-container">
                <button 
                    className={`length-button ${interviewLength === 'quick' ? 'selected' : ''}`}
                    onClick={() => handleSelect('quick')}
                >
                    Quick (5-10 min)
                </button>
                <button 
                    className={`length-button ${interviewLength === 'longer' ? 'selected' : ''}`}
                    onClick={() => handleSelect('longer')}
                >
                    Longer (15-20 min)
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
