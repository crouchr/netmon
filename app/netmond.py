

import time
from pprint import pprint

import get_env
import get_env_app
import send_metrics_to_telegraf
import run_sh_cmd


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
        rtt_msecs = -1.0

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
                rtt_msecs = -1.0
            if '64 bytes from ' in line:
                parts = line.split(' ')
                time = parts[6]
                rtt_msecs = time.split('=')[1]

        return rtt_msecs

    except Exception as e:
        print('ping_endpoint() : Error=' + e.__str__())
        return -1.0


def main():
    version = get_env.get_version()
    verbose = get_env.get_verbose()

    telegraf_endpoint_host = get_env_app.get_telegraf_endpoint()    # can be read from ENV
    poll_secs = get_env_app.get_poll_secs()

    print('netmond started, version=' + version)
    print('verbose=' + verbose.__str__())
    print('telegraf_endpoint_host=' + telegraf_endpoint_host)
    print('poll_secs=' + poll_secs.__str__())

    while True:
        try:
            dest_name = 'google_dns'
            dest_ip = '8.8.8.8'

            # dest_ip = '111.111.111.1118'
            # result = ping_endpoint('8.8.8.8')
            rtt_msecs = ping_endpoint(dest_ip)

            print(
                'dest=' + dest_ip + \
                ', rtt_msecs=' + rtt_msecs.__str__()
                )

            # Construct the metric bundle
            metric_name = 'netmon_' + dest_name
            metrics = {
                'metric_name': metric_name,
                'rtt': round(float(rtt_msecs), 2),
            }
            # pprint(metrics)

            send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)

            time.sleep(poll_secs)

        except Exception as e:
            print('Error : ' + e.__str__())
            print('sleeping...')
            # beep.warning(num_beeps=2, sound=3)
            time.sleep(60)     # wait 3 mins
            continue


if __name__ == '__main__':
    main()
