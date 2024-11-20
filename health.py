import xml.etree.ElementTree as ET
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


route = '01.xml'

tree = ET.parse(route, parser=ET.XMLParser(encoding='utf-8'))
root = tree.getroot()

namespace = {'': 'urn:hl7-org:v3', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
times=[]
heart=[]
Name = None
for sourceName_tag in root.findall('.//{urn:hl7-org:v3}sourceName', namespaces=namespace):
    checkName = sourceName_tag.text
    if checkName != 'Zepp Life':
        Name = checkName

    with open('output.txt','w') as f: 
        if Name:
            f.write(f'您好！{Name}，以下是您的心率數據：\n\n')

for observation in root.findall('.//{urn:hl7-org:v3}observation', namespaces=namespace):
    effective_time = observation.find('.//{urn:hl7-org:v3}effectiveTime', namespaces=namespace)

    if effective_time is not None:
        time = effective_time.find('.//{urn:hl7-org:v3}low', namespaces=namespace)
        
        if time is not None:
            time_value = time.get('value')
            TWtime = datetime.strptime(time_value, '%Y%m%d%H%M%S%z')
            TWtime = TWtime.strftime('%Y/%m/%d %H:%M:%S')
            
 
    value_tag = observation.find('.//{urn:hl7-org:v3}value[@xsi:type="PQ"]', namespaces=namespace)
    string = None

    try:
        if value_tag is not None:
            value = value_tag.get('value')
            unit = value_tag.get('unit')

            if unit == "count/min":
                string = value + " " + unit
                heart.append(int(value))
                times.append(TWtime)
                with open('output.txt','a') as f:
                    if string is not None:
                        f.write(f'時間:{TWtime}\n')
                        f.write(f'心率:{string}\n')
                        f.write('-------\n')
    except:
        pass



if len(times) != len(heart):
    print(f"Warning: 您的資料時間長度資料：({len(times)})及心率長度資料：({len(heart)})數量並不對等。")
else:
    df = pd.DataFrame({'time': times, 'heart_rate': heart})
    df['time'] = pd.to_datetime(df['time']) 
    df.set_index('time', inplace=True)
    df_resampled = df.resample('M').mean().dropna() 

    plt.figure(figsize=(10, 5))
    plt.plot(df_resampled.index, df_resampled['heart_rate'], color='blue',marker='o', linestyle='-')
    plt.title('Data changes')
    plt.xlabel('time')
    plt.ylabel('heart (count/min)')
    plt.tight_layout()
    plt.grid()
    plt.savefig('heart.png')
    plt.show()
