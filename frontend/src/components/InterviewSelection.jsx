import React, { useState } from 'react';
import './InterviewSelection.css'; // Make sure this path is correct
import axios from 'axios';
import TextSpeechFunction from './TextSpeechFunction';

function InterviewSelection(props) {
    const [interviewLength, setInterviewLength] = useState('');
    const textForSpeech = "So, tell me about yourself!"

    const handleSelect = (length) => {
        setInterviewLength(length);
    };

    const handleContinue = async() => {
        let thisLength = 5
        if (interviewLength === "demo"){
            thisLength = 2
        }
        props.afterSelection(thisLength)
    };

    return (
        <div className="interview-selection">
            <header>
                <div className="headerContainer">
                <p className="companyName">FLOO</p>
                </div>
            </header>
            <div className="selections">
                <div className="questionText">Select A Session</div>
                <div className="button-container">
                    <button 
                        className={`length-button ${interviewLength === 'demo' ? 'selected' : ''}`}
                        onClick={() => handleSelect('demo')}
                    >
                        Demo (2-3 min)
                    </button>
                    <button 
                        className={`length-button ${interviewLength === 'full' ? 'selected' : ''}`}
                        onClick={() => handleSelect('full')}
                    >
                        Normal (10-15 min)
                    </button>
                </div>
                <button 
                    className="continue-button" 
                    onClick={() => {handleContinue(); TextSpeechFunction(textForSpeech);}}
                    disabled={!interviewLength} // Disable if no option is selected
                >
                    Continue
                </button>
            </div>
        </div>
    );
}

export default InterviewSelection;
