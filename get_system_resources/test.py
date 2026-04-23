import pynvml

pynvml.nvmlInit()

count = pynvml.nvmlDeviceGetCount()
print("GPU COUNT:", count)
