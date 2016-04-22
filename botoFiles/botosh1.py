#!/usr/bin/python

import os
import boto

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *

EC2_ACCESS_KEY = (os.environ["EC2_ACCESS_KEY"])
EC2_SECRET_KEY = (os.environ["EC2_SECRET_KEY"])
region = RegionInfo(name="melbourne-np", endpoint="nova.rc.nectar.org.au")
connection = boto.connect_ec2(aws_access_key_id=EC2_ACCESS_KEY,
                    aws_secret_access_key=EC2_SECRET_KEY,
                    is_secure=True,
                    region=region,
                    validate_certs=False,
                    port=8773,
                    path="/services/Cloud")

reservations = connection.get_all_instances()
for instance in reservations:
    print 'id: ', instance.id,
#images = connection.get_all_images()
#print images

#Create an instance
connection.run_instances("ami-000022c5", key_name='Nectar_Key', instance_type='m1.small', security_groups=['NectarTwitterGroup'])

#Attach the volume to instance
#vol_req = connection.create_volume(50, "melbourne-np")
#connection.attch_volume(vol_req.id, instance.id, "/dev/vdc")
