import { useState } from "react";

import {
  StudyScheduleWithOptions,
  StudyScheduleProcessingResult,
} from "../../models";
import DaySelect from "./DaySelect";

export default function StudyUploader({
  studyScheduleWithOptions,
  setStudyScheduleWithOptions,
  processStudySchedule,
  removeFunction,
}: {
  studyScheduleWithOptions: StudyScheduleWithOptions;
  setStudyScheduleWithOptions: (
    studyScheduleWithOptions: StudyScheduleWithOptions
  ) => void;
  processStudySchedule: (file: File) => Promise<StudyScheduleProcessingResult>;
  removeFunction: () => void;
}) {
  const [options, setOptions] = useState<
    StudyScheduleProcessingResult | undefined
  >(undefined);

  async function process() {
    const result = await processStudySchedule(
      studyScheduleWithOptions.studySchedule.content
    );
    setOptions(result);
  }

  function handleChange({
    newDay,
    newCohort,
    newPatients,
  }: {
    newDay: string | undefined;
    newCohort: string | undefined;
    newPatients: string | undefined;
  }) {
    setStudyScheduleWithOptions({
      ...studyScheduleWithOptions,
      options: {
        day: newDay ?? studyScheduleWithOptions.options.day,
        cohort: newCohort ?? studyScheduleWithOptions.options.cohort,
        patients: newPatients ?? studyScheduleWithOptions.options.patients,
      },
    });
  }

  if (!options) process();

  return (
    <div className="uploader-container">
      <h2>{studyScheduleWithOptions.studySchedule.name}</h2>
      <div className="button-layout">
      {/* Study Day text input field */}
      <p>Day:</p>
      <input
          type="text"
          placeholder="Study Day"
          value={studyScheduleWithOptions.options.day}
          onChange={(e) =>
            handleChange({ newCohort: undefined, newDay: e.target.value, newPatients: undefined })
          }
        ></input>
        {/* Cohort text input field */}
        <p>Cohort:</p>
        <input
          type="text"
          placeholder="Cohort"
          value={studyScheduleWithOptions.options.cohort}
          onChange={(e) =>
            handleChange({ newCohort: e.target.value, newDay: undefined, newPatients: undefined})
          }
        ></input>
        {/* patients text input field */}
        <p>Cohort Size:</p>
        <input
          type="text"
          placeholder="Cohort Size"
          value={studyScheduleWithOptions.options.patients}
          onChange={(e) =>
            handleChange({ newCohort: undefined, newDay: undefined, newPatients: e.target.value })
          }
        ></input>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
