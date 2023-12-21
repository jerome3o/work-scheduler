export default function DaySelect({ options }: { options: string[] }) {
  return (
    <div className="day-select">
      <p>Day:</p>
      <select>
        {options.map((day) => {
          return <option>{day}</option>;
        })}
      </select>
    </div>
  );
}
