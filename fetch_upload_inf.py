import  os, csv, json
from urllib.request import urlopen

token = os.environ.get("YCDA2RxkOhJu_mZtWelcjhnb_PEbidIzC6FiN0STq1PmpYApqfa1wD4l9IvDbXWjobXl3jxorhOwDpKM10QIBQ==")
org = "c41d73e5d6fea323"
url = "https://odk.fmt.bme.hu:8086/orgs/c41d73e5d6fea323"




def fetch_curr():
    url_budaAPI = "https://api.weather.com/v2/pws/observations/current?stationId=IBUDAP126&format=json&units=m&apiKey=6ec49650c67e479e849650c67ed79e18"
    response = urlopen(url_budaAPI)
    data_json = json.loads(response.read())
    curr_time = data_json['observations'][0]['obsTimeUtc']
    curr_SolRad = data_json['observations'][0]['solarRadiation']
    curr_uv = data_json['observations'][0]['uv']
    curr_windir = data_json['observations'][0]['winddir']
    curr_hum = data_json['observations'][0]['humidity']
    curr_temp = data_json['observations'][0]['metric']['temp']
    curr_dewpt = data_json['observations'][0]['metric']['dewpt']
    curr_windspd = data_json['observations'][0]['metric']['windSpeed']
    curr_windgst = data_json['observations'][0]['metric']['windGust']
    curr_pressure = data_json['observations'][0]['metric']['pressure']
    curr_precip = data_json['observations'][0]['metric']['precipRate']
    curr_precipTot = data_json['observations'][0]['metric']['precipTotal']
    readings_lst = [curr_time, curr_SolRad, curr_uv, curr_windir, curr_hum, curr_temp, curr_dewpt, curr_windspd, curr_windgst, curr_pressure, curr_precip, curr_precipTot]
    for k, v in enumerate(readings_lst):
        if readings_lst[k] == None:
            readings_lst[k] = 0
    
    return readings_lst
    
def parse_to_csv(reading_lst, file_to):
    header = ['#group','FALSE','TRUE','TRUE','TRUE','TRUE','TRUE','TRUE']
    header_extra = [
        ['#datatype','string','string','string','string','string','double','dateTime:RFC3339'],
        ['#default','_result','','','','','',''],
        ['','result','nodes','_field','_tag','_measurement','_value','_time']
    ]
    curr_time, curr_SolRad, curr_uv, curr_windir, curr_hum, curr_temp, curr_dewpt, curr_windspd, curr_windgst, curr_pressure, curr_precip, curr_precipTot = reading_lst
    data_ls = []
    readings_lst = ["","",f"node{1}","temperature","tempAvg", "tempAvg", curr_temp,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","humidity","humAvg","humAvg", curr_hum,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","solarradiation","solRad","solRad", curr_SolRad,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","uv","uvHigh","uvHigh", curr_uv,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","winddirection","winddirAvg","winddirAvg", curr_windir,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","dewpoint","dwpt","dwpt", curr_dewpt,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","windspeed","windspeedAvg","windspeedAvg", curr_windspd,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","windgust","windgustAvg","windgustAvg", curr_windgst,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","pressureMax","prsrMax","prsrMax", curr_pressure,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","precipitationRate","precipRate","precipRate", curr_precip,curr_time]
    data_ls.append(list(readings_lst))
    readings_lst = ["","",f"node{1}","precipitationTotal","precipTot","precipTot", curr_precipTot,curr_time]
    data_ls.append(list(readings_lst))
    
    with open(file_to, 'w+', newline='') as csvf:
        writer = csv.writer(csvf, delimiter=',')
        writer.writerow(header)
        writer.writerows(header_extra)
        writer.writerows(data_ls)


# def write_to_inflx():
#     readings_lst = fetch_curr()
#     time_read = readings_lst[0]
    
#     write_api = client.write_api(write_options=SYNCHRONOUS)
#     bucket="w9smfo"
#     psol = Point("curr_solrad").tag("solrad", f"{readings_lst[1]}").field("solarradiation", readings_lst[1]).time(time_read)
#     puv = Point("curr_uv").tag("uv", f"{readings_lst[2]}").field("uv", readings_lst[2]).time(time_read)
#     pwindir = Point("curr_winddir").tag("winddir", f"{readings_lst[3]}").field("winddirection", readings_lst[3]).time(time_read)
#     ph = Point("curr_hum").tag("hum", f"{readings_lst[4]}").field("humidity", readings_lst[4]).time(time_read)
#     pt = Point("curr_temp").tag("temp", f"{readings_lst[5]}").field("temperature", readings_lst[5]).time(time_read)
#     pdewpt = Point("curr_dewpt").tag("dewpt", f"{readings_lst[6]}").field("dewpoint", readings_lst[6]).time(time_read)
#     pwindspd = Point("curr_windspd").tag("windspd", f"{readings_lst[7]}").field("windspeed", readings_lst[7]).time(time_read)
#     pwindgst = Point("curr_windgst").tag("windgst", f"{readings_lst[8]}").field("windgust", readings_lst[8]).time(time_read)
#     ppress = Point("curr_pressr").tag("pressr", f"{readings_lst[9]}").field("pressure", readings_lst[9]).time(time_read)
#     pprec = Point("curr_prec").tag("prec", f"{readings_lst[10]}").field("precipitationrate", readings_lst[10]).time(time_read)
#     pprectot = Point("curr_prectot").tag("prectot", f"{readings_lst[11]}").field("precipitationtotal", readings_lst[10]).time(time_read)
    
#     points = [psol, puv, pwindir, ph, pt, pdewpt, pwindspd, pwindgst, pprec, ppress, pprectot]
#     for p in points:
#         cl_resp = write_api.write(bucket=bucket, org="c41d73e5d6fea323", record=p)
#         if cl_resp is None:
#             print("Written")



def main():
    readings = fetch_curr()
    parse_to_csv(readings, "curr_read.csv")


if __name__ == "__main__":
    main()
