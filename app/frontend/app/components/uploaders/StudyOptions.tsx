import { useState } from "react";
import { useFilePicker } from "use-file-picker";

import { StudySchedule } from "../../models";

export default function StudyUploader({
  studySchedule,
  removeFunction,
}: {
  studySchedule: StudySchedule;
  removeFunction: () => void;
}) {
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
        <button>Cohort</button>
        <button>Day</button>
        <button onClick={removeFunction}>x</button>
      </div>
    </div>
  );
}
