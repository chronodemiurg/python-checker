import requests
import csv
import threading
import time
import signal
from datetime import timedelta

WAIT_TIME_SECONDS = 1
status_url = []
check_urls = []

with open("testfiles/test-urls.csv", 'r') as file:
    csv_dict_reader = csv.DictReader(file)
    for row in csv_dict_reader:
        status_url.append(row['STATUS_URL'])
print(status_url)
with open("testfiles/test-urls.csv", 'r') as read_obj:
    csv_dict_reader = csv.DictReader(read_obj)
    for row in csv_dict_reader:
        check_urls.append(row['CHECK_URL'])
print(check_urls)


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


def checker():
    for value in check_urls:
        check = requests.get(value)
        if check.status_code != 200:
            check
            time.sleep(5)
        else:
            status = requests.get(status_url[0])
            print(status.status_code)
            print(value)
            time.sleep(5)


class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=checker)
    job.start()

    while True:
        try:
            time.sleep(5)
        except ProgramKilled:
            print
            "Program killed: running cleanup code"
            job.stop()
            break


time.sleep(10)
print('task successful')
