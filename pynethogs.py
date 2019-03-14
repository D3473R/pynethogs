import os
import sys
import signal
import ctypes

LIBNETHOGS_VERSION = "0.8.5-54-gac5af1d"

NETHOGS_APP_ACTION_SET = 1
NETHOGS_APP_ACTION_REMOVE = 2


class NethogsMonitorRecord(ctypes.Structure):
    _fields_ = [
        ('record_id', ctypes.c_int), 
        ('name', ctypes.c_char_p), 
        ('pid', ctypes.c_int), 
        ('uid', ctypes.c_uint), 
        ('device_name', ctypes.c_char_p),
        ('sent_bytes', ctypes.c_ulonglong),
        ('recv_bytes', ctypes.c_ulonglong),
        ('sent_kbs', ctypes.c_float),
        ('recv_kbs', ctypes.c_float)]

    def __repr__(self):
        return 'record_id: {0}, name: {1}, pid: {2}, uid: {3}, device_name: {4}, sent_bytes: {5}, recv_bytes: {6}, sent_kbs: {7}, recv_kbs: {8}'.format(
            self.record_id, self.name, self.pid, self.uid, self.device_name, self.sent_bytes, self.recv_bytes, self.sent_kbs, self.recv_kbs)


def signal_handler(signal, frame):
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    libnethogs =  ctypes.CDLL("lib/libnethogs.so.%s" % LIBNETHOGS_VERSION)

    @ctypes.CFUNCTYPE(None, ctypes.c_int, NethogsMonitorRecord)
    def callback(action, update):
        print(update)

    libnethogs.nethogsmonitor_loop(callback, None)
    libnethogs.nethogsmonitor_breakloop()


if __name__ == '__main__':
    if os.getuid() != 0:
        print('This has to be run as root sorry :/')
    else:
        main()