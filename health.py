import xml.etree.ElementTree as ET
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

route = 'export_cda.xml'

tree = ET.parse(route)  
root = tree.getroot()

namespace = {'': 'urn:hl7-org:v3', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
times=[]
heart=[]

with open('output.txt','w') as f: 
    pass

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
    if value_tag is not None:
        value = value_tag.get('value')
        unit = value_tag.get('unit')
        if unit == "count/min":
            string = value + " " + unit
            heart.append(int(value))
            times.append(TWtime)
            # if string is not None:
            #     print(f"時間：{TWtime}")
            #     print(f'心率：{string}')
            #     print('---------')
            with open('output.txt','a') as f:
                if string is not None:
                    f.write(f'時間:{TWtime}\n')
                    f.write(f'心率:{string}\n')
                    f.write('-------\n')



if len(times) != len(heart):
    print(f"Warning: The length of times ({len(times)}) and heart ({len(heart)}) are not equal.")
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
    # plt.savefig('heart_rate_chart.png')
    plt.show()
