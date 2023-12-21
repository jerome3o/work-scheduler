import { useState } from "react";
import { useFilePicker } from "use-file-picker";
import { RosterProcessingResult } from "../../models";

export default function RosterUploader({
  fileType,
  processRoster,
}: {
  fileType: string;
  processRoster: (file: File) => RosterProcessingResult;
}) {
  const { openFilePicker, filesContent, loading, clear } = useFilePicker({
    accept: `.${fileType}`,
    onFilesSuccessfullySelected: ({
      plainFiles,
      filesContent,
    }: {
      plainFiles: File[];
      filesContent: any;
    }) => {
      // this callback is called when there were no validation errors
      console.log("onFilesSuccessfullySelected", plainFiles, filesContent);
      setSelectedFile(plainFiles[0]);
    },
  });

  const [selectedFile, setSelectedFile] = useState<File | undefined>(undefined);
  const [dayOptions, setDayOptions] = useState<string[]>([]);

  function onClear() {
    setSelectedFile(undefined);
    setDayOptions([]);
    clear();
  }

  function process() {
    if (!selectedFile) {
      return;
    }

    const result = processRoster(selectedFile);
    setDayOptions(result.days);
  }

  return (
    <div className="uploader-container">
      <h2>Upload Roster</h2>
      <p>{selectedFile?.name ?? "Please choose a file"}</p>
      {selectedFile ? (
        <div>
          <button>{dayOptions.length !== 0 ? dayOptions : "loading"}</button>
          <button onClick={onClear}>clear</button>
          <button onClick={process}>test upload</button>
        </div>
      ) : (
        <button onClick={openFilePicker}>upload ({fileType})</button>
      )}
    </div>
  );
}
