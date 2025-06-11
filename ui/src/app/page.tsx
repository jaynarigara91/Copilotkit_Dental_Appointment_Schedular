"use client";
import {useCopilotChatSuggestions, CopilotSidebar, UserMessageProps, HeaderProps, useChatContext, MessagesProps, AssistantMessageProps } from "@copilotkit/react-ui";
import { useCopilotAction } from "@copilotkit/react-core";
import { Calendar } from 'lucide-react';
import { BookOpenIcon } from "@heroicons/react/24/outline";
import { Markdown } from "@copilotkit/react-ui";
import { SparklesIcon } from "@heroicons/react/24/outline";
import "@copilotkit/react-ui/styles.css";


// Header
function Header({}: HeaderProps) {
  const { setOpen, icons, labels } = useChatContext();
 
  return (
    <div className="flex justify-between items-center p-4 bg-blue-500 text-white">
      <div className="w-24">
        <a href="/">
          <BookOpenIcon className="w-6 h-6" />
        </a>
      </div>
      <div className="text-lg">{labels.title}</div>
      <div className="w-24 flex justify-end">
        <button onClick={() => setOpen(false)} aria-label="Close">
          {icons.headerCloseIcon}
        </button>
      </div>
    </div>
  );
};

// user message

const CustomUserMessage = (props: UserMessageProps) => {
  const wrapperStyles = "flex items-center gap-2 justify-end mb-4";
  const messageStyles = "bg-blue-500 text-white py-2 px-4 rounded-xl break-words flex-shrink-0 max-w-[80%]";
  const avatarStyles = "bg-blue-500 shadow-sm min-h-10 min-w-10 rounded-full text-white flex items-center justify-center";
 
  return (
    <div className={wrapperStyles}>
      <div className={messageStyles}>{props.message}</div>
      {/* <div className={avatarStyles}>TS</div> */}
    </div>
  );
};


// assistant message

// const CustomAssistantMessage = (props: AssistantMessageProps) => {
//   const { icons } = useChatContext();
//   const { message, isLoading, subComponent } = props;
 
//   const avatarStyles = "bg-zinc-400 border-zinc-500 shadow-lg min-h-10 min-w-10 rounded-full text-white flex items-center justify-center";
//   const messageStyles = "px-4 rounded-xl pt-2";
 
//   const avatar = <div className={avatarStyles}><SparklesIcon className="h-6 w-6" /></div>
 
//   return (
//     <div className="py-2">
//       <div className="flex items-start">
//         {!subComponent && avatar}
//         <div className={messageStyles}>
//           {message && <Markdown content={message || ""} /> }
//           {isLoading && icons.spinnerIcon}
//         </div>
//       </div>
//       <div className="my-2">{subComponent}</div>
//     </div>
//   );
// };
 





//     pnpm install lucide-react
export default function YourApp() {
  return (
    <>
      <MainContent />
      <CopilotSidebar Header={Header} UserMessage={CustomUserMessage} 
        instructions={`
          Help users schedule meetings. When they request to schedule a meeting:
          1. Ask for any missing details (attendee, date, time)
          2. Use CREATE_CALENDAR_EVENT to show the meeting card
          3. Confirm with the user that it looks correct`}
        defaultOpen={true}
        labels={{
          title: "Darshan Clinic",
          initial: "Hello! I'm Smilo from the Dental Clinic",
        }}
      />
    </>
  );
}

function MainContent() {
  
    useCopilotChatSuggestions(
    {
      instructions: "Suggest the most relevant next actions.",
      minSuggestions: 4,
      maxSuggestions: 5,
    },
  );

  useCopilotAction({
    name: "CREATE_CALENDAR_EVENT",
    description: "Displays calendar meeting information",
    parameters: [
      {
        name: "summary",
        type: "string",
        description: "Title/name of the meeting",
        required: true,
      },
      {
        name: "date",
        type: "string",
        description: "Start time (e.g., 'September 28th 9am') — will be converted to 'YYYY-MM-DD HH:MM:SS' format internally",
        required: true,
      },
      {
        name: "time",
        type: "string",
        description: "End time (e.g., 'September 28th 10am') — will be converted to 'YYYY-MM-DD HH:MM:SS' format internally",
        required: true,
      },
      {
        name: "description", 
        type: "string",
        description: "Display description in string with additional",
        required: true,
      }
    ],

    // ✅ Added missing handler
    handler: async ({ date, time, summary, description }) => {
      return {
        summary: summary || "Team Member",
        date,
        time,
        description,
        calendarLink: "hs://calendar.example.com/event/12345",
        eventId: "event-12345",
      };
    },

    render: ({ status, result }) => {
      if (status === "executing") {
        return <p className="text-blue-600">📅 Scheduling meeting...</p>;
      }

      if (status === "complete" && result) {
        const { date, time,description, summary, calendarLink, eventId } = result;
        return (
              <div className="meeting-card bg-purple-100 rounded-2xl shadow-lg p-4 max-w-md mx-auto border border-purple-200">
               
                {/* Date Section */}
                <div className="meeting-card-header flex items-center gap-4 mb-2">
                  <div className="meeting-card-icon bg-purple-200 p-3 rounded-xl">
                    <Calendar className="w-8 h-8 text-purple-600" />
                  </div>
                  <h2 className="meeting-card-date text-2xl font-semibold text-gray-800">{date}</h2>
                </div>

                {/* Title */}
                <h1 className="meeting-card-title text-2xl font-bold text-gray-900 mb-2 leading-tight">
                  {summary}
                </h1>

                {/* Time */}
                <div className="meeting-card-time-section mb-1">
                  <span className="meeting-card-time-label text-xl text-gray-600 font-medium">Time: </span>
                  <span className="meeting-card-time-value text-xl text-gray-800 font-semibold">{time}</span>
                </div>

                {/* Description */}
                <p className="meeting-card-description text-lg text-gray-600 leading-relaxed">
                  {description}
                </p>
              </div>
        );
      }

      return <p className="text-red-500">⚠️ Failed to schedule meeting.</p>;
    },
  });



  return null; // still OK if you're only using hooks here
}




// // import { Calendar } from 'lucide-react';

// interface MeetingCardProps {
//   date: string;
//   title: string;
//   time: string;
//   description: string;
// }

// const MeetingCard = ({ date, title, time, description }: MeetingCardProps) => {
//   return (
//     <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md mx-auto border border-gray-100">
//       {/* Date Section */}
//       <div className="flex items-center gap-4 mb-6">
//         <div className="bg-blue-100 p-3 rounded-xl">
//           <Calendar className="w-8 h-8 text-blue-600" />
//         </div>
//         <h2 className="text-2xl font-semibold text-gray-800">{date}</h2>
//       </div>

//       {/* Title */}
//       <h1 className="text-3xl font-bold text-gray-900 mb-6 leading-tight">
//         {title}
//       </h1>

//       {/* Time */}
//       <div className="mb-6">
//         <span className="text-xl text-gray-600 font-medium">Time: </span>
//         <span className="text-xl text-gray-800 font-semibold">{time}</span>
//       </div>

//       {/* Description */}
//       <p className="text-lg text-gray-600 leading-relaxed">
//         {description}
//       </p>
//     </div>
//   );
// };

// export default MeetingCard;