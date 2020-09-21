import configparser


class ConfigParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('Config.ini')
        self.location1_hosts_path = None
        self.location2_hosts_path = None
        self.central_hosts_path = None
        self.location1_tcp_conversations_path = None
        self.location2_tcp_conversations_path = None
        self.central_tcp_conversations_path = None
        self.location1_from_ip = None
        self.location1_to_ip = None
        self.location2_from_ip = None
        self.location2_to_ip = None
        self.read_data()

    def read_data(self):
        self.location1_hosts_path = self.config.get('Hosts', 'location1 hosts path')
        self.location2_hosts_path = self.config.get('Hosts', 'location2 hosts path')
        self.central_hosts_path = self.config.get('Hosts', 'central hosts path')
        self.location1_tcp_conversations_path = self.config.get('Tcp Conversations', 'location1 tcp conversations path')
        self.location2_tcp_conversations_path = self.config.get('Tcp Conversations', 'location2 tcp conversations path')
        self.central_tcp_conversations_path = self.config.get('Tcp Conversations', 'central tcp conversations path')
        self.location1_from_ip = long(self.config.get('Ip Numeric', 'location1 from ip'))
        self.location1_to_ip = long(self.config.get('Ip Numeric', 'location1 to ip'))
        self.location2_from_ip = long(self.config.get('Ip Numeric', 'location2 from ip'))
        self.location2_to_ip = long(self.config.get('Ip Numeric', 'location2 to ip'))
