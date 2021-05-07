import playsound
import requests
import urllib3 as urllib
import datetime
import time
urllib.disable_warnings(urllib.exceptions.InsecureRequestWarning)

BASE_API_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"
QUERY_TEMPLATE = "?district_id={}&date={}"
SLEEP_TIME = 30
DISTRICT_CODES = {
    "Bangalore" : [294, 265],
    "Mumbai" : [395, 392, 393, 394],
    "Pune": [363],
    "Delhi" : [141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142, 199, 188, 207, 202, 650, 651],
    "Hyderabad" : [581],
    "Chennai" : [571, 565, 557]
}
REGION_LABELS = list(DISTRICT_CODES.keys())
MIN_AGE = 18
DISTRICT_LABEL_MAP = {
    294 : 'BBMP',
    265 : 'Bengaluru Urban'
}
ALARM_AUDIO_FILE = 'alarm_sound.wav'

def process_output(json_output, region, dist_id):
    no_of_centres = 0
    output = json_output
    centres = output["centers"]
    districtName = DISTRICT_LABEL_MAP.get(dist_id, 'DistrictID#{}'.format(dist_id))
    for centre in centres:
        sessions = centre["sessions"]
        for session in sessions:
            min_age = session["min_age_limit"]
            avbl_cap = session["available_capacity"]
            if min_age == MIN_AGE and avbl_cap > 0:
                print("[I][{}] Found {} slots available on {} at : \n{}, \n{}, \n{}, {}, \nPin Code : {}, \nVaccine : {}, \nFee : {}".format(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"), avbl_cap, session["date"], centre["name"],
                                                                                                centre["address"], districtName, region, centre["pincode"], session['vaccine'], centre['fee_type']))
                no_of_centres += 1

    if no_of_centres == 0:
        print("[I][{}] Sorry, no centre available in {}, {}".format(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"), districtName, region))
    else:
        playsound.playsound(ALARM_AUDIO_FILE)

def get_input():

    disp_str = "[I] Enter city index :"
    for idx, regionName in enumerate(REGION_LABELS):
        disp_str += "\n{}. {}".format(idx + 1, regionName)
    disp_str += "\n------------ Region : "
    reg_name = input(disp_str)
    try:
        reg_name = reg_name.upper()
        if reg_name not in [x.upper() for x in REGION_LABELS]:
            raise Exception("Invalid")
        reg_id = [x.upper() for x in REGION_LABELS].index(reg_name)
        region = REGION_LABELS[reg_id]
        print("[I] Your region is {}\n".format(region))
        return reg_id
    except:
        print("[X] Invalid input exiting...")
        exit()

def poll_cowin_portal(reg_id):

    region = REGION_LABELS[reg_id]
    dist_ids = DISTRICT_CODES[region]
    while True:
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime('%d-%m-%Y')
        for dist_id in dist_ids:
            formatted_api_call = BASE_API_URL + QUERY_TEMPLATE.format(dist_id, formatted_date)
            # print("[I] Pinging API : {}".format(formatted_api_call))
            headers_dict = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            }
            response = requests.get(formatted_api_call, headers=headers_dict, verify=False)
            if response.status_code == 200:
                process_output(response.json(), region, dist_id)
            else:
                print("[X] API call failed. {} status code. Error : \n{}".format(response.status_code, str(response.content)))
        print('\n[I] Sleeping for {} sec...\n'.format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)

def main():
    reg_id = get_input()
    poll_cowin_portal(reg_id)

if __name__ == '__main__':
    main()