#!/usr/bin/env python

import docker
import subprocess
import os
import sys

client = docker.from_env()
severity_level = os.environ['TRIV_LEVEL'] if 'TRIV_LEVEL' in os.environ else "CRITICAL"
verbose = True if 'TRIV_VERBOSE' in os.environ else False
images = set()
service_list = {}
exit_code = 0

for service in client.services.list():
    for task in service.tasks():
        short_image_name = task['Spec']['ContainerSpec']['Image'].split('@', 1)[0]
        images.add(short_image_name)
        if short_image_name not in service_list:
            service_list[short_image_name] = set()
        service_list[short_image_name].add(service.name)

if verbose:
    print(f"Scanning the following images : {images}")

for image in images:
    try:
        trivy = subprocess.run(["trivy", "--exit-code", "1", "--severity", severity_level, image], capture_output=True)
    except:
        exit_code = 2
        print("Error/Exception while running trivy")
        break
    if trivy.returncode == 1:
        exit_code = 1
        print(f"Image {image} has {severity_level} vulnarabilities. ", end='')
        print(f"Used in service(s) {service_list[image]}")
        if verbose:
            print(f"###### Output from trivy scan of {image} ######")
            for line in trivy.stdout.splitlines():
                print(line)
            print(f"###### End of output from trivy scan of {image} ######")
    if verbose and trivy.returncode == 0:
        print(f"Image {image} has no vulnarabilties")
    if trivy.returncode > 1 or trivy.returncode < 0:
        print(f"Unexpected return code from Trivy {trivy.returncode} while scanning {image}")
        exit_code = 2

sys.exit(exit_code)
