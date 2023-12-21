import { useState } from "react";

import { StudySchedule, StudyScheduleProcessingResult } from "../../models";
import DaySelect from "./DaySelect";

export default function StudyUploader({
  studySchedule,
  processStudySchedule,
  removeFunction,
  day,
  setDay,
  cohort,
  setCohort,
}: {
  studySchedule: StudySchedule;
  processStudySchedule: (file: File) => Promise<StudyScheduleProcessingResult>;
  removeFunction: () => void;
  day: string;
  setDay: (day: string) => void;
  cohort: string;
  setCohort: (cohort: string) => void;
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
        <DaySelect
          options={options?.days ?? []}
          value={day}
          setValue={setDay}
        />
        {/* text input that has placeholder text "cohort" */}
        <input
          type="text"
          placeholder="cohort name"
          value={cohort}
          onChange={(e) => setCohort(e.target.value)}
        ></input>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
