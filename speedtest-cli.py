#!/usr/bin/env python
from __future__ import print_function
import sys
import urllib2
import argparse
import time

__author__ = "Giorgio Crivellari <miticojo@gmail.com>"
__version__ = "1.0"


def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')
   sys.stdout.flush()

def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return bytes_so_far

def start_test(url):
    try:
        response = urllib2.urlopen(url)
        return chunk_read(response, report_hook=chunk_report)
    except Exception, ex:
        print("Download ERROR: \n", ex.message, file=sys.stderr)
        sys.exit(2)

def main():
    if len(sys.argv) == 1:
        print("Help: \n",
              "This script execute a download speed test of passed file.\n" \
              "Usage: speedtest-cli -f <test-file-url>" \
              "Version: %s" % __version__,
              file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--url-file", help="url of file used for test")
    args = parser.parse_args()
    start_time = time.time()
    size = start_test(args.url_file)
    elapsed_time = int(time.time() - start_time)
    print("Download complete in %d seconds (%d KB/s)" % (elapsed_time, (size/elapsed_time)/1000))


if __name__ == "__main__":
    main()