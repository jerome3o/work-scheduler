import { useState } from "react";
import { useFilePicker } from "use-file-picker";

export default function RosterUploader({ fileType }: { fileType: string }) {
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
      setSelectedFile(plainFiles[0].name);
    },
  });

  const [selectedFile, setSelectedFile] = useState<string | undefined>(
    undefined
  );

  function onClear() {
    setSelectedFile(undefined);
    clear();
  }

  return (
    <div className="uploader-container">
      <h2>Upload Roster</h2>
      <p>{selectedFile ?? "Please choose a file"}</p>
      {selectedFile ? (
        <div>
          <button>TODO: make dropdown</button>
          <button onClick={onClear}>clear</button>
        </div>
      ) : (
        <button onClick={openFilePicker}>upload ({fileType})</button>
      )}
    </div>
  );
}
