import time
from pprint import pprint

import get_env
import get_env_app
import send_metrics_to_telegraf
import run_sh_cmd
import host

# 'PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.6 ms
#
# --- 8.8.8.8 ping statistics ---
# 1 packets transmitted, 1 received, 0% packet loss, time 0ms
# rtt min/avg/max/mdev = 12.658/12.658/12.658/0.000 ms
# '
def ping_endpoint(dest_ip):
    """

    :param dest_host:
    :return:
    """

    try:
        rtt_msecs = -5.0

        # flush ARP caches etc.
        cmd_str = 'ping -c 2 ' + dest_ip
        run_sh_cmd.run_sh_cmd(cmd_str)

        # the real one !
        cmd_str = 'ping -c 1 ' + dest_ip
        console_output = run_sh_cmd.run_sh_cmd(cmd_str)

        # 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.6 ms
        lines = console_output.split('\n')
        for line in lines:
            if '100% packet loss' in line:
                rtt_msecs = -5.0
            if '64 bytes from ' in line:
                parts = line.split(' ')
                time = parts[6]
                rtt_msecs = time.split('=')[1]

        return rtt_msecs

    except Exception as e:
        print('ping_endpoint() : Error=' + e.__str__())
        return -5.0


def main():
    hosts = []
    version = get_env.get_version()
    verbose = get_env.get_verbose()

    telegraf_endpoint_host = get_env_app.get_telegraf_endpoint()    # can be read from ENV
    poll_secs = get_env_app.get_poll_secs()

    print('netmond started, version=' + version)
    print('verbose=' + verbose.__str__())
    print('telegraf_endpoint_host=' + telegraf_endpoint_host)
    print('poll_secs=' + poll_secs.__str__())

    host_x = host.Host('google_dns', '8.8.8.8')
    hosts.append(host_x)

    host_x = host.Host('dsl_router', '192.168.1.1')
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

    while True:
        try:
            for host_to_test in hosts:
                # print()
                rtt_msecs = ping_endpoint(host_to_test.hostname)

                # print(
                #     'dest=' + host_to_test.hostname + \
                #     ', rtt_msecs=' + rtt_msecs.__str__()
                #     )

                # Construct the metric bundle
                metric_name = 'netmon_' + host_to_test.name
                metrics = {
                    'metric_name': metric_name,
                    'rtt': round(float(rtt_msecs), 2),
                }
                # pprint(metrics)

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
