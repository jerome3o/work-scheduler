import { useState } from "react";

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
      <div className="button-layout">
        <select>
          {options?.days.map((day) => {
            return <option>{day}</option>;
          })}
        </select>
        {/* text input that has placeholder text "cohort" */}
        <input type="text" placeholder="cohort name"></input>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
