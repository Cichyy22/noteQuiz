import React from 'react';

const AudioTimer = ({ isRunning,
    setIsRunning,
    elapsedTime,
    setElapsedTime, }) => {

    React.useEffect(() => {
        let intervalId;
        if (isRunning) {
            // setting time from 0 to 1 every 10 milisecond using javascript setInterval method
            intervalId = setInterval(() => setElapsedTime(elapsedTime + 1), 10);
        }
        return () => clearInterval(intervalId);
    }, [isRunning, elapsedTime]);

    //  calculation
    const minutes = Math.floor((elapsedTime % 360000) / 6000);
    const seconds = Math.floor((elapsedTime % 6000) / 100);

    return (
        <div className=" text-[25px] mt-4 font-semibold " >
            <div className="time">{minutes.toString().padStart(2, "0")}:
                <span className=" w-[23px]  "> {seconds.toString().padStart(2, "0")}</span>
            </div>
        </div>
    );
};

export default AudioTimer;