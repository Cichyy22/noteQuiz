import { Unity, useUnityContext } from "react-unity-webgl";

function GamePage() {
  const { unityProvider } = useUnityContext({
    loaderUrl: "/assets/BuildQuiz.loader.js",
    dataUrl: "/assets/BuildQuiz.data",
    frameworkUrl: "/assets/BuildQuiz.framework.js",
    codeUrl: "/assets/BuildQuiz.wasm",
  });

  const handleClick = () => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    audioContext.resume().then(() => {
      console.log('AudioContext resumed successfully.');
    });

    console.log(unityProvider);
  };

  return (
    <div onClick={handleClick}>
      <Unity style={{
        width: "100%",
        justifySelf: "center",
         alignSelf: "center",
      }} unityProvider={unityProvider} />
    </div>
  );
}

export default GamePage;
  