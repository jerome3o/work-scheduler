import { useState } from "react";

export default function Uploader({
  fileType,
  title,
}: {
  fileType: string;
  title: string;
}) {
  const [clickCount, setClickCount] = useState(0);

  function inc() {
    setClickCount(clickCount + 1);
  }

  return (
    <div>
      <h2>Uploader of {title}</h2>
      <p>Upload count {clickCount}</p>
      <button onClick={inc}>upload ({fileType})</button>
    </div>
  );
}
