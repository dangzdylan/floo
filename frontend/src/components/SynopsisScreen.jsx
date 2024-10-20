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

    return (<div class="demo">
        {buttonsVisible && <button class="demo" onClick={() => showDetails()}>View Past Interview Feedback and Analysis</button>} 
        {buttonsVisible && <button class="demo" onClick={() => props.afterSynopsis()}>Practice another interview!</button>}
        {detailsVisible && <div>
            ok
        </div>
        }
    </div>);

}


export default SynopsisScreen;