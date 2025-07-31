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

def list_students():
    """Display all students for selection"""
    data = load_data()
    if not data:
        print("⚠️ No students found.")
        return None
    
    print("\n📋 STUDENTS LIST:")
    students = list(data.keys())
    for i, name in enumerate(students, 1):
        grades_count = len(data[name])
        avg = sum(data[name]) / len(data[name])
        print(f"{i}. {name} ({grades_count} grades, avg: {avg:.1f})")
    
    return students

def select_student():
    """Let user select a student from the list"""
    students = list_students()
    if not students:
        return None
    
    while True:
        try:
            choice = input(f"\nSelect student (1-{len(students)}) or enter name: ").strip()
            
            # Check if it's a number
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(students):
                    return students[index]
                else:
                    print(f"❌ Please enter a number between 1 and {len(students)}")
                    continue
            
            # Check if it's a name
            if choice in students:
                return choice
            
            # Fuzzy search
            matches = [s for s in students if choice.lower() in s.lower()]
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                print(f"❌ Multiple matches found: {', '.join(matches)}")
                continue
            else:
                print(f"❌ Student '{choice}' not found.")
                continue
                
        except ValueError:
            print("❌ Invalid input.")

def add_grades_to_student(student_name):
    """Add new grades to existing student"""
    data = load_data()
    current_grades = data[student_name]
    
    print(f"\n📊 Current grades for {student_name}: {current_grades}")
    print(f"📈 Current average: {sum(current_grades)/len(current_grades):.2f}")
    
    while True:
        new_grades_input = input("Enter new grades to add (space-separated): ")
        is_valid, new_grades, error_msg = validate_marks(new_grades_input)
        
        if not is_valid:
            print(f"❌ {error_msg}")
            continue
        
        # Add new grades to existing ones
        updated_grades = current_grades + new_grades
        data[student_name] = updated_grades
        save_data(data)
        
        new_avg = sum(updated_grades) / len(updated_grades)
        print(f"✅ Added {len(new_grades)} new grades to {student_name}")
        print(f"📊 Updated grades: {updated_grades}")
        print(f"📈 New average: {new_avg:.2f}")
        break

def update_specific_grade(student_name):
    """Update a specific grade by position"""
    data = load_data()
    current_grades = data[student_name]
    
    print(f"\n📊 Current grades for {student_name}:")
    for i, grade in enumerate(current_grades, 1):
        print(f"{i}. {grade}")
    
    while True:
        try:
            position = input(f"Which grade to update? (1-{len(current_grades)}): ").strip()
            position = int(position) - 1
            
            if not (0 <= position < len(current_grades)):
                print(f"❌ Please enter a number between 1 and {len(current_grades)}")
                continue
            
            old_grade = current_grades[position]
            print(f"Current grade at position {position + 1}: {old_grade}")
            
            while True:
                new_grade_input = input("Enter new grade (0-100): ")
                is_valid, new_grades, error_msg = validate_marks(new_grade_input)
                
                if not is_valid:
                    print(f"❌ {error_msg}")
                    continue
                
                if len(new_grades) != 1:
                    print("❌ Please enter exactly one grade.")
                    continue
                
                # Update the specific grade
                current_grades[position] = new_grades[0]
                data[student_name] = current_grades
                save_data(data)
                
                new_avg = sum(current_grades) / len(current_grades)
                print(f"✅ Updated grade from {old_grade} to {new_grades[0]}")
                print(f"📊 Updated grades: {current_grades}")
                print(f"📈 New average: {new_avg:.2f}")
                return
                
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def edit_student_name(old_name):
    """Edit student name"""
    data = load_data()
    
    print(f"Current name: {old_name}")
    
    while True:
        new_name = input("Enter new name: ").strip()
        
        is_valid, error_msg = validate_student_name(new_name)
        if not is_valid:
            print(f"❌ {error_msg}")
            continue
        
        if new_name == old_name:
            print("❌ New name is same as current name.")
            continue
        
        if new_name in data:
            print(f"❌ Student '{new_name}' already exists.")
            continue
        
        # Update the name
        data[new_name] = data[old_name]
        del data[old_name]
        save_data(data)
        
        print(f"✅ Student name changed from '{old_name}' to '{new_name}'")
        break

def edit_student():
    """Main edit student function"""
    print("\n🔧 EDIT STUDENT")
    
    student_name = select_student()
    if not student_name:
        return
    
    while True:
        data = load_data()
        current_grades = data[student_name]
        avg = sum(current_grades) / len(current_grades)
        
        print(f"\n👤 Selected: {student_name}")
        print(f"📊 Current grades: {current_grades}")
        print(f"📈 Average: {avg:.2f}")
        
        print("\n🔧 EDIT OPTIONS:")
        print("1. Add new grades")
        print("2. Update existing grade")
        print("3. Change student name")
        print("4. Back to main menu")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '1':
            add_grades_to_student(student_name)
        elif choice == '2':
            update_specific_grade(student_name)
        elif choice == '3':
            old_name = student_name
            edit_student_name(student_name)
            # Update student_name if it was changed
            data = load_data()
            if old_name not in data:
                # Name was changed, find the new name
                break
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")

def main():
    print("🎓 Welcome to Student Grade Tracker!")
    
    while True:
        print("\n📘 MENU\n1. Add Student\n2. Show Report\n3. Edit Student\n4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

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
            edit_student()
            
        elif choice == '4':
            print("👋 Exiting... Peace out.")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
