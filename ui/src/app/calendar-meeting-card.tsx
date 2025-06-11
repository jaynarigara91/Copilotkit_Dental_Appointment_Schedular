import React from "react";

interface CalendarMeetingCardProps {
  date: string;
  time: string;
  meetingName: string;
  attendees: string[];
}

export const CalendarMeetingCard: React.FC<CalendarMeetingCardProps> = ({
  date,
  time,
  meetingName,
  attendees,
}) => {
  const formattedDate = new Date(date).toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <h2 className="text-xl font-semibold mb-2 text-gray-800">{meetingName}</h2>
      <div className="flex items-center mb-4">
        <div className="mr-4">
          <p className="text-sm font-medium text-gray-500">Date</p>
          <p className="text-gray-800">{formattedDate}</p>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-500">Time</p>
          <p className="text-gray-800">{time}</p>
        </div>
      </div>
      {attendees.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-500 mb-1">Attendees</p>
          <ul className="space-y-1">
            {attendees.map((attendee, index) => (
              <li key={index} className="text-gray-800">
                • {attendee}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="mt-6 pt-4 border-t border-gray-200 flex justify-end">
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
          Add to Calendar
        </button>
      </div>
    </div>
  );
};