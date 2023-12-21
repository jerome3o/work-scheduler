"use client";

import { useState } from "react";
import { StudySchedule, StudyScheduleProcessingResult } from "../models";
import { useFilePicker } from "use-file-picker";

import StudyOptions from "./uploaders/StudyOptions";
import RosterUploader from "./uploaders/RosterUploader";

export default function SchedulerApp() {
  const [studyScheduleInfoList, setStudyScheduleInfoList] = useState<
    StudySchedule[]
  >([]);

  const { openFilePicker, filesContent, loading } = useFilePicker({
    accept: `.xlsx`,
    onFilesSuccessfullySelected: async ({
      plainFiles,
      filesContent,
    }: {
      plainFiles: File[];
      filesContent: any;
    }) => {
      const i = studyScheduleInfoList.length;
      setStudyScheduleInfoList((prevStudySchedules) => [
        ...prevStudySchedules,
        { name: plainFiles[0].name, content: plainFiles[0] },
      ]);
    },
  });

  function addStudySchedule() {
    openFilePicker();
  }

  function removeStudySchedule(index: number) {
    setStudyScheduleInfoList(
      studyScheduleInfoList.filter((studySchedule, i) => i !== index)
    );
  }

  async function processRoster(file: File) {
    // async sleep for a second
    await new Promise((resolve) => setTimeout(resolve, 1000));

    return {
      days: ["1", "2", "3", "4"],
    };
  }

  async function processStudySchedule(
    file: File
  ): Promise<StudyScheduleProcessingResult> {
    // async sleep for a second
    console.log("processing study schedule");
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("processing study schedule done");
    return {
      days: ["1", "2", "3", "4"],
      cohorts: ["alpha", "beta"],
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
        {studyScheduleInfoList.map((studySchedule, index) => {
          return (
            <StudyOptions
              key={studySchedule.name + index}
              studySchedule={studySchedule}
              processStudySchedule={processStudySchedule}
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
