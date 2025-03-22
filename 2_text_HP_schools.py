""""******* TEXT FILE ABOUT HARRY POTTER SHOOLS *******"""

# PROCESSING THE DATA from the file by creating a list of dictionaries
# Each dictionary is a school with its grades and each grade has its respective students.
# Pattern:
# [{"school": "school's 'name", "grade n":[[student a], [b], ...], "grade n+1": [[...], [...], ...]}]
# The length of a dictionary will be (number of grades + school).

with open("2_text_HP_schools.txt", "r") as sample_text:
    text = sample_text.read().splitlines()
    counter = 0
    school_positions = []
    text_chunks = []
    for line in text:
        if line.startswith("School ="):
            school_positions.append(counter)
        else:
            counter += 1
    # print(school_positions, len(school_positions))
    # print(text)
    for k in range(len(school_positions)):
        # print("k:", k, "school_positions[k]:", school_positions[k])
        # if k == len(school_positions):
        #     break
        if k == len(school_positions) - 1:
            text_chunks.append(text[school_positions[k] :])
        else:
            text_chunks.append(text[school_positions[k] : school_positions[k + 1]])

    # print(text_chunks)

    schools_list = []

    for school in text_chunks:
        test_dict = {}
        current_grade = 0
        in_grade = False

        students_num = []
        students_names = []
        students_grades = []

        for line in school:
            if not line:
                pass
            else:
                if line.startswith("School"):
                    school_name = line.split("=")[-1].strip()
                    test_dict["school"] = school_name

                if line.startswith("Grade"):
                    grade = line.split("=")[-1].strip()
                    test_dict[grade] = []

                if line[0].isdigit():
                    line = line.split(",")
                    student_num = int(line[0])

                    try:  # Check if the student's info (list) exists
                        test_dict[grade][student_num]
                    except IndexError:
                        test_dict[grade].append([line[0].strip()])

                    for i in test_dict[grade]:
                        # Check the existing lists and see if the current student
                        # number exists. If so, we add the new info (name then score)
                        if str(student_num) == i[0]:
                            test_dict[grade][student_num].append(line[-1].strip())
        schools_list.append((test_dict))

print("schools_list:")
print(schools_list)

# PROCESSING THE DATA in order to render a table
# First step: get the longest length of each column.
# Note \t = 8 spaces
# The only columns that need to be checked are "School"
# and "Name" as some names' lengths are likely to be
# greater than the length of the column's name (6 and 4)

# The table will look like this:
# School    Grade   Student number  Name    Score

maxlength_school = len("School")
maxlength_name = len("Name")

for school in schools_list:
    school_name = school["school"]
    if len(school_name) > maxlength_school:
        maxlength_school = len(school_name)

    for g in range(len(school) - 1):
        grade_students = school[str(g + 1)]
        for student in grade_students:
            student_name = student[1]
            if len(student_name) > maxlength_name:
                maxlength_name = len(student_name)

print("maxlength_school:", maxlength_school)
print("maxlength_name:", maxlength_name)


def render_for_terminal(maxlength_school):
    txt_filename = "2_text_HP_schools_result.txt"
    space_school_title = maxlength_school - len("School") + 4
    space_name_title = maxlength_name - len("Name") + 4
    end_to_grade = len("school") + space_school_title + len("Grade") - 1
    end_to_student_num = end_to_grade + 4 + len("Student number")
    end_to_name = end_to_student_num + space_name_title + len("Name")
    end_to_score = end_to_name + 4 + len("Score")

    row_titles = f'School{" "*space_school_title}Grade{" "*4}Student number{" "*space_name_title}Name{" "*4}Score'
    print(row_titles)

    with open(txt_filename, "a") as output_file:
        output_file.write(f"{row_titles}\n")

    for school in schools_list:
        school_name = school["school"]
        line = school_name
        # print(school_name, end="")
        if len(school_name) > maxlength_school:
            maxlength_school = len(school_name)

        for g in range(len(school) - 1):  # Group of a given grade (g+1)
            space_grade = end_to_grade - len(school_name) if g == 0 else end_to_grade
            line += f'{" "*space_grade}{g + 1}'
            # print(f'{" "*space_grade}{g + 1}', end="")

            grade_students = school[str(g + 1)]

            for student in grade_students:
                student_number = student[0]
                student_name = student[1]
                student_score = student[2]

                space_student_num = (
                    end_to_student_num - end_to_grade - 1
                    if grade_students[0] == student
                    else end_to_student_num
                )
                space_student_name = (
                    end_to_name - end_to_student_num - (len(student_name))
                )
                space_student_score = end_to_score - end_to_name - len(student_score)

                line += f'{" "*space_student_num}{student_number}{" "*space_student_name}{student_name}{" "*space_student_score}{student_score}'
                # print(
                #     f'{" "*space_student_num}{student_number}{" "*space_student_name}{student_name}{" "*space_student_score}{student_score}'
                # )
                print(line)
                with open(txt_filename, "a") as output_file:
                    output_file.write(f"{line}\n")
                line = ""

            with open(txt_filename, "a") as output_file:
                output_file.write("\n")


def render_for_csv(maxlength_school):
    import csv

    csv_filename = "2_text_HP_schools_result.csv"

    with open(csv_filename, "w", newline="") as file:
        csv_file = csv.writer(file)
        title_row = ["School", "Grade", "Student number", "Name", "Score"]
        formatted_title_row = [f"{title:<30}" for title in title_row]
        # print(formatted_title_row)
        csv_file.writerow(formatted_title_row)

    for school in schools_list:
        school_first_line = True
        school_name = school["school"]
        line = school_name
        if len(school_name) > maxlength_school:
            maxlength_school = len(school_name)

        for g in range(len(school) - 1):  # Group of a given grade (g+1)
            grade_first_line = True
            grade_students = school[str(g + 1)]

            for student in grade_students:
                student_number = student[0]
                student_name = student[1]
                student_score = student[2]

                if not school_first_line:
                    school_name = ""
                grade = "" if not grade_first_line else g + 1

                line = [school_name, grade, student_number, student_name, student_score]
                school_first_line = False
                grade_first_line = False
                with open(csv_filename, "a", newline="") as file:
                    csv_file = csv.writer(file)
                    formatted_row = [f"{word:<30}" for word in line]
                    csv_file.writerow(formatted_row)


maxlength_school = 20
render_for_csv(maxlength_school)
render_for_terminal(maxlength_school)
