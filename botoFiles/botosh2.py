#!/usr/bin/python

from pprint import pprint
import os
import boto

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *

#EC2_ACCESS_KEY = (os.environ["EC2_ACCESS_KEY"])
#EC2_SECRET_KEY = (os.environ["EC2_SECRET_KEY"])
EC2_ACCESS_KEY="84a0d195974946619fca994f753d698c"
EC2_SECRET_KEY="fdea633e0b304b75a4d3ef6902bfa3ba"
region = RegionInfo(name="melbourne-np", endpoint="nova.rc.nectar.org.au")
connection = boto.connect_ec2(aws_access_key_id=EC2_ACCESS_KEY,
                    aws_secret_access_key=EC2_SECRET_KEY,
                    is_secure=True,
                    region=region,
                    validate_certs=False,
                    port=8773,
                    path="/services/Cloud")

reservations = connection.get_all_instances()
instances =  [i for r in reservations for i in r.instances]
for i in instances:
    pprint(i.__dict__)
    break
#images = connection.get_all_images()
#print images

#connection.run_instances("ami-00002f31", key_name='Nectar_Key', instance_type='m1.small', security_groups=['NectarTwitterGroup'])
