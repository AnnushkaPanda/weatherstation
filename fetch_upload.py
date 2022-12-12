import  csv, json





def fetch_curr(file_from, file_to):
    header = ['#group','FALSE','TRUE','TRUE','TRUE','TRUE','TRUE','TRUE']
    header_extra = [
        ['#datatype','string','string','string','string','string','double','dateTime:RFC3339'],
        ['#default','_result','','','','','',''],
        ['','result','nodes','_field','_tag','_measurement','_value','_time']
    ]
    data_ls = []
    with open(file_from, 'r+') as jsf:
        data_json = json.load(jsf)
    for i in range(len(data_json['observations'])):
        curr_time = data_json['observations'][i]['obsTimeUtc']
        curr_SolRad = data_json['observations'][i]['solarRadiationHigh']
        curr_uv = data_json['observations'][i]['uvHigh']
        curr_windir = data_json['observations'][i]['winddirAvg']
        curr_hum = data_json['observations'][i]['humidityAvg']
        curr_temp = data_json['observations'][i]['metric']['tempAvg']
        curr_dewpt = data_json['observations'][i]['metric']['dewptAvg']
        curr_windspd = data_json['observations'][i]['metric']['windspeedAvg']
        curr_windgst = data_json['observations'][i]['metric']['windgustAvg']
        curr_pressuremax = data_json['observations'][i]['metric']['pressureMax']
        curr_pressuremin = data_json['observations'][i]['metric']['pressureMin']
        curr_precip = data_json['observations'][i]['metric']['precipRate']
        curr_precipTot = data_json['observations'][i]['metric']['precipTotal']
        readings_lst = ["","",f"node{i}","temperature","tempAvg", "tempAvg", curr_temp,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","humidity","humAvg","humAvg", curr_hum,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","solarradiation","solRad","solRad", curr_SolRad,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","uv","uvHigh","uvHigh", curr_uv,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","winddirection","winddirAvg","winddirAvg", curr_windir,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","dewpoint","dwpt","dwpt", curr_dewpt,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","windspeed","windspeedAvg","windspeedAvg", curr_windspd,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","windgust","windgustAvg","windgustAvg", curr_windgst,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","pressureMax","prsrMax","prsrMax", curr_pressuremax,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","pressureMin","prsrMin","prsrMin", curr_pressuremin,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","precipitationRate","precipRate","precipRate", curr_precip,curr_time]
        data_ls.append(list(readings_lst))
        readings_lst = ["","",f"node{i}","precipitationTotal","precipTot","precipTot", curr_precipTot,curr_time]
        data_ls.append(list(readings_lst))
    
    with open(file_to, 'w+', newline='') as csvf:
        writer = csv.writer(csvf, delimiter=',')
        writer.writerow(header)
        writer.writerows(header_extra)
        writer.writerows(data_ls)
        




def main():
    fetch_curr("buda.json", "parsedbuda_test.csv")


if __name__ == "__main__":
    main()
