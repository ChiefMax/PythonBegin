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

    def on_key_event(event):
        nonlocal stop
        if event.name == 's':
            stop = True

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
        time.sleep(1)

    keyboard.unhook_all()

if __name__ == "__main__":
    main()


'''
Dear fellow human/programmer,

I deeply sorry for what I have started here. 
This code is generated by ChatGPT 3.5 to test what it can do without me knowing python.
It started as a joke at work as we were discussing the future of programmers as my company is laying off developers.
We joked that soon we would be replaced with ChatGPT users that have an interest in programming.
We each choose a language that we don't know and used ChatGPT to build a simple program.
It failed a few times, but since I knew what to ask it fixed the code for me.
I don't know where this is heading, but I do know we programmers need to adapt.

- a programmer.
''' 