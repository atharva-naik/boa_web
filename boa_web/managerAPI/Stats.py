import os, sys, math, json, time, GPUtil, psutil, getpass, logging, datetime, platform, threading

class EngagementTracker:
    pass


class PerformanceTracker:
    '''
    some code is inspired by: https://www.thepythoncode.com/article/get-hardware-system-information-python    
    '''
    def __init__(self, filename='perf_stats.log', freq=59):
        self.freq = freq
        self.stats = {"battery":0, "network":1, "cpu":2, "gpu":3, "keyboard":4, "default":5}
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename, "w", encoding="utf-8")
        self.logger.addHandler(self.handler)
        self.sysinfo = self.get_sysinfo() # get system information
        self.cpuinfo = self.get_cpuinfo() # get cpu information
        self.gpuinfo = self.get_gpuinfo() # get gpu information
        self.meminfo = self.get_meminfo() # get memory information
        # self.netinfo, self.srinfo = self.get_netinfo() 
        self.diskinfo, self.ioinfo = self.get_diskinfo()
        now = datetime.datetime.now()
        logging.info(f"running at: {os.path.realpath(__file__)}")
        logging.info(sys.version)
        logging.info(f"date: {now.strftime('%d %B %Y')}\nday: {now.strftime('%A')}")
        logging.info(f"\nSys info:\n {self._str(' ', **self.sysinfo)}")
        logging.info(f"\nMem info:\n {self._str(' ', **self.meminfo)}")
        logging.info(f"\nCPU info:\n {self._str(' ', **self.cpuinfo)}")
        logging.info(f"\nGPU info:")
        for i,info in enumerate(self.gpuinfo):
            logging.info(f" GPU {i}:")
            logging.info(self._str('  ', **self.gpuinfo[i]))        
        logging.info(f"\nDisk info:\n {self._str(' ', **self.ioinfo)}")
        for i,info in enumerate(self.diskinfo):
            logging.info(f" partition {i}:")
            logging.info(self._str('  ', **self.diskinfo[i]))

    def start(self):
        '''start logging stuff'''
        self.loggerThread = threading.Thread(target=self._log)
        self.loggerThread.start()

    def _log(self):
        self.log()
        time.sleep(self.freq)
        self._log()

    def _str(self, sep=", ", **kwargs):
        return sep.join(f"{k}={v}" for k,v in kwargs.items())

    def memh(self, bytes):
        '''Convert memory to human readable formats'''
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < 1024:
                return f"{bytes:.3f}{unit}B"
            bytes /= 1024

    def log(self):
        logging.info("\n"+datetime.datetime.now().strftime("%-I:%M:%S %p"))
        self.cpu_usage_info = self.get_cpu_usage()
        logging.info(f"cpu usage: {self._str(**self.cpu_usage_info)}")
        self.mem_usage_info = self.get_mem_usage()
        logging.info(f"mem usage: {self._str(**self.mem_usage_info)}")
        self.gpu_usage_info = self.get_gpu_usage()
        logging.info(f"gpu usage: {self._str(**self.gpu_usage_info)}")

    def get_sysinfo(self):
        info = {}
        uname = platform.uname()
        info["os"] = uname.system+"\n"
        info["user"] = getpass.getuser()+"\n"
        info["node_name"] = uname.node+"\n"
        info["arch"] = uname.machine+"\n"
        info["release"] = uname.release+"\n"
        info["version"] = uname.version+"\n"
        info["processor"] = uname.processor

        return info

    def get_cpuinfo(self):
        info = {}
        info["total_cores"] = f"{psutil.cpu_count(logical=True)}\n"
        info["physical_cores"] = f"{psutil.cpu_count(logical=False)}\n"
        cpu_freq = psutil.cpu_freq()
        info["max_freq"] = f"{cpu_freq.max:.4f} MHz\n"
        info["min_freq"] = f"{cpu_freq.min:.4f} MHz"

        return info

    def get_gpuinfo(self):
        info = []
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            ginf = {} # gpu info
            ginf["  id"] = f"{gpu.id}\n"
            ginf["name"] = gpu.name+"\n"
            ginf["uuid"] = gpu.uuid
            # ginf["load"] = f"{gpu.load*100}%\n"
            # ginf["temperature"] = f"{gpu.temperature} °C\n"
            # total = self.memh(2**20*gpu.memoryTotal)+"\n"
            # used = self.memh(2**20*gpu.memoryUsed)+"\n"
            # free = self.memh(2**20*gpu.memoryFree)
            # ginf["total"] = total 
            # ginf["used"] = used
            # ginf["free"] = free
            info.append(ginf)

        return info

    def get_meminfo(self):
        info = {}
        vmem = psutil.virtual_memory()
        smem = psutil.swap_memory()
        info["total_virtual_memory"] = f"{self.memh(vmem.total)}\n"
        info["total_swap_memory"] = f"{self.memh(smem.total)}"

        return info

    def get_diskinfo(self):
        info = []
        io_info = {}
        partitions = psutil.disk_partitions()
        for part in partitions:
            pinf = {} # dictionary of partition info
            pinf["  device"] = f"{part.device}\n"
            pinf["mountpoint"] = f"{part.mountpoint}\n"
            pinf["file_sys_type"] = part.fstype+"\n"
            try: part_usage = psutil.disk_usage(part.mountpoint)
            except PermissionError: continue # if partition isn't ready
            pinf["total"] = f"{self.memh(part_usage.total)}\n"
            pinf["used"] = f"{self.memh(part_usage.used)}\n"
            pinf["free"] = f"{self.memh(part_usage.free)}\n"
            pinf["percent"] = f"{self.memh(part_usage.percent)}"
            info.append(pinf)
        disk_io = psutil.disk_io_counters()
        io_info["read"] = f"{self.memh(disk_io.read_bytes)}\n"
        io_info["write"] = f"{self.memh(disk_io.write_bytes)}"

        return info, io_info

    def get_mem_usage(self):
        info = {}
        vmem = psutil.virtual_memory()
        used = self.memh(vmem.used)
        free = self.memh(vmem.available)
        info["virt_mem"] = f"used: {used} ({vmem.percent}%), free: {free}"
        smem = psutil.swap_memory()
        used = self.memh(smem.used)
        free = self.memh(smem.free)
        info["swap_mem"] = f"used: {used} ({smem.percent}%), free: {free}"

        return info

    def get_gpu_usage(self):
        info = {}
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            load = f"{gpu.load*100}%"
            temperature = f"{gpu.temperature} °C"
            total = self.memh(2**20*gpu.memoryTotal)
            used = self.memh(2**20*gpu.memoryUsed)
            free = self.memh(2**20*gpu.memoryFree)
            info[f"GPU_{gpu.id}"] = f"load: {load}, temp: {temperature}, used: {used}, free: {free}, total: {total}"

        return info

    def get_cpu_usage(self):
        info = {}
        cpu_freq = psutil.cpu_freq()
        info["freq"] = f"{cpu_freq.current:.4f} MHz"
        for i, percent in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            info[f"core_{i}"] = f"{percent}%"
        info["total"] = f"{psutil.cpu_percent()}%"

        return info
        # logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG)
        # for stat in self.stats: 
        #     newHandler = logging.FileHandler(filename=f"{self.path}/{stat}.log", encoding='utf-8', level=logging.DEBUG) 
        #     formatter = logging.Formatter("%(asctime)s "+" %(message)s", "%H:%M:%S")
        #     newHandler.setFormatter(formatter)
        #     self.logger.addHandler(newHandler)
if __name__ == "__main__":
    perf_tracker = PerformanceTracker()
    perf_tracker.start()