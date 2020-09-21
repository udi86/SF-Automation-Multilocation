import json
import argparse
from collections import defaultdict
from config_parser import ConfigParser
from pprint import pprint
import json2html


def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def write_to_json(data, file_name):
    # Writing data to file data.json 
    with open(file_name + '.json', 'w') as _file:
        data_json_obj = json.dumps(data, indent=4)
        _file.write(data_json_obj)
    print("locations json created")


def determine_locations_count(hosts_data):
    locations = []
    for host in hosts_data:
        if "location_id" in host:
            if host["location_id"] not in locations:
                locations.append(str(host["location_id"]))
    locations_dict = defaultdict(list)
    return locations_dict


def prepare_data_by_location_hosts(hosts_data, from_subnet_1, to_subnet_1, from_subnet_2, to_subnet_2):
    locations_dict = determine_locations_count(hosts_data)
    locations_dict['0'] = []
    for host in hosts_data:
        if "location_id" in host:
            if host["location_id"] == 1:
                if to_subnet_1 >= host["ip_numeric"] >= from_subnet_1:
                    locations_dict[host["location_id"]].append(host)
            elif host["location_id"] == 2:
                if to_subnet_2 >= host["ip_numeric"] >= from_subnet_2:
                    locations_dict[host["location_id"]].append(host)
        else:
            locations_dict['0'].append(host)
    return locations_dict


def prepare_data_ip_numeric(tcp_conversations_data, from_subnet_1,
                            to_subnet_1, from_subnet_2, to_subnet_2):
    sorted_tcp_conversations_data = {"Tcp Conversations": {"location1_entity_a": [],
                                                           "location2_entity_a": [],
                                                           "location1_entity_b": [],
                                                           "location2_entity_b": []}}
    for tcp_conversation in tcp_conversations_data:
        if from_subnet_1 <= tcp_conversation["entity_a"]["ip_numeric"] <= to_subnet_1:
            sorted_tcp_conversations_data["Tcp Conversations"]["location1_entity_a"].append(tcp_conversation)
        elif from_subnet_2 <= tcp_conversation["entity_a"]["ip_numeric"] <= to_subnet_2:
            sorted_tcp_conversations_data["Tcp Conversations"]["location2_entity_a"].append(tcp_conversation)

    for tcp_conversation in tcp_conversations_data:
        if from_subnet_1 <= tcp_conversation["entity_b"]["ip_numeric"] <= to_subnet_1:
            sorted_tcp_conversations_data["Tcp Conversations"]["location1_entity_b"].append(tcp_conversation)
        elif from_subnet_2 <= tcp_conversation["entity_b"]["ip_numeric"] <= to_subnet_2:
            sorted_tcp_conversations_data["Tcp Conversations"]["location2_entity_b"].append(tcp_conversation)
    return sorted_tcp_conversations_data


def sort_location_hosts(location_hosts, from_subnet, to_subnet):
    sorted_location_hosts = {"Hosts": []}
    for host in location_hosts:
        if to_subnet >= host["ip_numeric"] >= from_subnet:
            sorted_location_hosts["Hosts"].append(host)
    return sorted_location_hosts


def sort_location_tcp_conversations(location_tcp_conversations, from_subnet, to_subnet):
    sorted_location_tcp_conversations = {"Tcp Conversations": {"entity_a": [],
                                                               "entity_b": []}}
    for tcp_conversation in location_tcp_conversations:
        if from_subnet <= tcp_conversation["entity_a"]["ip_numeric"] <= to_subnet:
            sorted_location_tcp_conversations["Tcp Conversations"]["entity_a"].append(tcp_conversation)
    for tcp_conversation in location_tcp_conversations:
        if from_subnet <= tcp_conversation["entity_b"]["ip_numeric"] <= to_subnet:
            sorted_location_tcp_conversations["Tcp Conversations"]["entity_b"].append(tcp_conversation)

        # elif from_subnet <= tcp_conversation["entity_b"]["ip_numeric"] <= to_subnet:
        #     sorted_location_tcp_conversations["Tcp Conversations"].append(tcp_conversation)
        # if to_subnet >= tcp_conversation["entity_a"]["ip_numeric"] >= from_subnet and\
        #         to_subnet >= tcp_conversation["entity_b"]["ip_numeric"] >= from_subnet:
        #     sorted_location_tcp_conversations["Tcp Conversations"].append(tcp_conversation)
    # print("entity_a: " + str(len(sorted_location_tcp_conversations["Tcp Conversations"]["entity_a"])))
    # print("entity_b: " + str(len(sorted_location_tcp_conversations["Tcp Conversations"]["entity_b"])))
    return sorted_location_tcp_conversations


def compare_hosts(locations_dict, sorted_location1_hosts, sorted_location2_hosts):
    pass
    # To Do


def format_report(locations_dict, sorted_locations1_hosts, sorted_locations2_hosts,
                  tcp_conversations_data, sorted_location1_tcp_conversations, sorted_location2_tcp_conversations):
    report_dict = {"Hosts": {
        "Sensor 2": len(sorted_locations2_hosts["Hosts"]),
        "Central Sensor 2": len(locations_dict[2]),
        "Central Sensor 1": len(locations_dict[1]),
        "Sensor 1": len(sorted_locations1_hosts["Hosts"])},
        "Tcp Conversations": {
            "Sensor 2 entity_a": len(sorted_location2_tcp_conversations["Tcp Conversations"]["entity_a"]),
            "Sensor 2 entity_b": len(sorted_location2_tcp_conversations["Tcp Conversations"]["entity_b"]),
            "Central Sensor 2 entity_a": len(tcp_conversations_data["location2_entity_a"]),
            "Central Sensor 2 entity_b": len(tcp_conversations_data["location2_entity_b"]),
            "Central Sensor 1 entity_a": len(tcp_conversations_data["location1_entity_a"]),
            "Central Sensor 1 entity_b": len(tcp_conversations_data["location1_entity_b"]),
            "Sensor 1 entity_a": len(sorted_location1_tcp_conversations["Tcp Conversations"]["entity_a"]),
            "Sensor 1 entity_b": len(sorted_location1_tcp_conversations["Tcp Conversations"]["entity_b"])
        }}
    return report_dict


def convert_json_to_html(report_dict):
    report_dict = {"Tcp Conversations": report_dict["Tcp Conversations"],
                   "Hosts": [report_dict["Hosts"]]}
    formatted_table = json2html.json2html.convert(json=report_dict)
    html_file = open("results.html", "w")
    html_file.write(formatted_table)
    html_file.close()


def main():
    config = ConfigParser()
    hosts_data = read_json(config.central_hosts_path)
    location1_hosts = read_json(config.location1_hosts_path)
    sorted_location1_hosts = sort_location_hosts(location1_hosts,
                                                 config.location1_from_ip,
                                                 config.location1_to_ip)
    location2_hosts = read_json(config.location2_hosts_path)
    sorted_location2_hosts = sort_location_hosts(location2_hosts,
                                                 config.location2_from_ip,
                                                 config.location2_to_ip)
    locations_dict = prepare_data_by_location_hosts(hosts_data,
                                                    config.location1_from_ip,
                                                    config.location1_to_ip,
                                                    config.location2_from_ip,
                                                    config.location2_to_ip)

    tcp_conversations_data = read_json(config.central_tcp_conversations_path)
    location1_tcp_conversations = read_json(config.location1_tcp_conversations_path)
    sorted_location1_tcp_conversations = sort_location_tcp_conversations(location1_tcp_conversations,
                                                                         config.location1_from_ip,
                                                                         config.location1_to_ip)
    location2_tcp_conversations = read_json(config.location2_tcp_conversations_path)
    sorted_location2_tcp_conversations = sort_location_tcp_conversations(location2_tcp_conversations,
                                                                         config.location2_from_ip,
                                                                         config.location2_to_ip)
    sorted_tcp_conversations_data = prepare_data_ip_numeric(tcp_conversations_data,
                                                            config.location1_from_ip,
                                                            config.location1_to_ip,
                                                            config.location2_from_ip,
                                                            config.location2_to_ip)
    report_dict = format_report(locations_dict,
                                sorted_location1_hosts,
                                sorted_location2_hosts,
                                sorted_tcp_conversations_data["Tcp Conversations"],
                                sorted_location1_tcp_conversations,
                                sorted_location2_tcp_conversations)
    convert_json_to_html(report_dict)


# def get_args():
#     parser = argparse.ArgumentParser(description='Prepare and compare data for compare')
#     # parser.add_argument('-c', nargs='+', help='Collections list to export')
#     parser.add_argument('-c1', help='Central hosts path')
#     parser.add_argument('-l1', help='Location 1 hosts path')
#     parser.add_argument('-l2', help='Location 2 hosts path')
#     parser.add_argument('-s1f', help='From subnet')
#     parser.add_argument('-s1t', help='To subnet')
#     parser.add_argument('-s2f', help='From subnet')
#     parser.add_argument('-s2t', help='To subnet')
#     return parser.parse_args()


if __name__ == '__main__':
    # args = get_args()
    # main(args.c1, args.l1, args.l2, long(args.s1f), long(args.s1t), long(args.s2f), long(args.s2t))
    main()
