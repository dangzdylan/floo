const TextSpeechFunction = async (text) => {
    if (text) {
      try {
        // Fetch the audio file from your Flask backend
        const response = await fetch('http://127.0.0.1:5000/text_to_speech', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text }), // Send the text as JSON
        });
  
        // Get the audio file and play it
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
      } catch (error) {
        console.error('Error playing audio:', error);
      }
    }
  };

  export default TextSpeechFunction;