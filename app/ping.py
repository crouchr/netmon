
import run_sh_cmd

# fping : 8.8.8.8 : xmt/rcv/%loss = 10/10/0%, outage(ms) = 0, min/avg/max = 12.0/13.0/16.6
def extract_ping_measurements(console_output):
    try:
        ping_measurements = {}

        a = console_output.split('loss = ')[1]
        packet_loss = a.split('/')[2]
        packet_loss = packet_loss.split('%')[0]
        ping_measurements['packet_loss'] = float(packet_loss)

        if 'min/avg/max' in console_output:
            b = console_output.split('min/avg/max = ')[1]
            rtt_min = b.split('/')[0]
            rtt_avg = b.split('/')[1]
            rtt_max = b.split('/')[2]
        else:
            rtt_min = -10.0
            rtt_avg = -10.0
            rtt_max = -10.0

        ping_measurements['rtt_min'] = float(rtt_min)
        ping_measurements['rtt_avg'] = float(rtt_avg)
        ping_measurements['rtt_max'] = float(rtt_max)

        return ping_measurements

    except Exception as e:
        print(e.__str__)
        return None

# 'PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.6 ms
#
# --- 8.8.8.8 ping statistics ---
# 1 packets transmitted, 1 received, 0% packet loss, time 0ms
# rtt min/avg/max/mdev = 12.658/12.658/12.658/0.000 ms
# '
# fping has to be run as root


def ping_endpoint(dest_ip):
    """

    :param dest_host:
    :return:
    """

    try:
        rtt_msecs = -5.0

        # flush ARP caches etc.
        #cmd_str = 'ping ' + dest_ip + ' -c 5 '
        #run_sh_cmd.run_sh_cmd(cmd_str)

        # the real one !
        # cmd_str = 'sudo /usr/sbin/fping ' + dest_ip + ' -c 10 -p 100 -o -q -t 500'
        cmd_str = 'sudo /usr/sbin/fping ' + dest_ip + ' -c 10 -p 100 -o -q -t 500'
        console_output = run_sh_cmd.run_sh_cmd(cmd_str)

        # regular ping : 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.6 ms
        # fping : 8.8.8.8 : xmt/rcv/%loss = 10/10/0%, outage(ms) = 0, min/avg/max = 12.0/13.0/16.6
        # lines = console_output.split('\n')
        # for line in lines:
        #     if '100% packet loss' in line:
        #         rtt_msecs = -5.0
        #     if '64 bytes from ' in line:
        #         parts = line.split(' ')
        #         time = parts[6]
        #         rtt_msecs = time.split('=')[1]

        ping_measurements = extract_ping_measurements(console_output)


        return ping_measurements

    except Exception as e:
        print('ping_endpoint() : Error=' + e.__str__())
        return -5.0
