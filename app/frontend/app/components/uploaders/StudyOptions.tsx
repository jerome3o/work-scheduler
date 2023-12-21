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
  }: {
    newDay: string | undefined;
    newCohort: string | undefined;
  }) {
    setStudyScheduleWithOptions({
      ...studyScheduleWithOptions,
      options: {
        day: newDay ?? studyScheduleWithOptions.options.day,
        cohort: newCohort ?? studyScheduleWithOptions.options.cohort,
      },
    });
  }

  if (!options) process();

  return (
    <div className="uploader-container">
      <h2>{studyScheduleWithOptions.studySchedule.name}</h2>
      <div className="button-layout">
        <DaySelect
          options={options?.days ?? []}
          value={studyScheduleWithOptions.options.day}
          setValue={(value: string) =>
            handleChange({ newDay: value, newCohort: undefined })
          }
        />
        {/* text input that has placeholder text "cohort" */}
        <input
          type="text"
          placeholder="cohort name"
          value={studyScheduleWithOptions.options.cohort}
          onChange={(e) =>
            handleChange({ newCohort: e.target.value, newDay: undefined })
          }
        ></input>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
