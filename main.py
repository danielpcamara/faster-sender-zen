import loadfiles
from models import CreateBase, update_clean

###################### MAIN VARIABLES ####################################
root_dir = r"C:\Temp XML"
main_url = "escritorio_contabil"
token = "119c963a17e4bca679a247ca0b11af93"
skip = 1 #use 1 if you dont need to skip folders (in second runs)
simult_quant = 2000
sleep_time = 0
retry_status = 500

#Create the Database file
CreateBase()

#Feed the Database with all XML files in a given folder and save some propeirties of the XML
loadfiles.load_to_database(root_dir, skip)

#Send a request to all file in the databae that have not been sent yet
loadfiles.send_valid_new(main_url, token, simult_quant, sleep_time)

#Retry some times error 500

for _ in range(3):
    update_clean(retry_status)
    loadfiles.send_valid_new(main_url, token, simult_quant, sleep_time)