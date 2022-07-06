from avi.sdk.avi_api import ApiSession
import sys, json
#
# Variables to be modified
#
pool_server_list = ['100.64.130.203', '100.64.130.204']
cloud_name = 'dc1_vCenter'
domain_name = 'vmw.avidemo.fr'
network_name = "vxw-dvs-34-virtualwire-118-sid-1080117-sof2-01-vc08-avi-dev114"
#
#
# other variables
#
fileCredential = sys.argv[1]
tenant = "admin"
objectPrefix = 'python-'
# Health Monitor
hmHttpName = 'hm1'
hmHttpType = 'HEALTH_MONITOR_HTTP'
hmHttpRt = 1
hmHttpFc = 3
hmHttpSi = 1
hmHttpR = 'HEAD / HTTP/1.0'
hmHttpRc = ["HTTP_2XX", "HTTP_3XX", "HTTP_5XX"]
hmHttpSc = 2
# Pool
poolName = 'pool1'
poolA = 'LB_ALGORITHM_ROUND_ROBIN'
poolHm = hmHttpName
poolPort = 80
# Vs
vsName = 'app1'
vsPorts = [80, 443]
vsSslProfile = 'System-Standard'
vsSslCertificate = 'System-Default-Cert'
#
# Avi class
#
class aviSession:
  def __init__(self, fqdn, username, password, tenant):
    self.fqdn = fqdn
    self.username = username
    self.password = password
    self.tenant = tenant

  def debug(self):
    print("controller is {0}, username is {1}, password is {2}, tenant is {3}".format(self.fqdn, self.username, self.password, self.tenant))

  def retrieveNetworkNameMaskType(self, network_name):
    api = ApiSession.get_session(self.fqdn, self.username, self.password, self.tenant)
    network = api.get('network?page_size=-1')
    for item in network.json()['results']:
        if item['name'] == network_name:
            uuid = item['uuid']
            mask = item['configured_subnets'][0]['prefix']['mask']
            network = item['configured_subnets'][0]['prefix']['ip_addr']['addr']
            type = item['configured_subnets'][0]['prefix']['ip_addr']['type']
            break
    return uuid, network, mask, type

  def getObjByName(self, object, objectName):
    api = ApiSession.get_session(self.fqdn, self.username, self.password, self.tenant)
    return api.get_object_by_name(object, objectName)

  def configureMyObjectMyData(self, myObject, myData):
    api = ApiSession.get_session(self.fqdn, self.username, self.password, self.tenant)
    myResult = api.post(myObject, data=myData)
    return myResult
#
# Main Pyhton script
#
if __name__ == '__main__':
    with open(fileCredential, 'r') as stream:
        credential = json.load(stream)
    stream.close
    defineClass = aviSession(credential['avi_credentials']['controller'], credential['avi_credentials']['username'], credential['avi_credentials']['password'], tenant)
    network_uuid, networkAddress, networkMask, networkType = defineClass.retrieveNetworkNameMaskType(network_name)
    print('Network uuid is {0}, Network Address is {1}, Network mask is {2}, Network type is {3}'.format(network_uuid, networkAddress, networkMask, networkType))
    #
    # Create a hm_data variable to be used when creating the health monitor
    #
    hm_data = {
      "receive_timeout": hmHttpRt,
      "name": objectPrefix + hmHttpName,
      "failed_checks": hmHttpFc,
      "send_interval": hmHttpSi,
      "http_monitor": {
        "http_request": hmHttpR,
        "http_response_code": hmHttpRc
      },
      "successful_checks": hmHttpSc,
      "type": hmHttpType
    }
    print('+++++++++++++++++++ Creating a http health monitor')
    print(defineClass.configureMyObjectMyData('healthmonitor', hm_data))
    #
    # Create a pool_data variable to be used when creating the pool
    #
    servers = []
    for server in pool_server_list:
        serverDict = {}
        serverDict['addr'] = server
        serverDict['type'] = 'V4'
        IpDict = {}
        IpDict['ip'] = serverDict
        servers.append(IpDict)
    pool_data = {
      "name": objectPrefix + poolName,
      "lb_algorithm:": poolA,
      "health_monitor_refs": ['/api/healthmonitor?name=' + objectPrefix + hmHttpName],
      "cloud_ref": '/api/cloud/?name=' + cloud_name,
      "servers": servers
    }
    print('+++++++++++++++++++ Creating a pool')
    print(defineClass.configureMyObjectMyData('pool', pool_data))
    #
    # Create a vsvip (ipam and DNS integration)
    #
    vsvip_data = {
      "name": objectPrefix + 'vsvip-' + vsName,
      "cloud_ref": '/api/cloud/?name=' + cloud_name,
      "dns_info": [{"fqdn": objectPrefix + vsName + '.' + domain_name}],
      "vip": [{"auto_allocate_ip": "true", "ipam_network_subnet": {"network_ref": network_uuid, "subnet": {"mask": networkMask, "ip_addr": {"type": networkType, "addr": networkAddress}}}}]
    }
    print('+++++++++++++++++++ Creating a vsvip')
    print(defineClass.configureMyObjectMyData('vsvip', vsvip_data))
    #
    # Create a list of services (with ssl enabled if tcp port == 443)
    #
    services = []
    for port in vsPorts:
        serviceDict = {}
        serviceDict['port'] = port
        if port != 443:
            serviceDict['enable_ssl'] = 'false'
        else:
            serviceDict['enable_ssl'] = 'true'
        services.append(serviceDict)
    #
    # Create a vs_data variable to be used when creating the VS
    #
    vs_data = {
      "name": objectPrefix + vsName,
      "ssl_profile_ref": "/api/sslprofile?name=" + vsSslProfile,
      "ssl_key_and_certificate_refs": "/api/sslkeyandcertificate?name=" + vsSslCertificate,
      "services" : services,
      "pool_ref": defineClass.getObjByName('pool', pool_data['name'])['uuid'],
      "vsvip_ref": defineClass.getObjByName('vsvip', objectPrefix + 'vsvip-' + vsName)['uuid'],
      "cloud_ref": '/api/cloud/?name=' + cloud_name
    }
    print('+++++++++++++++++++ Creating a vs')
    print(defineClass.configureMyObjectMyData('virtualservice', vs_data))