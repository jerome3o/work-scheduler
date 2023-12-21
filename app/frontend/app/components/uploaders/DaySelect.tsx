export default function DaySelect({
  options,
  value,
  setValue,
}: {
  options: string[];
  value: string;
  setValue: (value: string) => void;
}) {
  return (
    <div className="day-select">
      <p>Day:</p>
      <select
        value={value}
        onChange={() => (e: any) => setValue(e.target.value)}
      >
        {options.map((day, i) => {
          return <option key={i}>{day}</option>;
        })}
      </select>
    </div>
  );
}
