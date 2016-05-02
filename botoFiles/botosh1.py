# You need source ec2rc.sh file before running this script
# This script is used to manage the instances in Nectar Research Cloud
#!/usr/bin/python

import os
import boto

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *


#The parameters become environment value after source the file downloaded
#from Nectar Research Cloud 
EC2_ACCESS_KEY = (os.environ["EC2_ACCESS_KEY"])
EC2_SECRET_KEY = (os.environ["EC2_SECRET_KEY"])

#Define the cloud region information
region = RegionInfo(name="melbourne-np", endpoint="nova.rc.nectar.org.au")
#Connect to the Nectar Cloud with key information and region information
connection = boto.connect_ec2(aws_access_key_id=EC2_ACCESS_KEY,
                    aws_secret_access_key=EC2_SECRET_KEY,
                    is_secure=True,
                    region=region,
                    validate_certs=False,
                    port=8773,
                    path="/services/Cloud")

reservations = connection.get_all_instances()
#for instance in reservations:
#    print 'id: ', instance.id,
#images = connection.get_all_images()
#print images

#Create 4 instances
for x in range(0, 4):
    reservation = connection.run_instances("ami-000022c5", key_name='Nectar_Key', instance_type='m1.small', security_groups=['NectarTwitterGroup'], placement="melbourne-np")

#instance = reservation.instances[0]
#connection.create_tags([instance.id], {"Name": "1"})


#Create volumes for instances, 3 volumes are 50GB, 1 volume is 100GB
for x in range(0, 3):
    vol_req[x] = connection.create_volume(50, "melbourne-np")

vol_req[4] = connection.create_volume(100, "melbourne-np")

#Attach the volumes to instances
for x in range(0, 4):
    connection.attch_volume(vol_req[x], reservation.instance[x], "/dev/vdc")
