import { useState } from "react";
import { useFilePicker } from "use-file-picker";
import { RosterProcessingResult } from "../../models";

export default function RosterUploader({
  fileType,
  processRoster,
}: {
  fileType: string;
  processRoster: (file: File) => Promise<RosterProcessingResult>;
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

  async function process() {
    if (!selectedFile) {
      return;
    }

    const result = await processRoster(selectedFile);
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
