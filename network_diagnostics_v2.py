import subprocess
import speedtest
import re
import json
import csv
import sys
import argparse
import time
from datetime import datetime
from statistics import mean, stdev

def run_ping(host='8.8.8.8', count=20):
    try:
        result = subprocess.run(['ping', '-c', str(count), host], capture_output=True, text=True)
        output = result.stdout
        loss_search = re.search(r'(\d+)% packet loss', output)
        loss = float(loss_search.group(1)) if loss_search else None
        rtts = [float(m.group(1)) for m in re.finditer(r'time=([0-9.]+) ms', output)]
        stats = {
            'host': host,
            'sent': count,
            'recv': len(rtts),
            'loss_pct': loss,
            'rtt_ms_min': min(rtts) if rtts else None,
            'rtt_ms_avg': mean(rtts) if rtts else None,
            'rtt_ms_max': max(rtts) if rtts else None,
            'rtt_ms_std': stdev(rtts) if len(rtts)>1 else None,
            'rtts_ms': rtts
        }
        return stats
    except Exception as e:
        return {'host': host, 'error': str(e)}

def run_speedtest(repeats=3, pause_sec=2):
    ds, us, servers, errors = [], [], [], []
    for i in range(repeats):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download()/1_000_000
            upload = st.upload()/1_000_000
            ds.append(download)
            us.append(upload)
            servers.append(st.results.server['host'])
        except Exception as e:
            errors.append(str(e))
        time.sleep(pause_sec)
    summary = {
        'download_Mbps': {'mean': mean(ds) if ds else None, 'std': stdev(ds) if len(ds)>1 else None, 'min': min(ds) if ds else None, 'max': max(ds) if ds else None, 'raw': ds},
        'upload_Mbps': {'mean': mean(us) if us else None, 'std': stdev(us) if len(us)>1 else None, 'min': min(us) if us else None, 'max': max(us) if us else None, 'raw': us},
        'test_servers': list(set(servers)),
        'repeats': repeats,
        'errors': errors
    }
    return summary

def export_json(data, path):
    with open(path,"w") as f:
        json.dump(data, f, indent=2)

def export_csv(ping, stest, path):
    with open(path,"w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp']+list(ping.keys())+['dl_mean','dl_std','ul_mean','ul_std','dl_raw','ul_raw','st_servers','st_errors'])
        writer.writerow([
            datetime.now().isoformat(),
            *[ping[k] for k in ping.keys()],
            stest['download_Mbps']['mean'],stest['download_Mbps']['std'],
            stest['upload_Mbps']['mean'],stest['upload_Mbps']['std'],
            stest['download_Mbps']['raw'],stest['upload_Mbps']['raw'],
            ';'.join(map(str,stest['test_servers'])), ';'.join(stest['errors'])
        ])

def main():
    parser = argparse.ArgumentParser(description='Advanced Network Diagnostic Tool (ping+speedtest)')
    parser.add_argument('--host',type=str,default='8.8.8.8',help='Ping host')
    parser.add_argument('--count',type=int,default=20,help='Number of pings')
    parser.add_argument('--speed_repeats',type=int,default=3,help='Speedtest repetitions')
    parser.add_argument('--pause',type=float,default=2.0,help='Pause seconds between speedtests')
    parser.add_argument('--json',type=str,default='/root/diag_results.json',help='Output JSON path')
    parser.add_argument('--csv',type=str,default='/root/diag_results.csv',help='Output CSV path')
    args = parser.parse_args()
    meta = {
        'timestamp': datetime.now().isoformat(),
        'host': args.host, 'ping_count': args.count,
        'speed_repeats': args.speed_repeats, 'pause_s': args.pause,
        'platform': sys.platform
    }
    print('== PING ==')
    ping_stats = run_ping(args.host, args.count)
    for k,v in ping_stats.items():
        print(f'{k}: {v}')
    print('== SPEEDTEST ==')
    speed_stats = run_speedtest(args.speed_repeats, args.pause)
    for d in ['download_Mbps','upload_Mbps']:
        if speed_stats[d]['mean'] is not None:
            print(f"> {d}: mean {speed_stats[d]['mean']:.2f} Mbps, std {speed_stats[d]['std']:.2f} Mbps, raw: {speed_stats[d]['raw']}")
        else:
            print(f"> {d}: No valid samples.")
    if speed_stats['errors']:
        print('Errors during speedtest:', '; '.join(speed_stats['errors']))
    out = {'meta':meta,'ping':ping_stats,'speedtest':speed_stats}
    export_json(out,args.json)
    export_csv(ping_stats,speed_stats,args.csv)
    print(f"Results saved to: {args.json}, {args.csv}")

if __name__=='__main__':
    main()
