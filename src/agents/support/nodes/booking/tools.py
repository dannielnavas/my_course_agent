from langchain.tools import tool


@tool("book_appointment", description="Book a medical appointment for a given date, time, doctor and patient")
def book_appointment(date: str, time: str, doctor: str, patient: str) -> str:
    """Book a medical appointment"""
    return f"Appointment booked for {date} at {time} with {doctor} for {patient}"


@tool("get_appointment_availability", description="Get the availability of a medical appointment for a given date, time, doctor and patient")
def get_appointment_availability(date: str, time: str, doctor: str) -> str:
    """Get the availability of a medical appointment"""
    return f"""
    The availability slots for the {doctor} are:
    - Monday: 10:00 - 12:00
    - Tuesday: 10:00 - 12:00
    - Wednesday: 10:00 - 12:00
    - Thursday: 10:00 - 12:00
    - Friday: 10:00 - 12:00
    """


tools = [book_appointment, get_appointment_availability]
