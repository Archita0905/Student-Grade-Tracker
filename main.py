import json

DATA_FILE = 'students.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_student(name, marks):
    data = load_data()
    data[name] = marks
    save_data(data)
    print(f"✅ Added student: {name}")

def show_report():
    data = load_data()
    if not data:
        print("⚠️ No data found.")
        return

    for name, marks in data.items():
        avg = sum(marks) / len(marks)
        print(f"{name}: 📊 Avg: {avg:.2f} | 🔼 High: {max(marks)} | 🔽 Low: {min(marks)}")

def edit_student():
    data = load_data()
    name = input("Enter the name of the student to edit: ")

    if name not in data:
        print("Student not found.")
        return

    print("\n Edit Menu\n1. Add Grades\n2. Update Specific Grade\n3. Edit Name")
    option = input("Choose an option: ")

    if option == '1':
        new_grades = list(map(int, input("Enter new grades to add (space-separated): ").split()))
        data[name].extend(new_grades)
        print(f"Added {len(new_grades)} grades to {name}.")
    elif option == '2':
        print(f"Current grades for {name}: {data[name]}")
        index = int(input("Enter index of grade to update (starting from 0): "))
        if 0 <= index < len(data[name]):
            new_value = int(input("Enter new grade value: "))
            data[name][index] = new_value
            print(f"Grade at index {index} updated")
        else:
            print("Invalid index")
    elif option == '3':
        new_name = input("Enter new name: ")
        if new_name in data:
            print("A student already exists")
        else:
            data[new_name] = data.pop(name)
            print(f"Renamed {name} to {new_name}.")
    else:
        print("Invalid option.")
        return

    save_data(data)

import csv

def export_report():
    data = load_data()
    if not data:
        print("No data to export.")
        return

    with open("student_report.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Average", "Highest", "Lowest", "All Marks"])

        for name, marks in data.items():
            avg = sum(marks) / len(marks)
            writer.writerow([name, f"{avg:.2f}", max(marks), min(marks), ', '.join(map(str, marks))])

    print("Report exported to 'student_report.csv'")

def import_data():
    print("\nImport Options:\n1. JSON File\n2. CSV File")
    choice = input("Choose file type to import: ")

    if choice == '1':
        filename = input("Enter JSON file name: ")
        try:
            with open(filename, 'r') as file:
                new_data = json.load(file)
        except Exception as e:
            print(f"Failed to load JSON: {e}")
            return
    elif choice == '2':
        filename = input("Enter CSV file name: ")
        new_data = {}
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) < 2:
                        continue
                    name = row[0]
                    try:
                        marks = list(map(int, row[1:]))
                        new_data[name] = marks
                    except ValueError:
                        print(f"Invalid marks for {name}, skipping.")
        except Exception as e:
            print(f"Failed to load CSV: {e}")
            return
    else:
        print("Invalid choice.")
        return

    data = load_data()
    data.update(new_data)
    save_data(data)
    print(f"Imported {len(new_data)} student(s) from {filename}.")

def main():
    while True:
        print("\n MENU\n1. Add Student\n2. Show Report\n3. Edit Student\n4. Export to CSV\n5. Import Data\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            marks = list(map(int, input("Enter marks separated by space: ").split()))
            add_student(name, marks)
        elif choice == '2':
            show_report()
        elif choice == '3':
            edit_student()
        elif choice == '4':
            export_report()
        elif choice == '5':
            import_data()
        elif choice == '6':
            print("👋 Exiting... Peace out.")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
