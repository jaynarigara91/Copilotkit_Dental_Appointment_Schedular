# Darshan Clinic Dental Appointment Scheduler

A smart dental appointment scheduling system for Darshan Clinic that integrates with Google Calendar and provides a conversational interface for managing appointments.

## Screen Shot

![Screenshot 2025-06-11 072912](https://github.com/user-attachments/assets/2c6365e7-17f6-4fce-b035-8481568f4351)
![Screenshot 2025-06-11 072950](https://github.com/user-attachments/assets/b77e5568-8a38-4603-87cd-6561aa2c6f70)
![Screenshot 2025-06-11 073014](https://github.com/user-attachments/assets/7c71f96f-10d0-4ca1-a78d-80f23d7024ce)

## Features

- **Conversational AI Interface**: Chatbot interface for natural language appointment scheduling
- **Google Calendar Integration**: 
  - Create new appointments
  - Update existing appointments
  - Delete appointments
  - Search available slots
- **Interactive UI Elements**:
  - Appointment cards with visual display
  - Suggested questions for users
- **Memory Management**: Full conversation history and context retention
- **Fast AI Responses**: Powered by Groq API for high-speed LLM processing
- **Modern Tech Stack**: Built with:
  - CoPilot Kit for conversational AI
  - LangGraph for workflow management
  - React/Next.js for frontend

## Technology Stack

- **Frontend**: React/Next.js with CoPilot Kit
- **AI Services**: Groq API (LLM)
- **Backend**: Node.js/Express
- **Calendar Integration**: Google Calendar API
- **State Management**: Custom memory management for conversation history
- **UI Components**: Custom appointment cards with useCopilotKit Action

## Usage

Getting started with the dental appointment scheduler is simple and intuitive:

1. **Start a conversation** with the chatbot
2. Use **natural language commands** like:
   - "Schedule an appointment for next Tuesday at 2pm"
   - "Show me available slots this week"
   - "Cancel my 3pm appointment tomorrow"
   - "What appointments do I have this month?"
   - "Reschedule my cleaning to Friday afternoon"

**The system will automatically:**
- 📇 Display interactive appointment cards with all details
- 💡 Suggest relevant follow-up questions
- 🔄 Handle all calendar operations in the background
- 📲 Send confirmation notifications


## API Integration

The solution leverages powerful APIs:

- **Google Calendar API**
  - Full CRUD operations for appointments
  - Real-time availability checking
  - Timezone-aware scheduling

- **Groq API**
  - Ultra-fast LLM processing
  - Natural language understanding
  - Context-aware responses

- **CoPilot Kit Actions**
  - Secure calendar operations from chat
  - User confirmation flows
  - Error handling and validation

## Google Calendar
  - Note : you have to put credantials.json and token.json in credentials folder. in this repo token.json is removed you have to install yours


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/darshan-clinic-scheduler.git
   cd darshan-clinic-scheduler
   ```

   ```bash
   cd agent-py
   poetry lock
   poetry install
   poetry run demo
   ```

   ```bash
   cd ui
   pnpm i
   pnpm run dev
