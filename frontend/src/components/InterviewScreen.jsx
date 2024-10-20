import React, {useEffect, useState} from 'react';
import './InterviewScreen.css';
import AudioRecorder from './AudioRecorder';
import axios from 'axios';

const behavioralQuestions = [
    "Tell me about a time when you faced a difficult technical problem. How did you approach it?",
    "Describe a situation where you had to work with a challenging team member. How did you handle it?",
    "Give an example of a project where you had to quickly learn a new technology or framework.",
    "Tell me about a time when you received critical feedback. How did you respond and improve?",
    "Describe a situation where you had to balance competing priorities or deadlines. How did you manage it?",
    "Can you share an example of a time you took ownership of a task or project?",
    "Tell me about a time when you had to collaborate with a non-technical team member. How did you ensure effective communication?",
    "Describe a situation where you had to make a decision with incomplete information. How did you handle it?",
    "Tell me about a project where things didn’t go as planned. What did you do to address the issues?",
    "Describe a time when you had to work under pressure. How did you maintain productivity?",
    "Tell me about a time when you had to debug a complex issue. How did you approach the problem?",
    "Can you share an example of a time when you helped a team member resolve a technical issue?",
    "Tell me about a time you went above and beyond in a project. What motivated you?",
    "Describe a situation where you had to adapt to significant changes in a project. How did you adjust?",
    "Tell me about a time when you contributed to improving a process or workflow. What was the outcome?"
];

const InterviewScreen = (props) => {

    const [question, setQuestion] = useState("Tell me about yourself.")
    const [questionsLeft, setQuestionsLeft] = useState(props.length)
    const [time, setTime] = useState(60)
    const [questionsUsed, setQuestionsUsed] = useState(["Tell me about yourself."])
    const [isActive, setIsActive] = useState(false);

    useEffect(() => {
        // Check if time is greater than 0 before starting the interval
        if (!isActive) {
            return;
        }
        if (time > 0) {
            const interval = setInterval(() => {
            setTime((prevTime) => prevTime - 1); // Decrement time by 1
            }, 1000); // Run every 1 second (1000 ms)

            // Cleanup function to clear the interval when component unmounts or time changes
            return () => clearInterval(interval);
        } else {
            setQuestionsLeft(questionsLeft-1)
            if (questionsLeft===0){
                props.afterInterview()
            }
            let outsideRandomQuestion = "?"
            while (true) {
                let randomQuestion = behavioralQuestions[Math.floor(Math.random() * behavioralQuestions.length)]
                if (!questionsUsed.includes(randomQuestion)){
                    setQuestion(randomQuestion)
                    outsideRandomQuestion = randomQuestion
                    break
                }
            }
            setQuestionsUsed([...questionsUsed, outsideRandomQuestion])
            setTime(60)
        }
    }, [time]); // Dependency array, will run effect when 'time' changes

    const buttonClickHandler = () => {
        if (time===60){
            setIsActive(true);
            setTime(59)
        } else {

            setIsActive(false);
            setQuestionsLeft(questionsLeft-1)
            if (questionsLeft===0){
                props.afterInterview()
            }
            let outsideRandomQuestion = "?"
            while (true) {
                let randomQuestion = behavioralQuestions[Math.floor(Math.random() * behavioralQuestions.length)]
                if (!questionsUsed.includes(randomQuestion)){
                    setQuestion(randomQuestion)
                    outsideRandomQuestion = randomQuestion
                    break
                }
            }
            setQuestionsUsed([...questionsUsed, outsideRandomQuestion])
            setTime(60)
        }
    }


    return (<div>
        <div class="demo2">{question}</div>
        {/*<AudioRecorder/>*/}
        <button onClick={() => buttonClickHandler()}>
            {time===60 ? "Start" : "Stop"} Recording
        </button>
        <div class="demo">Timer: {time}</div>
    </div>);

}


export default InterviewScreen;