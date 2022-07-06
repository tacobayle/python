# python Avi VS

## Goals
Configure a Health Monitor, Pool and VS through Python (Python SDK)

## Prerequisites:
1. Make sure python3 is installed
2. Make sure pip install avisdk is installed:
```
pip install avisdk
```
3. Make sure your Avi Controller is reachable from your host
4. Make sure you have an IPAM/DNS profile is configured

## Environment:

### Avi version

```
Avi 21.1.4
```

### Avi Environment

- vCenter Cloud


## Input/Parameters:

- Make sure you have a json file with the Avi credentials like the following:

```
avi@ansible:~/python/aviVs$ more creds.json
{"avi_credentials": {"username": "admin", "controller": "192.168.142.135", "password": "*****", "api_version": "18.2.9"}}

```

- All the other paramaters/variables are stored in the python script aviVs.py.
The below variable(s) called need(s) to be adjusted:
```
   pool_server_list = ['100.64.130.203', '100.64.130.204']
   cloud_name = 'dc1_vCenter'
   domain_name = 'vmw.avidemo.fr'
   network_name = "vxw-dvs-34-virtualwire-118-sid-1080117-sof2-01-vc08-avi-dev114"
```   
   The other varaiables don't need to be adjusted.
```
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
```

## Use the the python script to:
- Create a Health Monitor 
- Create a Pool (based on the Health Monitor previously created)
- Retrieve the network details (first subnet)
- Create a vsvip based on IPAM and DNS 
- Create a VS based on pool and vsvip previously configured

## Run the terraform:
- clone git
```
git clone https://github.com/tacobayle/python
cd python/aviVs
```

- deploy:
```
python3 aviVs.py creds.json
```

## Improvements:
- add SE service group
- add log and analytics capabilities
```
resource "avi_virtualservice" "https_vs" {
  name                          = var.vs_name
  pool_group_ref                = avi_poolgroup.poolgroup1.id
  tenant_ref                    = data.avi_tenant.default_tenant.id
  vsvip_ref                     = avi_vsvip.test_vsvip.id
  cloud_ref                     = data.avi_cloud.default_cloud.id
  ssl_key_and_certificate_refs  = [data.avi_sslkeyandcertificate.ssl_cert1.id]
  ssl_profile_ref               = data.avi_sslprofile.ssl_profile1.id
  application_profile_ref       = data.avi_applicationprofile.application_profile1.id
  network_profile_ref           = data.avi_networkprofile.network_profile1.id
  services {
    port           = var.vs_port
    enable_ssl     = true
  }
  analytics_policy {
    client_insights = "NO_INSIGHTS"
    all_headers = "false"
    udf_log_throttle = "10"
    significant_log_throttle = "0"
    metrics_realtime_update {
      enabled  = "true"
      duration = "0"
    }
    full_client_logs {
        enabled = "true"
        throttle = "10"
        duration = "30"
    }
  }
}
```
