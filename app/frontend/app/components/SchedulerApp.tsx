"use client";

import { useState } from "react";
import {
  StudySchedule,
  StudyScheduleProcessingResult,
  StudyScheduleWithOptions,
  StudyScheduleOptions,
} from "../models";
import { useFilePicker } from "use-file-picker";
import ApiWrapper from "../apiWrapper";

import StudyOptions from "./uploaders/StudyOptions";
import RosterUploader from "./uploaders/RosterUploader";

export default function SchedulerApp() {
  const [studyScheduleList, setStudyScheduleList] = useState<
    StudyScheduleWithOptions[]
  >([]);
  const [roster, setRoster] = useState<File | undefined>(undefined);
  const [rosterDay, setRosterDay] = useState<string | undefined>(undefined);

  const apiWrapper = new ApiWrapper();

  const { openFilePicker, filesContent, loading } = useFilePicker({
    accept: `.xlsx`,
    onFilesSuccessfullySelected: async ({
      plainFiles,
      filesContent,
    }: {
      plainFiles: File[];
      filesContent: any;
    }) => {
      setStudyScheduleList((prevStudySchedules) => [
        ...prevStudySchedules,
        {
          studySchedule: { name: plainFiles[0].name, content: plainFiles[0] },
          options: { day: "", cohort: "" },
        },
      ]);
    },
  });

  function addStudySchedule() {
    openFilePicker();
  }

  function removeStudySchedule(index: number) {
    setStudyScheduleList(
      studyScheduleList.filter((studySchedule, i) => i !== index)
    );
  }

  async function processRoster(file: File) {
    return await apiWrapper.processRoster(file);
  }

  async function processStudySchedule(
    file: File
  ): Promise<StudyScheduleProcessingResult> {
    return await apiWrapper.processStudySchedule(file);
  }

  async function generateSchedule() {
    if (!roster) {
      alert("Please select a roster");
      return;
    }
    if (studyScheduleList.length === 0) {
      alert("Please select at least one study schedule");
      return;
    }

    const studyScheduleFiles = studyScheduleList.map(
      (studySchedule) => studySchedule.studySchedule.content
    );

    const workDay = await apiWrapper.generateWorkDay(
      studyScheduleFiles,
      roster,
      {
        studyScheduleOptions: studyScheduleList.map(
          (studySchedule) => studySchedule.options
        ),
        rosterDay: rosterDay ?? "",
      }
    );
    console.log(workDay);
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
        <h1>NZCR Scheduler</h1>
        <RosterUploader
          fileType="xlsx"
          processRoster={processRoster}
          changeRoster={setRoster}
          rosterDay={rosterDay}
          setRosterDay={setRosterDay}
        ></RosterUploader>
        <h3>Study Schedules:</h3>
        {studyScheduleList.map((studySchedule, index) => {
          return (
            <StudyOptions
              key={studySchedule.studySchedule.name + index}
              studyScheduleWithOptions={studySchedule}
              setStudyScheduleWithOptions={(
                studyWithOptions: StudyScheduleWithOptions
              ) => {
                const newStudySchedules = [...studyScheduleList];
                newStudySchedules[index] = studyWithOptions;
                setStudyScheduleList(newStudySchedules);
              }}
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
        <button id="generate-button" onClick={generateSchedule}>
          Generate Task Allocations
        </button>
      </div>
    </div>
  );
}
