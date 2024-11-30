import AudioPlay from "../components/AddSound";
// import Recorder from "../components/RecordSound";
import FreqTable from "../components/FreqTable"


function HomePage() {
  

  return (
    <>
      <div className="bg-slate-800 h-[100vh] pt-10 text-white flex">
        <div className="flex-1"> {/* Increased margin for more space */}
          {/* <Recorder /> */}
          <AudioPlay />
        </div>
        <div className="flex-1">
          <FreqTable />
        </div>
      </div>
    </>
  );
}

export default HomePage;
