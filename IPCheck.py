#!/usr/bin/env python3
import subprocess

def get_unique_ips(request):
    project_ids = subprocess.check_output(['gcloud', 'projects', 'list', '--format=value(projectId)']).decode().splitlines()
    ip_addresses = []

    for project in project_ids:
        print("Project: ", project)

        internal_ips = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--project=' + project, '--format=value(networkInterfaces[0].networkIP)']).decode().splitlines()
        ip_addresses.extend(internal_ips)

        external_ips = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--project=' + project, '--format=value(networkInterfaces[0].accessConfigs[0].natIP)']).decode().splitlines()
        ip_addresses.extend(external_ips)

        load_balancer_ips = subprocess.check_output(['gcloud', 'compute', 'addresses', 'list', '--project=' + project, '--format=value(address)']).decode().splitlines()
        ip_addresses.extend(load_balancer_ips)

        sql_instance_ips = subprocess.check_output(['gcloud', 'sql', 'instances', 'list', '--project=' + project, '--format=value(ipAddresses.ipAddress)']).decode().splitlines()
        ip_addresses.extend(sql_instance_ips)

        print("------------------------------")

    # Remove duplicates from the IP addresses list
    unique_ip_addresses = list(set(ip_addresses))

    # Print the unique IP addresses
    print("Unique IP Addresses:")
    for uip in unique_ip_addresses:
        print(uip)

    return "Finished execution"

if __name__ == '__main__':
    get_unique_ips(None)
