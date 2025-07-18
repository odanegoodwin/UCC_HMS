





#Importing needed modules. 
import random  #For ID generation
import datetime #For Time/Date formatting

#Defining reusable varables
company_name = "UCC Hospital"
company_contact_number = "(876) 906-3000"
company_address = "17 Worthington Ave, Kingston"
consultation_fee = 3000





# Step 1. Creating the Person CLASS (Parent Class)
# Generic person with attributes: Name, age, gender

class Person:
    def __init__(self,name, age, gender):  
        self.name = name
        self.age = age
        self.gender = gender
        
        
    def display_info(self):
        print (f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")



# Step 2. Create Patient CLASS. (sub class of Person class)
# Adds patient_id & appointment_list

class Patient (Person):
    
    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)
        self.patient_id = generate_id ("PT")
        self.appointment_list = []
        
    def book_appointment (self, appointment):
        self.appointment_list.append (appointment)
        
    def view_profile (self):
        print("\n-----------------------------")
        print("***** Patient Profile *****")
        self.display_info()
        print (f"Patient ID: {self.patient_id}")
        if self.appointment_list:
            for appt in self.appointment_list:
                print(f"Appointment with Dr. {appt.doctor.name} on {appt.date} at {appt.time}\n")
                print("-------------------------------------\n")
        else: 
                print("No Appointments On File")
                print("-----------------------------\n")
                
                    
                    
        
# Step 3. Create Doctor CLASS. (sub-class of Person class)
# Adds doctoer_id, specialty and schedule.

class Doctor (Person):  
    
    def __init__(self, name, age, gender, specialty):
        super().__init__(name, age, gender)
        self.doctor_id = generate_id ("DR")
        self.specialty = specialty
        self.schedule = []
        
    def is_available(self, date, time):
        return is_time_available (self.schedule, date, time)
    
    
    def view_schedule (self):
        print (f"Schedule for Dr. {self.name}")
        if self.schedule:
            for date, time in self.schedule:
                print (f"{date} at {time}")
        else:
            print (f"No appointments scheduled for Dr. {self.name}.")
        


#Step 4. Create Appointment CLASS. (standalone class)
#Appointment between patient and doctor
        
class Appointment:
    def __init__(self, patient, doctor, date, time):
        self.appointment_id = generate_id("APT")
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Your Appointment is confirmed"
        
    def confirm (self):
        print("\n------------------------")
        print("Appointment Confirmed!")
        print(f"Appointment ID is: {self.appointment_id}")
        print("--------------------------\n")
        
    def cancel (self):
        self.status = "Your Appointment is cancelled"
        print("\n-------------------------------------")
        print (f"Appointment {self.appointment_id} has been cancelled")
        print("-------------------------------------\n")
        


# Step 5. Create Hospital System class. 
# Manages all functionality between patient, doctor and appointment

class Hospital_System:
    def __init__(self):
        self.patient = {}
        self.doctor = {}
        self.appointment = {}
        
    #Function to Register a new Patient
    def add_patient (self, name, age, gender):
        patient = Patient(name, age, gender.capitalize())
        self.patient[patient.patient_id] = patient
        print("\n---------------------")
        print(f"Registration Complete")
        print(f"Patient ID is: {patient.patient_id}")
        print("-----------------------")
        
    # Function to Register a new Doctor
    
    def add_doctor(self, name, age, gender, specialty):
        doctor = Doctor(name, age, gender.capitalize(), specialty)
        self.doctor[doctor.doctor_id] = doctor 
        print("\n------------------------")
        print(f"Registration Complete")
        print(f"Doctor ID is: {doctor.doctor_id}")
        print("--------------------------")
        
        
    
    #Function to Book An Appointment
    def book_appointment (self, patient_id, doctor_id, date, time):
        patient = self.patient.get(patient_id)
        doctor = self.doctor.get(doctor_id)
        
        if not patient or not doctor:
            print ("Invalid entry, Patient ID or Doctor ID incorrect")
            return
        if not doctor.is_available(date, time): 
            print ("Doctor is already booked for this time. Please retry again")
            return 
        
        appointment = Appointment(patient, doctor, date, time)
        self.appointment[appointment.appointment_id] = appointment
        patient.book_appointment (appointment)
        doctor.schedule.append ((date, time))
            
        appointment.confirm()
    
    
    #Function to cancel an appointment
    def cancel_appointment (self, appointment_id):
        appointment = self.appointment.get(appointment_id)
        if appointment:
            appointment.cancel()
            
            # Deleteing the appointment from the doctor's schedule
            if (appointment.date, appointment.time) in appointment.doctor.schedule:
                appointment.doctor.schedule.remove((appointment.date, appointment.time))
        
            # Deleteing the appointment from patient's appointment list           
            if appointment in appointment.patient.appointment_list:
                appointment.patient.appointment_list.remove(appointment)
        
            # Deleting appointment from system
            del self.appointment[appointment_id]
            
        else:
            print("\n-------------------------------------")
            print("*** No Appointment found with this ID")
            print("-------------------------------------\n")
        
        
        
        
    #Function to Generate a bill
    def generate_bill (self, appointment_id):
        appointment = self.appointment.get(appointment_id)
        if not appointment:
            print("Appointment not found.")
            return
            
        print(f"\n=========== {company_name} ===========")
        print (f"Contact number: Tel: {company_contact_number} ")
        print (f"Address: {company_address} ")
        print ("--------------------------------")
        print(f"Patient: {appointment.patient.name}")
        print(f"Doctor: Dr. {appointment.doctor.name}")
        print(f"Date & Time: {appointment.date}, {appointment.time}")
        print("--------------------------------")
        
        print (f"Consultation fee: JMD ${consultation_fee}")

        try: 
            extra_fee = float(input("Please enter addional charges (tests/meds): JMD $"))
            if extra_fee < 0:
                    raise ValueError
        except ValueError:
            print ("Invalid Input. Fees cannot be negative or 0")
            extra_fee = 0
                
        total = consultation_fee + extra_fee
        print (f"TOTAL BILL: JMD $ {total}")
        print ("===================================\n")
        
        

# Function that generates random ID using the prefix and number 1000-9999
def generate_id (prefix):
    return prefix + str(random.randint(1000,9999))


# Function that prevents double booking. 
def is_time_available (schedule, date, time):
    return (date, time) not in schedule        
        
        
        
        
        
        
# Step 6. Main Program Loop


def main (): #Menu Function
    hospital = Hospital_System() #Used to connect meny with main functons
    
    while True: #Displaying Menu options
        print ("\n==== UCC Hospital Managment System ====")
        print ("               Menu                    ")
        print ("Select option from menu below\n")
        print ("1. Register New Patient")
        print ("2. Register New Doctor")
        print ("3. Book an Appointment")
        print ("4. Cancel Appointment")
        print ("5. View Doctor Schedule")
        print ("6. View Patient Profile")
        print ("7. Generate Patient Bill")
        print ("0. Exit System")
        print ("=====================================\n")
        
        
        #Collecting User input to correspond to above menu. 
        option = input("Choose an option: ").strip()
     
     
 #Option 1: Register Patient
    
        if option == "1":
            while True:   #Error Handling for Patient name input ensureing that field is not left blank or contains any numbers
                name = input("Patient Name: ").strip() 
                if any (char.isdigit() for char in name) or name == "":
                    print ("\n**** Invalid entry. Field contains digits or left blank")
                else:
                    break  
                        
            while True:                             
                age = input("Patient Age: ").strip()
                if age == "":       # Ensuring field is not left blank
                    print ("\n**** Blank entry. Please enter valid age.")
                    continue
                try:
                    age = int(age)              
                    if age <= 0:    # Ensuring age is greater than zero
                        print ("\n**** Invalid entry. Please enter age greater than 0")
                    else:
                        break
                except ValueError:
                    print("\n**** Invalid entry. Age must be a number")
                           
            while True:  # Ensuring that the gender input can only be 'M' or 'F', or not left blank
                gender = input("Patient Gender (M/F): ").strip()
                if gender.lower() not in ['m', 'f']:
                  print ("\n**** Invalid entry. Please enter 'M' or 'F'.")
                else:
                    break 
                
            hospital.add_patient(name, age, gender)
            
            
    #Option 2: Register Doctor
        
        elif option == "2":
            while True:     
                name = input ("Doctor Name: ").strip().upper()
                if any (char.isdigit() for char in name) or name == "":
                    print ("\n**** Invalid entry. Field contains digits or left blank")
                else:
                    break
                 
            while True:                             
                age = input("Doctor Age: ").strip()
                if age == "":       # Ensuring field is not left blank
                    print ("\n**** Blank entry. Please enter valid age.")
                    continue
                try:
                    age = int(age)              
                    if age <= 0:     # Ensuring age is greater than zero
                        print ("\n**** Invalid entry. Please enter age greater than 0")
                    else:
                        break
                except ValueError:
                    print("\n**** Invalid entry. Age must be a number")
            while True:        # Ensuring that the gender input can only be 'M' or 'F', or not left blank
                gender = input("Doctor Gender (M/F): ").strip()
                if gender.lower() not in ['m', 'f']:
                  print ("\n**** Invalid entry. Please enter 'M' or 'F'.")
                else:
                    break 
                
            specialty = input ("Doctor Specialty: ").strip().upper()
            hospital.add_doctor(name, age, gender, specialty)
            
        
    #Option 3: Book an Appointment
        elif option == "3":
            pid = input ("Enter Patient ID: ").strip().upper()
            did = input ("Enter Doctor ID: ").strip().upper()
            
            while True:
                date = input ("Date (yyyy-mm-dd): ").strip()
                time = input ("Time (HH:MM): ").strip()
                try:            # Ensuring date and time input is in correct format and not in the past.
                    appt_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                    
                    if appt_datetime < datetime.datetime.now(): # Comparing inpur to current time
                        print ("\n**** Invalid entry. Appointment cannot be in the past.")
                        continue
                    break
                except ValueError:
                    print("\n**** Invalid format. Please use yyyy-mm-dd and HH:MM.")
                
            
            hospital.book_appointment(pid, did, date, time)
            

        
    #Option 4: Cancel an Appointment
        elif option == "4":
            appointment_id = input("Enter Appointment ID: ").strip().upper()
            hospital.cancel_appointment(appointment_id)
         
         
         
    #Option 5: View Doctor Schedule
        elif option == "5":
            did = input ("Enter Doctor ID: ").strip().upper()
            doctor = hospital.doctor.get(did)
            if doctor:
                doctor.view_schedule()
            else:
                print ("\n---------------------------")
                print ("No Doctor found with this ID")
                print ("---------------------------\n")
          
          
          
     #Option 6: View Patient Profile
        elif option == "6":
            pid = input ("Enter Patient ID: ").strip().upper()
            patient = hospital.patient.get(pid)
            if patient:
                patient.view_profile()
            else:
                print ("\n----------------------------")
                print ("No patient found with this ID")
                print ("----------------------------\n")
           
        
           
     #Option 7: Genrate Patient Bill
        elif option == "7":
            appointment_id = input("Enter Appointment ID: ").strip().upper()
            hospital.generate_bill(appointment_id)
            
            
     #Option 8: Exit
        elif option == "0":
            print ("\n**** Exiting system. Goodbye ****")
            break
     
        else:
            print("\n **** Invalid Option, Please select a valid number from 0 to 7.")
        
        
            
 # Ensures the main() function runs only when this program is ran direclty and not when imported
if __name__ == "__main__":
    main()
    


