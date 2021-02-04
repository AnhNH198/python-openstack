import requests
response = requests.get('https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(%22value%22) FROM %22instances%22 WHERE (%22tags1%22 %3D~ %2F%5E9fbd48d2-01b2-4490-a748-c27dd7083acf%24%2F AND %22tags2%22 %3D %27libvirt-kvm%27 AND %22tags3%22 %3D %27cpu%27 AND %22tags4%22 %3D %27total%27 AND %22tags5%22 %3D %27time%27) AND time %3E%3D now() - 24h GROUP BY time(2m) fill(none)&epoch=ms')
data = response.json()
print(f"{data}")