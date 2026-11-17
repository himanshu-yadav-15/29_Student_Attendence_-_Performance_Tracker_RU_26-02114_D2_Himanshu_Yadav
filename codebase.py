import csv

def load_and_clean_data(filename="students.csv"):
    students = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=1):
                name = row['Name'].strip()
                
                # Validate numbers
                try:
                    held = int(row['Classes_Held'])
                except ValueError:
                    print(f"Row {row_num} skipped: invalid Classes_Held '{row['Classes_Held']}'.")
                    continue

                try:
                    attended = int(row['Classes_Attended'])
                except ValueError:
                    print(f"Row {row_num} skipped: invalid Classes_Attended '{row['Classes_Attended']}'.")
                    continue

                try:
                    marks = int(row['Marks'])
                except ValueError:
                    print(f"Row {row_num} skipped: invalid Marks '{row['Marks']}'.")
                    continue

                # Validate logical limits
                if held <= 0 or attended < 0 or marks < 0 or marks > 100:
                    print(f"Row {row_num} skipped: values out of range.")
                    continue
                if attended > held:
                    print(f"Row {row_num} skipped: attended ({attended}) cannot exceed held ({held}).")
                    continue

                # Calculations
                attendance_pct = (attended / held) * 100

                # Determine status
                if attendance_pct < 75 and marks < 40:
                    status = "At Risk (attendance below 75% and marks below 40)"
                elif attendance_pct < 75:
                    status = "At Risk (attendance below 75%)"
                elif marks < 40:
                    status = "At Risk (marks below 40)"
                else:
                    status = "OK"

                # Store student record as a Dictionary
                students.append({
                    'Name': name,
                    'Held': held,
                    'Attended': attended,
                    'Marks': marks,
                    'Attendance_%': attendance_pct,
                    'Status': status
                })
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
    return students

def show_report(students):
    for s in students:
        print(f"{s['Name']}: {s['Attendance_%']:.2f}% | Marks {s['Marks']} | {s['Status']}")

def show_summary_and_charts(students):
    total_att = sum(s['Attendance_%'] for s in students)
    total_marks = sum(s['Marks'] for s in students)
    avg_att = total_att / len(students)
    avg_marks = total_marks / len(students)

    # Filter At Risk students
    at_risk = [s['Name'] for s in students if s['Attendance_%'] < 75 or s['Marks'] < 40]

    print(f"Average attendance: {avg_att:.2f}% | Average marks: {avg_marks:.2f}")
    if at_risk:
        print(f"At Risk students: {len(at_risk)} ({', '.join(at_risk)})")
    else:
        print("At Risk students: 0")

    # Simple Console Bar Charts (Visualization)
    print("\n--- Attendance % Bar Chart ---")
    for s in students:
        bar = "█" * int(s['Attendance_%'] // 5)
        print(f"{s['Name']:<10} | {bar} {s['Attendance_%']:.1f}%")

    print("\n--- Marks Bar Chart (out of 100) ---")
    for s in students:
        bar = "█" * int(s['Marks'] // 5)
        print(f"{s['Name']:<10} | {bar} {s['Marks']}")

def main():
    students = load_and_clean_data("students.csv")

    if not students:
        print("No valid data to analyse.")
        return

    print("\n1. Report")
    print("2. Summary and charts")
    choice = input("Enter menu option (1 or 2): ").strip()
    print()

    if choice == '1':
        show_report(students)
    elif choice == '2':
        show_summary_and_charts(students)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()