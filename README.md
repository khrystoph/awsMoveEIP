# awsMoveEIP
Utility to detach an EIP and attach to a new instance

# Usage
To use this application, just make sure that you have python 2.7 or 3.x installed and boto3 and you can see the help this way:
```moveip -h```
Also, you can do the simplest form of usage here:
```moveip <ip_address> -i <destination_instance_id>```
As is built-in with boto3, you can simply specify a different profile or credentials by either exporting them OR using --profile:
```moveip <ip_address> -i <destination_instance_id> --profile <profile_name>```

This is intended as a quick and easy way to dissassociate and re-associate an IP address to the instance that you intend for it to be moved to.