# CoWinAlert
Periodically pings CoWin portal to check for Covid vaccination appointments in a selected city.
Thanks to https://github.com/vishalkhopkar/cowin_vaccination_ping

# Requirements
Working installation of python 
Requires the following python packages :
1. playsound
2. requests
3. urllib3

Can be installed using the following command :
pip install -r requirements.txt

# Instructions
1. Alter variables in main.py :
	1. DISTRICT_CODES - to include all the district codes for which you would like to be notified
	2. DISTRICT_LABELS - update this map to have appropriate labels for each of the district codes 
	3. SLEEP_TIME - make appropriate changes to alter the frequency at which the CoWin portal will be pinged
2. Run main.py 
3. Enter the name of the city 
4. The program will raise an alarm if it finds any slots



