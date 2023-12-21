import { useState } from "react";
import { useFilePicker } from "use-file-picker";
import { RosterProcessingResult } from "../../models";
import DaySelect from "./DaySelect";

export default function RosterUploader({
  fileType,
  processRoster,
  changeRoster,
}: {
  fileType: string;
  processRoster: (file: File) => Promise<RosterProcessingResult>;
  changeRoster: (file: File | undefined) => void;
}) {
  const { openFilePicker, filesContent, loading, clear } = useFilePicker({
    accept: `.${fileType}`,
    onFilesSuccessfullySelected: async ({
      plainFiles,
      filesContent,
    }: {
      plainFiles: File[];
      filesContent: any;
    }) => {
      setSelectedFile(plainFiles[0]);
      await process(plainFiles[0]);
      changeRoster(plainFiles[0]);
    },
  });

  const [selectedFile, setSelectedFile] = useState<File | undefined>(undefined);
  const [dayOptions, setDayOptions] = useState<string[]>([]);

  function onClear() {
    setSelectedFile(undefined);
    changeRoster(undefined);
    setDayOptions([]);
    clear();
  }

  async function process(file: File) {
    const result = await processRoster(file);
    setDayOptions(result.days);
  }

  return (
    <div className="uploader-container">
      <h2>Upload Roster</h2>
      <p>{selectedFile?.name ?? "Please choose a file"}</p>
      {selectedFile ? (
        <div className="button-layout">
          <DaySelect options={dayOptions} />
          <button onClick={onClear}>x</button>
        </div>
      ) : (
        <button onClick={openFilePicker}>upload ({fileType})</button>
      )}
    </div>
  );
}
