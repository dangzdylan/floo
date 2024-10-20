import React, {useEffect, useState} from 'react';
import './SynopsisScreen.css';
import AudioRecorder from './AudioRecorder';
import axios from 'axios';

const SynopsisScreen = (props) => {

    const [buttonsVisible, setButtonsVisible] = useState(true)
    const [detailsVisible, setDetailsVisible] = useState(false)

    const showDetails = () => {
        setButtonsVisible(false)
        setDetailsVisible(true)
    }

    useEffect(() => {
        axios.get("http://localhost:5000/perform_interview").then((response) => {
            console.log('Response data from Flask:', response.data);
            
        }).catch((error) => {
            console.error('Error fetching data:', error);
        })
    }, [detailsVisible])

    return (<div class="alvin">
        <div className="demo1">
            {buttonsVisible && <button class="demo" onClick={() => showDetails()}>Reveal Feedback and Analysis</button>} 
            {detailsVisible && <div>
                ok
            </div>
            }
        </div>
    </div>);

}


export default SynopsisScreen;