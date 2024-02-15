class Timer:
    def __init__(self, func, args=None):
        self._start_time = None
        self.func = func
        self.args = args
        
        self.total_time = 0
        self.iterations = 0
        self.all_times = []
    
    def start(self):
        if self._start_time is not None:
            raise Exception("Timer is running. Use .stop().")

        if self.args is None:
            self._start_time = self.func()
        else:
            self._start_time = self.func(self.args)
            
    def stop(self):
        if self._start_time is None:
            raise Exception("Timer is not ruuning. Use .start().")
        
        if self.args is None:
            elapsed_time = self.func() - self._start_time
        else:
            elapsed_time = self.func(self.args) - self._start_time
        
        self._start_time = None
        self.iterations += 1
        self.total_time += elapsed_time
        self.all_times.append(elapsed_time)
    
    def average(self):
        if self.iterations == 0:
            return None
        return self.total_time / self.iterations
    
    def reset(self):
        self._start_time = None
        self.iterations = 0
        self.total_time = 0
        self.all_times = []
        
    def __repr__(self):
        name = self.func.__name__
        return f'Timer : {name} | iterations: {self.iterations} | total_elapsed_time: {self.total_time} | average_elapsed_time: {self.average()}'