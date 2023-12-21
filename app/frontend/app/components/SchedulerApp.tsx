"use client";

import StudyUploader from "./uploaders/StudyUploader";
import RosterUploader from "./uploaders/RosterUploader";

const requiredFiles: { title: string; fileType: string }[] = [
  { title: "study", fileType: "docx" },
  { title: "cohort", fileType: "xlsx" },
  { title: "Durations", fileType: "xlsx" },
  { title: "Jerome's just adding an example", fileType: "csv" },
];

export default function SchedulerApp() {
  return (
    <div className="scheduler-app-container">
      <div
        // this needs some cleaning up
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          padding: "0 10px",
        }}
      >
        <h1>Scheduler App</h1>
        <RosterUploader fileType="xlsx"></RosterUploader>
        <StudyUploader fileType="docx" title="Staff Roster"></StudyUploader>
        <StudyUploader fileType="xlsx" title="Task list"></StudyUploader>
        <button id="plus-button">+</button>
      </div>
      <div id="generate-button-div">
        <button id="generate-button">Generate</button>
      </div>
    </div>
  );
}
