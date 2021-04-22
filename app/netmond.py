import time
from pprint import pprint

import get_env
import get_env_app
import send_metrics_to_telegraf
import ping
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
    host_x = host.Host('blackhole', '192.168.1.199')
    hosts.append(host_x)

    host_x = host.Host('dsl_router', '192.168.1.1')
    hosts.append(host_x)

    host_x = host.Host('google_dns', '8.8.8.8')
    hosts.append(host_x)

    host_x = host.Host('j1900', '192.168.1.6')
    hosts.append(host_x)

    host_x = host.Host('netgear', '192.168.1.8')
    hosts.append(host_x)

    host_x = host.Host('pi', '192.168.1.12')
    hosts.append(host_x)

    host_x = host.Host('web_server', '192.168.1.102')
    hosts.append(host_x)

    host_x = host.Host('registry', '192.168.1.109')
    hosts.append(host_x)

    # host_x = host.Host('blackhole', '111.111.111.111')
    # hosts.append(host_x)

    if stage == 'DEV':
        sudo = True
    else:
        sudo = False

    while True:
        try:
            for host_to_test in hosts:
                # print()
                ping_measurements = ping.ping_endpoint(host_to_test.hostname, sudo)

                # print(
                #     'dest=' + host_to_test.hostname + \
                #     ', rtt_msecs=' + rtt_msecs.__str__()
                #     )

                # Construct the metric bundle
                metric_name = 'netmon_' + probe_name + '_to_' + host_to_test.name
                metrics = {
                    'metric_name': metric_name,
                    'packet_loss': ping_measurements['packet_loss'],
                    'rtt_min': ping_measurements['rtt_min'],
                    'rtt_avg': ping_measurements['rtt_avg'],
                    'rtt_max': ping_measurements['rtt_max'],
                }
                pprint(metrics)

                send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)
                time.sleep(2)

            # wait for next cycle of pinging hosts
            time.sleep(poll_secs)

        except Exception as e:
            print('Error : ' + e.__str__())
            print('sleeping...')
            # beep.warning(num_beeps=2, sound=3)
            time.sleep(60)     # wait 1 mins
            continue


if __name__ == '__main__':
    main()
