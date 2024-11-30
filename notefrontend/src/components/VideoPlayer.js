import React from 'react';

const VideoPlayer = ({ encodedVideo }) => {
  const handlePlay = () => {
    // Dekodowanie base64
    const decodedVideo = atob(encodedVideo);

    // Tworzenie tablicy bajtów z ciągu znaków
    const byteArray = new Uint8Array(decodedVideo.length);
    for (let i = 0; i < decodedVideo.length; i++) {
      byteArray[i] = decodedVideo.charCodeAt(i);
    }

    // Tworzenie Bloba z tablicy bajtów
    const blob = new Blob([byteArray], { type: 'video/mp4' });

    // Tworzenie linku URL do Bloba
    const videoUrl = URL.createObjectURL(blob);

    // Odtwarzanie wideo
    const video = document.getElementById('myVideo');
    video.src = videoUrl;
    video.play();
  };

  return (
    <div className="mt-6">
   

    {/* Use the Tailwind 'mt-2' class to add margin top */}
    <video id="myVideo" width="640" height="360" controls className="mt-2" />

    {/* Use the Tailwind 'mt-2' class to add margin top */}
    <button
      onClick={handlePlay}
      className="bg-white text-black rounded-md py-1 px-3 font-semibold text-base mt-2"
    >
      Play
    </button>
  </div>
  );
};

export default VideoPlayer;