import React, { useState, useRef } from 'react';
import axios from 'axios';
import "./AudioRecorder.css";


function AudioRecorder({ buttonClickHandler}) {
    const [recording, setRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
  
    const startRecording = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];
  
        mediaRecorderRef.current.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };
  
        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
          const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
          sendAudioToBackend(audioFile);  // Call backend function to upload the file
        };
  
        mediaRecorderRef.current.start();
        setRecording(true);
      } catch (err) {
        console.error('Error accessing microphone:', err);
      }
    };
  
    const stopRecording = () => {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
        setRecording(false);
      }
    };
  
    const toggleRecording = () => {
      if (recording) {
        stopRecording();
      } else {
        startRecording();
      }
    };
  
    const sendAudioToBackend = async (file) => {
      const formData = new FormData();
      formData.append('audio', file);
  
      try {
        await axios.post('http://127.0.0.1:5000/upload_audio', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        alert('Audio file sent to the server successfully!');
      } catch (error) {
        console.error('Error uploading audio:', error);
      }
    };
  
    return (
        <button onClick={() => {toggleRecording(); buttonClickHandler();}}>
          {recording ? 'Stop Recording' : 'Start Recording'}
        </button>
    );
  }
  export default AudioRecorder;
  

