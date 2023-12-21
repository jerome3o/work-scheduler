"use client";

import { useState } from "react";
import { StudySchedule } from "../models";
import { useFilePicker } from "use-file-picker";

import StudyOptions from "./uploaders/StudyOptions";
import RosterUploader from "./uploaders/RosterUploader";

export default function SchedulerApp() {
  const [studySchedules, setStudySchedules] = useState<StudySchedule[]>([]);

  const { openFilePicker, filesContent, loading } = useFilePicker({
    accept: `.xlsx`,
    onFilesSuccessfullySelected: ({
      plainFiles,
      filesContent,
    }: {
      plainFiles: File[];
      filesContent: any;
    }) => {
      setStudySchedules([
        ...studySchedules,
        { name: plainFiles[0].name, content: plainFiles[0] },
      ]);
    },
  });

  function addStudySchedule() {
    openFilePicker();
  }

  function removeStudySchedule(index: number) {
    setStudySchedules(studySchedules.filter((studySchedule, i) => i !== index));
  }

  function processRoster(file: File) {
    return {
      days: ["1", "2", "3", "4"],
    };
  }

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
        <RosterUploader
          fileType="xlsx"
          processRoster={processRoster}
        ></RosterUploader>
        {studySchedules.map((studySchedule, index) => {
          return (
            <StudyOptions
              key={studySchedule.name + index}
              studySchedule={studySchedule}
              removeFunction={() => removeStudySchedule(index)}
            />
          );
        })}
        <button onClick={addStudySchedule} id="plus-button">
          +
        </button>
      </div>
      <div id="generate-button-div">
        <button id="generate-button">Generate</button>
      </div>
    </div>
  );
}
