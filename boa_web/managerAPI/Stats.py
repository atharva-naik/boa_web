class EngagementTracker:
    pass


class PerformanceTracker:
    import os
    import logging
    def __init__(self, path='stats'):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.stats = {"battery":0, "network":1, "cpu":2, "gpu":3, "keyboard":4, "default":5}
        self.funcs = {k:exec(f"self.{k}_stats") for k in self.stats}
        self.logger = logging.getLogger()
        for stat in self.stats: 
            newHandler = logging.FileHandler(filename=f"{self.path}/{stat}.log", encoding='utf-8', level=logging.DEBUG) 
            formatter = logging.Formatter("%(asctime)s "+" %(message)s", "%H:%M:%S")
            newHandler.setFormatter(formatter)
            self.logger.addHandler(newHandler)
        
    def start(self):
        '''start logging stuff'''
        # use non blocking scheduling here 
        self.log()

    def log(self):
        '''log all relevant stats for the current timestep'''
        for stat in self.stats: 
            self.log_stats(stat)

    def log_stats(self, stat="cpu"):
        '''call each log function. It is a separate function to allow finer level of  control.'''
        i = self.stats.get(stat,-1)
        handler = self.logger.handlers[i]
        self.funcs[stat](handler)

    def cpu_stats(self, handler):
        pass

    def gpu_stats(self, handler):
        pass

    def battery_stats(self, handler):
        pass

    def network_stats(self, handler):
        pass

    def keyboard_stats(self, handler):
        pass