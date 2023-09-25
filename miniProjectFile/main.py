import tkinter as tk
import time
from datetime import datetime, date
from tkinter import messagebox, ttk

import csv
import re

import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode

# Create the main window
window = tk.Tk()
window.title('Attendance Management System for IT Department')
window.geometry('600x500+320+45')
window['background'] = 'lavender'

# Nested dictionary mapping options to related options
related_options = {
    "1st": ["1st", "2nd"],
    "2nd": ["3rd", "4th"],
    "3rd": ["5th", "6th"],
    "4th": ["7th", "8th"]
}

def on_select(event):
    selected_option = combo_box.get()

    # Get the related options for the selected option
    if selected_option in related_options:
        options = related_options[selected_option]
    else:
        options = []

    # Clear the previous related options and populate the related combo box
    combo_box1['values'] = options

year = tk.StringVar()
sem = tk.StringVar()
subject = tk.StringVar()


# Create the combo box for selecting options
label = tk.Label(window, text="Attendance Management System", bg="lavender", fg="black", font=("times new roman", 25))
label.place(x=90, y=10)

label1 = tk.Label(window, text="Year", bg="lavender", fg="black", font=("times new roman", 15))
label1.place(x=120, y=100)
combo_box = ttk.Combobox(window, textvariable=year, values=["1st", "2nd", "3rd", "4th"], state="readonly")
combo_box.bind("<<ComboboxSelected>>", on_select)
combo_box.place(x=270, y=100)

related_options1 = {
    "1st": ["EM-I", "Physics", "Graphics", "Communication Skills", "Energy and Environmental Engineering", "Basics civil and mechanical engineering"],
    "2nd": ["EM-II", "Chemistry", "Mechanics", "Computer programming in C", "Basics electrical and electronics engineering"],
    "3rd": ["EM-III", "Interpersonal Communication Skills", "Computer Architecture and Organization", "Object Oriented Programming in C++", "Data Structure and Applications"],
    "4th": ["Organization Behaviour", "Probability and Statistics", "Discrete Mathematics", "Design Analysis and Algorithms", "Digital Logic and Microprocessor", "Web Technology"],
    "5th": ["Software Engineering", "Computer Networks and Internetworking Protocols", "IT service management", "Network Management", "Data Visualization", "Virtual Reality", "Graph Theory", "Programming in Java", "Human Computer Interaction"],
    "6th": ["Operating System", "Database Management System", "Software testing", "Data Warehousing and Data Mining", "Compiler Design", "Enterprise Resource Planning", "Software Project Management", "Introduction to Data Science"],
    "7th": ["Cloud Computing and Storage Management", "Artificial Intelligence", "Pattern Recognition", "Soft Computing", "Electronic Payment System", "Natural Language Processing", "Machine Learning", "Real Time Systems", "Information Security", "Management Information Systems", "Distributed Computing"],
    "8th": ["Internet of Things", "Mobile Computing"]
}

def on_select1(event):
    selected_option1 = combo_box1.get()

    # Get the related options for the selected option
    if selected_option1 in related_options1:
        options = related_options1[selected_option1]
    else:
        options = []

    # Clear the previous related options and populate the related combo box
    combo_box2['values'] = options

# Create the combo box for displaying related options
label2 = tk.Label(window, text="Semester", bg="lavender", fg="black", font=("times new roman", 15))
label2.place(x=120, y=150)
combo_box1 = ttk.Combobox(window, textvariable=sem, state="readonly")
combo_box1.bind("<<ComboboxSelected>>", on_select1)
combo_box1.place(x=270, y=155)

label3 = tk.Label(window, text="Subject", bg="lavender", fg="black", font=("times new roman", 15))
label3.place(x=120, y=205)
combo_box2 = ttk.Combobox(window, textvariable=subject, state="readonly")
combo_box2.place(x=270, y=208)

def check():
    if year.get() and sem.get() and subject.get():
        selected_year = year.get()  # Get the selected year from the combo box
        selected_semester = sem.get()  # Get the selected semester from the combo box
        selected_subject = subject.get()  # Get the selected subject from the combo box

        # Store the year data in a variable or use it as needed
        # For example:
        print("Selected Year:", selected_year)
        print("Selected Semester:", selected_semester)
        print("Selected Subject:", selected_subject)

        window.destroy()
    else:
        messagebox.showwarning("Warning", "All Fields are Required !!")


button = tk.Button(window, text="Submit", bg="lavender", fg="black", font=("times new roman", 16), command=check)
button.place(x=250, y=300)

# Start the GUI event loop
window.mainloop()


'''Capturing'''
capture = cv2.VideoCapture(0)
names=[]
today=date.today()
d= today.strftime("%b-%d-%Y")
sub = subject.get()

fob=open(d + "_"+ sub +'.csv','w+')
fob.write("PR No. and Name \t\t")
fob.write("Year \t\t")
fob.write("Semester \t\t")
fob.write("Subject \t\t")
fob.write("In Time \t\t")


def enterData(z):
    if z in names:
        pass
    else:
        it = datetime.now()
        names.append(z)
        z = ''.join(str(z))
        intime = it.strftime("%H:%M:%S")
        fob.write(z + '\t' +year.get() + '\t' + sem.get() + '\t' + subject.get() +'\t' + intime + '\n')
    return names

print('Reading...')

def checkData(data):
    # data=str(data)
    if data in names:
        print('Already Present')
    else:
        print('\n' + str(len(names) + 1) + '\n' + 'present...')
        enterData(data)

while True:
    _, frame = capture.read()
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        checkData(obj.data)
        time.sleep(0.5)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded = pyzbar.decode(gray)

    for barcode in decoded:
        x, y, w, h = barcode.rect
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f'{barcode_data} ({barcode_type})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0),
                    2)

        # Process attendance data here
        print("QR Code Data:", barcode_data)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

fob.close()


# Read the CSV file and sort the data
attendance_data = []
with open(d + "_" + sub + '.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    headers = next(reader)
    attendance_data = sorted(reader, key=lambda x: int(re.sub(r'\D', '', x[0])))

# Write the sorted data back to the CSV file
with open(d + "_" + sub + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(headers)
    writer.writerows(attendance_data)

with open(d + "_" + sub + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["PR No. and Name \t", "Year\t","Semester\t", "Subject\t", "In Time\t"])
    writer.writerows(attendance_data)
