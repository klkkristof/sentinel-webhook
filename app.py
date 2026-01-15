import psutil, datetime, requests

CPU_THRESHOLD = 90
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL"

def send_system_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    has_alert = (cpu_usage > CPU_THRESHOLD or
                 mem.percent > MEMORY_THRESHOLD or
                 disk.percent > DISK_THRESHOLD)

    if not has_alert:
        return

    embed = {
        "title": "Server Resource Alert",
        "color": 0xff0000,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "fields":[
            {
                "name": f"{'DANGER' if cpu_usage > CPU_THRESHOLD else 'OKAY'} CPU Usage",
                "value": f"{cpu_usage}%",
                "inline": True
            },
            {
                "name": f"{'DANGER' if mem.percent > MEMORY_THRESHOLD else 'OKAY'} Memory Usage",
                "value": f"{mem.percent}% ({mem.available / (1024**3):.2f} GB FREE)",
                "inline": True
            },
            {
                "name": f"{'DANGER' if disk.percent > DISK_THRESHOLD else 'OKAY'} Disk Usage",
                "value": f"{disk.percent}% ({disk.free / (1024**3):.2f} GB FREE)",
                "inline": True
            }
        ],
        "footer": {
            "text": "Linux Server Monitor"
        }
    }
    
    data = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"Webhook status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_system_status()
