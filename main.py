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

def main():
    while True:
        print("\n MENU\n1. Add Student\n2. Show Report\n3. Edit Student\n4. Exit")
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
            print("👋 Exiting... Peace out.")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
