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
  const [dayOptions, setDayOptions] = useState<string[]>([]);
  const [cohortOptions, setCohortOptions] = useState<string[]>([]);

  async function process() {
    const result = await processStudySchedule(studySchedule.content);
    setDayOptions(result.days);
    setCohortOptions(result.cohorts);
  }

  useEffect(() => {
    process();
  }, []);

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
        <button>{dayOptions}</button>
        <button>{cohortOptions}</button>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
