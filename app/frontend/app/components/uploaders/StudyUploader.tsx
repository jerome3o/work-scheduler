import { useState } from "react";
import { useFilePicker } from "use-file-picker";

export default function StudyUploader({
  fileType,
  title,
}: {
  fileType: string;
  title: string;
}) {
  const { openFilePicker, filesContent, loading } = useFilePicker({
    accept: `.${fileType}`,
  });

  function onClick() {
    openFilePicker();
    console.log(filesContent)
    console.log("nice");
  }

  return (
    <div className="uploader-container">
      <h2>Upload: {title}</h2>
      <button onClick={onClick}>upload ({fileType})</button>
    </div>
  );
}
