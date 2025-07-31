import json

DATA_FILE = 'students.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error: Corrupted data file. Starting with empty data.")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def validate_student_name(name):
    """Validate student name input"""
    if not name or not name.strip():
        return False, "Student name cannot be empty."
    if len(name.strip()) < 2:
        return False, "Student name must be at least 2 characters long."
    return True, ""

def validate_marks(marks_input):
    """Validate and parse marks input"""
    if not marks_input or not marks_input.strip():
        return False, [], "Marks cannot be empty."
    
    try:
        marks = list(map(float, marks_input.split()))
        
        if not marks:
            return False, [], "Please enter at least one mark."
        
        # Check if all marks are in valid range (0-100)
        for mark in marks:
            if not (0 <= mark <= 100):
                return False, [], f"Mark {mark} is out of range. Please enter marks between 0 and 100."
        
        # Convert to integers if they're whole numbers
        marks = [int(mark) if mark.is_integer() else mark for mark in marks]
        return True, marks, ""
        
    except ValueError:
        return False, [], "Invalid input. Please enter numeric values only (e.g., '85 90 88')."

def add_student(name, marks):
    data = load_data()
    
    # Check if student already exists
    if name in data:
        overwrite = input(f"⚠️ Student '{name}' already exists. Overwrite? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("❌ Operation cancelled.")
            return
    
    data[name] = marks
    save_data(data)
    print(f"✅ Added student: {name}")

def show_report():
    data = load_data()
    if not data:
        print("⚠️ No data found.")
        return

    print("\n" + "="*60)
    print(f"{'STUDENT NAME':<20} {'AVG':<8} {'HIGH':<8} {'LOW':<8}")
    print("="*60)
    
    for name, marks in data.items():
        avg = sum(marks) / len(marks)
        print(f"{name:<20} {avg:<8.2f} {max(marks):<8} {min(marks):<8}")
    
    print("="*60)

def get_student_input():
    """Get and validate student input with error handling"""
    while True:
        name = input("Enter student name: ").strip()
        
        # Validate name
        is_valid, error_msg = validate_student_name(name)
        if not is_valid:
            print(f"❌ {error_msg}")
            continue
        
        break
    
    while True:
        marks_input = input("Enter marks separated by space (0-100): ")
        
        # Validate marks
        is_valid, marks, error_msg = validate_marks(marks_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            continue
        
        break
    
    return name, marks

def main():
    print("🎓 Welcome to Student Grade Tracker!")
    
    while True:
        print("\n📘 MENU\n1. Add Student\n2. Show Report\n3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            try:
                name, marks = get_student_input()
                add_student(name, marks)
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled.")
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                
        elif choice == '2':
            show_report()
            
        elif choice == '3':
            print("👋 Exiting... Peace out.")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
