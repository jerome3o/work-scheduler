import { useState, useEffect } from "react";

import { StudySchedule, StudyScheduleProcessingResult } from "../../models";

export default function StudyUploader({
  studySchedule,
  processStudySchedule,
  removeFunction,
}: {
  studySchedule: StudySchedule;
  processStudySchedule: (file: File) => Promise<StudyScheduleProcessingResult>;
  removeFunction: () => void;
}) {
  const [options, setOptions] = useState<
    StudyScheduleProcessingResult | undefined
  >(undefined);

  async function process() {
    const result = await processStudySchedule(studySchedule.content);
    setOptions(result);
  }

  if (!options) process();

  return (
    <div className="uploader-container">
      <h2>{studySchedule.name}</h2>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          gap: "10px",
          width: "100%",
        }}
      >
        <button>{options?.days}</button>
        <button>{options?.cohorts}</button>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
