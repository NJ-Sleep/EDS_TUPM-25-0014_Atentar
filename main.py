# Loads main program file for the Comprog-Project
import functions

# =======================
# Main program execution
# =======================
while True:
     month = input("Enter month number (1-12) to filter data: ")
     if month.isdigit() and 1 <= int(month) <= 12:
         break
     else:
         print("Invalid input. Please enter a valid month number (1-12).")

functions.csv_data_chunk(int(month)) 
functions.clean_data()
functions.descriptive_statistics()
functions.distribution_analysis()
functions.correlation_analysis()
functions.comparative_analysis()

# Remove the functions module after execution to reduce memory usage
del functions

# ===========================================================================================================
# ALL FINAL OUTPUTS ARE SAVED IN THE 'outputs' FOLDER. PLEASE CHECK THE FOLDER FOR ALL GENERATED PNG FILES.
# ===========================================================================================================