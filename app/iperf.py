# Functions related to sending traffic to a en endpoint that runs iperf daemon
import run_sh_cmd


def extract_throughput_measurements(console_output):
    try:
        throughput_measurements = {}

        for line in console_output.split('\n'):
            if 'Connection refused' in line:
                throughput = -5.0
                break
            if 'receiver' in line:
                fields = line.split(' ')
                i = 0
                for a in fields:
                    if 'Mbits/sec' in a:
                        throughput = float(fields[i-1])
                        break
                    i = i + 1
                break

        throughput_measurements['throughput_mbps'] = throughput

        return throughput_measurements

    except Exception as e:
        print(e.__str__)
        throughput_measurements['throughput_mbps'] = -10.0
        return throughput_measurements


def measure_throughput_endpoint(dest_ip):
    """
    Measure throughput to a destination endpoint also running iperf3
    :param dest_host:
    :return:
    """

    try:
        cmd_str = 'iperf3 -c ' + dest_ip

        console_output = run_sh_cmd.run_sh_cmd(cmd_str)

        throughput_measurements = extract_throughput_measurements(console_output)

        return throughput_measurements

    except Exception as e:
        print('measure_throughput_endpoint() : Error=' + e.__str__())
        return None


def extract_jitter_measurements(console_output):
    try:
        jitter_measurements = {}

        for line in console_output.split('\n'):
            if 'Connection refused' in line:
                jitter = -5.0
                break
            if 'receiver' in line:
                fields = line.split(' ')
                i = 0
                for a in fields:
                    if 'ms' in a:
                        jitter = float(fields[i-1])
                        break
                    i = i + 1
                break

        jitter_measurements['jitter'] = jitter

        return jitter_measurements

    except Exception as e:
        print(e.__str__)
        jitter_measurements['jitter'] = -10.0
        return jitter_measurements


def measure_jitter_endpoint(dest_ip):
    """
    Measure jitter to a destination endpoint also running iperf3
    :param dest_host:
    :return:
    """

    try:
        cmd_str = 'iperf3 -c ' + dest_ip + ' -u'

        console_output = run_sh_cmd.run_sh_cmd(cmd_str)

        jitter_measurements = extract_jitter_measurements(console_output)

        return jitter_measurements

    except Exception as e:
        print('measure_jitter_endpoint() : Error=' + e.__str__())
        return None