import requests
from urllib.parse import urlparse
import ipaddress


def get_tracker_list(tracker_urls):
    url = requests.get(tracker_urls)
    tracker_list = url.text.split('\n')
    return tracker_list


def process_tracker(tracker_list):
    count = 0

    # del the empty string
    tracker_list = [x for i in tracker_list if (x := i.strip()) != '']

    tracker_parts_list = []
    for tracker in tracker_list:
        t = urlparse(tracker)

        # form to a dict from a list
        tracker_parts = {
            'scheme': t.scheme,
            'hostname': t.hostname,
        }

        tracker_parts_list.append(tracker_parts)

    return tracker_parts_list


def process_hostname(tracker_parts_list):
    for t in tracker_parts_list:
        try:
            ip = ipaddress.ip_address(t.get('hostname'))
            if isinstance(ip, ipaddress.IPv4Address):
                t['ip'] = 'IPv4'
            elif isinstance(ip, ipaddress.IPv6Address):
                t['ip'] = 'IPv6'
        except ValueError:
            t['ip'] = 'hostname'

    # process the tracker_parts_list to three different list, ipv4, ipv6, server
    ipv4, ipv6, server = [], [], []
    for t in tracker_parts_list:
        if t.get('ip') == 'IPv4':
            ipv4.append(t)
        elif t.get('ip') == 'IPv6':
            ipv6.append(t)
        else:
            server.append(t)
    return ipv4, ipv6, server


def output_tracker(ipv4, ipv6, server, dns):
    with open('ipv4.txt', 'w') as f:
        for t in ipv4:
            line = f'{t.get("hostname")}/32\n'
            f.write(line)

    with open('ipv6.txt', 'w') as f:
        for t in ipv6:
            line = f'{t.get("hostname")}/128\n'
            f.write(line)
    with open('server.txt', 'w') as f:
        for t in server:
            line = f'server=/{t.get("hostname")}/{dns}\n'
            f.write(line)

    print('All Done')


if __name__ == '__main__':
    tracker_urls = 'https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt'
    tracker_list = get_tracker_list(tracker_urls)
    process_tracker(tracker_list)
    tracker_parts = process_tracker(tracker_list)
    ipv4, ipv6, server = process_hostname(tracker_parts)

    output_tracker(ipv4, ipv6, server, '8.8.8.8')
