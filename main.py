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

def delete_student(name):
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
        print(f"🗑️ Deleted student: {name}")
    else:
        print("❌ Student not found.")

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
        print("\n📘 MENU\n1. Add Student\n2. Show Report\n3. Delete Student\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            marks = list(map(int, input("Enter marks separated by space: ").split()))
            add_student(name, marks)
        elif choice == '2':
            show_report()
        elif choice == '3':
            name = input("Enter student name to delete: ")
            delete_student(name)
        elif choice == '4':
            print("👋 Exiting... Peace out.")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
