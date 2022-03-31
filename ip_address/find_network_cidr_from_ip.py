from ipaddress import IPv4Interface
#
#
#
interface = IPv4Interface('10.41.135.46/22')
myreverse='.'.join(list(reversed(str(interface.network).split("/")[0].split(".")[:-1])))
print(myreverse)

