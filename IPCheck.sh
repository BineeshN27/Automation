#!/bin/bash

project_ids=$(gcloud projects list --format="value(projectId)")
ip_addresses=()

for project in $project_ids; do
    echo "Project: $project"

    # Retrieve internal IP addresses of instances
    internal_ips=$(gcloud compute instances list --project="$project" --format="value(networkInterfaces[0].networkIP)")
    ip_addresses+=($internal_ips)

    # Retrieve external IP addresses of instances
    external_ips=$(gcloud compute instances list --project="$project" --format="value(networkInterfaces[0].accessConfigs[0].natIP)")
    ip_addresses+=($external_ips)

    # Retrieve IP addresses of load balancers
    load_balancer_ips=$(gcloud compute addresses list --project="$project" --format="value(address)")
    ip_addresses+=($load_balancer_ips)

    # Retrieve IP addresses of Cloud SQL instances
    sql_instance_ips=$(gcloud sql instances list --project="$project" --format="value(ipAddresses.ipAddress)")
    ip_addresses+=($sql_instance_ips)

    echo "------------------------------"
done

# Print the IP addresses array
echo "IP Addresses:"
for ip in "${ip_addresses[@]}"; do
    echo "$ip"
done


# Remove duplicates from the IP addresses array
unique_ip_addresses=($(echo "${ip_addresses[@]}" | tr ' ' '\n' | awk '!a[$0]++'))

# Print the unique IP addresses
echo "Unique IP Addresses:"
for uip in "${unique_ip_addresses[@]}"; do
    echo "$uip"
done
