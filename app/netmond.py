import time
from pprint import pprint

import get_env
import get_env_app
import send_metrics_to_telegraf

# Different tests
import ping
import iperf

import host


def main():
    hosts = []
    version = get_env.get_version()
    verbose = get_env.get_verbose()
    stage = get_env.get_stage()

    telegraf_endpoint_host = get_env_app.get_telegraf_endpoint()    # can be read from ENV
    poll_secs = get_env_app.get_poll_secs()
    probe_name = get_env_app.get_probe_name()

    print('netmond started, version=' + version)
    print('verbose=' + verbose.__str__())
    print('stage=' + stage.__str__())
    print('telegraf_endpoint_host=' + telegraf_endpoint_host)
    print('poll_secs=' + poll_secs.__str__())
    print('probe_name=' + probe_name.__str__())

    # does not exist - for testing purposes
    # host_x = host.Host('blackhole', '192.168.1.199', False)
    # hosts.append(host_x)

    host_x = host.Host('j1900', '192.168.1.6', True)
    hosts.append(host_x)

    host_x = host.Host('dsl_router', '192.168.1.1', False)
    hosts.append(host_x)

    host_x = host.Host('google_dns', '8.8.8.8', False)
    hosts.append(host_x)

    host_x = host.Host('netgear', '192.168.1.8', False)
    hosts.append(host_x)

    host_x = host.Host('pi', '192.168.1.12', True)
    hosts.append(host_x)

    host_x = host.Host('web_server', '192.168.1.102', False)
    hosts.append(host_x)

    host_x = host.Host('registry', '192.168.1.109', False)
    hosts.append(host_x)

    if stage == 'DEV':
        sudo = True
    else:
        sudo = False

    while True:
        try:
            for host_to_test in hosts:
                if host_to_test.iperf_capable:
                    jitter_measurements = iperf.measure_jitter_endpoint(host_to_test.hostname)
                    throughput_measurements = iperf.measure_throughput_endpoint(host_to_test.hostname)

                ping_measurements = ping.ping_endpoint(host_to_test.hostname, sudo)

                # Construct the metric bundle
                metric_name = 'netmon_' + probe_name + '_to_' + host_to_test.name
                metrics = {
                    'metric_name': metric_name,
                    'packet_loss': ping_measurements['packet_loss'],
                    'rtt_min': ping_measurements['rtt_min'],
                    'rtt_avg': ping_measurements['rtt_avg'],
                    'rtt_max': ping_measurements['rtt_max']
                }

                # if destination is iperf-capable then add throughput metric
                if host_to_test.iperf_capable:
                    metrics['throughput_mbps'] = throughput_measurements['throughput_mbps']
                    metrics['jitter'] = jitter_measurements['jitter']

                pprint(metrics)

                send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)
                time.sleep(2)

            # wait for next cycle of pinging hosts
            time.sleep(poll_secs)

        except Exception as e:
            print('main() : Error : ' + e.__str__())
            print('sleeping...')
            time.sleep(60)     # wait 1 mins
            continue


if __name__ == '__main__':
    main()
