import psutil
import subprocess
import time
import keyboard

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    gpu_usage = get_gpu_usage()
    return cpu_usage, memory_usage, network_usage, gpu_usage

def get_gpu_usage():
    try:
        result = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"])
        gpu_usage = int(result.decode().strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        gpu_usage = 0
    return gpu_usage

def format_bytes(bytes):
    if bytes == 0:
        return "0B"
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while bytes >= 1024 and i < len(suffixes) - 1:
        bytes /= 1024.0
        i += 1
    f = ('%.2f' % bytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def update_terminal(content):
    print("\033[2J\033[H" + content, end="", flush=True)

def main():
    stop = False
    showFunnySentence = False
    
    def on_key_event(event):
        nonlocal stop
        nonlocal showFunnySentence
        if event.name == 's':
            stop = True
        elif event.name == 'h':
            showFunnySentence = True

    keyboard.on_press(on_key_event)

    while not stop:
        cpu_usage, memory_usage, network_usage, gpu_usage = get_system_info()
        network_usage = format_bytes(network_usage)
        content = (f"{'-' * 30}\n"
                    f"CPU Usage: {cpu_usage}%\n"
                   f"Memory Usage: {memory_usage}%\n"
                   f"Network Usage: {network_usage}\n"
                   f"GPU Usage: {gpu_usage}%\n"
                   f"{'-' * 30}")
        update_terminal(content)
        if showFunnySentence:
            funnyContent = "Fancy seeing you here!"
            update_terminal(funnyContent)
        time.sleep(1)

    keyboard.unhook_all()

if __name__ == "__main__":
    main()