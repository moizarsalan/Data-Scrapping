import pdfplumber
import pandas as pd
import re

def extract_timetable(pdf_path, output_csv):
    time_slots = [
        "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
        "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00",
        "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00",
        "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
    ]
    
    course_pattern = re.compile(r"([A-Za-z\s&-]+)\n([A-Za-z\s.]+)\n(C\d-[A-Za-z0-9]+)")
    structured_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    match = course_pattern.search(line)
                    if match:
                        course_name = match.group(1).strip()
                        instructor = match.group(2).strip()
                        room = match.group(3).strip()
                        
                        for slot in time_slots:
                            if slot in line:
                                structured_data.append([slot, course_name, instructor, room])
    
    df_timetable = pd.DataFrame(structured_data, columns=["Time", "Course", "Instructor", "Room"])
    df_timetable.to_csv(output_csv, index=False)
    print(f"Timetable extracted and saved to {output_csv}")

# Example usage
pdf_path = "D:\Github Repsitories\Data-Scrapping\Timetable Extraction"  # Change this to your PDF file
output_csv = "university_timetable.csv"
extract_timetable(pdf_path, output_csv)