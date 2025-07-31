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

def show_topper():
    data = load_data()
    if not data:
        print("⚠️ No data found.")
        return

    topper_name = None
    highest_avg = -1

    for name, marks in data.items():
        avg = sum(marks) / len(marks)
        if avg > highest_avg:
            highest_avg = avg
            topper_name = name

    print(f"\n🏆 Topper: {topper_name} with Avg: {highest_avg:.2f}")



def show_report():
    data = load_data()
    if not data:
        print("⚠️ No data found.")
        return

    print("\n📊 Student Report")
    print("-" * 49)
    print(f"{'Name':<10} | {'Avg Marks':^10} | {'Highest':^7} | {'Lowest':^6}")
    print("-" * 49)

    total_students = 0
    total_marks_sum = 0
    total_marks_count = 0

    for name, marks in data.items():
        avg = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)

        print(f"{name:<10} | {avg:^10.2f} | {highest:^7} | {lowest:^6}")

        total_students += 1
        total_marks_sum += sum(marks)
        total_marks_count += len(marks)

    print("-" * 49)
    overall_avg = total_marks_sum / total_marks_count if total_marks_count else 0
    print(f"👥 Total Students: {total_students}")
    print(f"📈 Overall Class Avg: {overall_avg:.2f}")

def main():
    while True:
        print("\n📘 MENU\n1. Add Student\n2. Show Report\n3. Show Topper\n4. Delete Student\n5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            marks = list(map(int, input("Enter marks separated by space: ").split()))
            add_student(name, marks)
        elif choice == '2':
            show_report()
       
        elif choice == '3':
            show_topper()

        elif choice == '4':
            name = input("Enter student name to delete: ")
            delete_student(name)

        elif choice == '5':
            print("👋 Exiting... Peace out.")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
