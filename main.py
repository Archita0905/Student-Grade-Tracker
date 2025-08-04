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

def add_student():
    data = load_data()

    while True:
        name = input("Enter student name: ").strip()
        if not name:
            print("❌ Name cannot be empty. Please try again.")
            continue
        break

    if name in data:
        overwrite = input(f"⚠️ Student '{name}' already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("❌ Student not added.")
            return

    while True:
        try:
            marks_input = input("Enter marks separated by space: ").strip()
            if not marks_input:
                raise ValueError("Empty input")
            marks = list(map(int, marks_input.split()))
            break
        except ValueError:
            print("❌ Invalid marks input. Please enter integers separated by space.")

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

def main():
    while True:
        print("\n📘 MENU\n1. Add Student\n2. Show Report\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            show_report()
        elif choice == '3':
            print("👋 Exiting... Peace out.")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
