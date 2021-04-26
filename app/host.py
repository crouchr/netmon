class Host:
    def __init__(self, name, hostname, iperf_capable):
        self.name = name
        self.hostname = hostname
        self.iperf_capable = iperf_capable


class Destinations:
    def __init__(self, probe_name):
        self.hosts = []
        self.probe_name = probe_name

    def add_host(self, a):
        if a.name != self.probe_name:
          self.hosts.append(a)


# Test / sample code
if __name__ == '__main__':
    probe_name = 'kube'
    destinations = Destinations(probe_name)

    destinations.add_host(Host('trey', '192.168.1.1', True))
    destinations.add_host(Host('nos', '192.168.1.3', True))
    destinations.add_host(Host('kube', '192.168.1.5', True))
    destinations.add_host(Host('seven', '192.168.1.7', True))

    print()
