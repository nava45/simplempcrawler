import csv
import requests
import sys
import multiprocessing
import datetime
import re

from BeautifulSoup import BeautifulSoup


def parse_html(page):
    '''
    Parse the html page whether jquery.js available or not
    returns bool type
    '''
    soup = BeautifulSoup(page)
    for i in soup.findAll("script"):
        _src = i.get("src", "")
        if 'jquery.js' in _src:
            return True
    return False
    

def process_record(url):
    '''
    Process the given url which works with parser also
    '''
    html_page = requests.get(url).content
    is_valid_page =  parse_html(html_page)
    return is_valid_page


def worker_logic(doc_q, stdout_lock, afd, rfd):
    '''
    Worker process business logic handler
    queue, lock, success file descriptor, failure file des passed as input
    '''
    while True:
        url = doc_q.get()
        is_valid_page = process_record(url)
        with stdout_lock:
            if is_valid_page:
                print('Accepted:', url)
                afd.writelines(url+"\n")
                afd.flush()
            else:
                print('Rejected:', url)
                rfd.writelines(url+"\n")
                rfd.flush()
        doc_q.task_done()


# Multprocessing crawler module
class SMProcess(object):

    def __init__(self):
       
        self.count = 0
        self.start = datetime.datetime.now()

        sys.stderr.write("Will spawn %s workers.\n" % multiprocessing.cpu_count())
        self.doc_q = multiprocessing.JoinableQueue(100)
        self.stdout_lock = multiprocessing.Lock()
        self.input_fd = open('urls.csv')
        self.accept_fd = open('accepted.csv', 'wb')
        self.reject_fd = open('rejected.csv', 'wb')

        self.workers = []
        for _ in range(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=worker_logic, 
                                        args=(self.doc_q, self.stdout_lock, 
                                              self.accept_fd, self.reject_fd))
            p.start()
            self.workers.append(p)

        try:
            self.run()
        finally:
            sys.stderr.write("Terminating workers...")
            for i, worker in enumerate(self.workers):
                try:
                    worker.terminate()
                except Exception:
                    sys.stderr.write("Unable to terminate worker %s !" % i)

    def run(self):
        cin = csv.reader(self.input_fd)

        for line in cin:
            line = line[0]
            sys.stderr.write('Retrieving %s.\n' % line)
            self.distribute(line)
            sys.stderr.write('%s documents parsed. %s doc/s.\n' % (self.count, self.count // (datetime.datetime.now() - self.start).total_seconds()))

        # Wait for all the workers
        self.doc_q.join()

    def distribute(self, line):
        '''
        '''
        self.doc_q.put(line)
        self.count += 1


if __name__ == '__main__':
    SMProcess()
