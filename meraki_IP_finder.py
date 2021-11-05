
'''
Libraries
=========
meraki
keyring

Notes
=====

'''
import meraki
import keyring

api_key  = keyring.get_password("SRG_API", "API_KEY")
dashboard = meraki.DashboardAPI(api_key)


# Function to validate IP address entry#
def isValidIP(s):
     # check number of periods
    if s.count('.') != 3:
        return 'Invalid Ip address'
    l = list(map(str, s.split('.')))
     # check range of each number between periods
    for ele in l:
        if int(ele) < 0 or int(ele) > 255:
            return 'Invalid Ip address'
    return 'Valid Ip address'
#########################################    

ORG_name = input("Enter ORG Name:")
ipv4_address = input("Enter IP Address:")



print(isValidIP(ipv4_address))
# Break out if invalid IP address
if isValidIP(ipv4_address) == 'Invalid Ip address':
    exit()

response = dashboard.organizations.getOrganizations(suppress_logging=True, print_console=False, output_log=False)
loop_count=0
found=False
for item in response:
    if ORG_name==item["name"]:
        ORG_id = item["id"]
        organization_id = item["id"]
        found=True
        
       # Get all networks from ORG
        response_networks = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all', suppress_logging=True, print_console=False, output_log=False)

        # Run loop on all networks to find client  - Break when found
        for item in response_networks:
            loop_count+=1
            print("Searching Network: "+item["name"]+" "+str(loop_count))
            response_clients = dashboard.networks.getNetworkClients(item["id"], total_pages='all',suppress_logging=True, print_console=False, output_log=False)

            for item in response_clients:
                if ipv4_address==item["ip"]:
                 ip=item["ip"]
                 mac=item["mac"]
                 seen_on_device=item["recentDeviceName"]
                 connection_type=(item["recentDeviceConnection"])
                 switch_port=(item["switchport"])
                 os=(item["os"])
                 vlan=(item["vlan"])
                 status=(item["status"])
                 description=(item["description"])
                 break
            else:
             continue  # only executed if the inner loop did NOT break
            break  # only executed if the inner loop DID break

print("IP Address: "+ip)
print("MAC Address: "+mac)
print("Last seen on: "+seen_on_device+" Port: "+switch_port)
print("Connection Type: "+connection_type)
print("Hostname: "+str(description))
print("Operating System Detected: "+str(os))
print("VLAN ID: "+str(vlan))
print("Status: "+str(status))
