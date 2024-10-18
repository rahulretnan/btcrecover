#!/usr/bin/env python3

import locale
import os
import time
import logging

# Try to set the locale to C.UTF-8
try:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except locale.Error:
    # If C.UTF-8 is not available, try to use the default locale
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        # If setting the locale fails, we'll continue with the default
        pass

# Set environment variables
os.environ['LC_ALL'] = os.environ.get('LC_ALL', 'en_US.UTF-8')
os.environ['LANG'] = os.environ.get('LANG', 'en_US.UTF-8')

# seedrecover.py -- Bitcoin mnemonic sentence recovery tool
# Copyright (C) 2014-2017 Christopher Gurnee
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# If you find this program helpful, please consider a small
# donation to the developer at the following Bitcoin address:
#
#           3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4
#
#                      Thank You!

# PYTHON_ARGCOMPLETE_OK - enables optional bash tab completion

import compatibility_check

from btcrecover import btcrseed
import sys, multiprocessing
import concurrent.futures

# Configure logging
logging.basicConfig(filename='execution.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    start_time = time.time()  # Record the start time
    logging.info("Execution started")

    print()
    print("Starting", btcrseed.full_version())
    logging.info(f"Starting {btcrseed.full_version()}")

    btcrseed.register_autodetecting_wallets()
    mnemonic_sentence, path_coin = btcrseed.main(sys.argv[1:])

    result = ""
    if mnemonic_sentence:
        if not btcrseed.tk_root:  # if the GUI is not being used
            print("Seed found:", mnemonic_sentence)  # never dies from printing Unicode
            logging.info(f"Seed found: {mnemonic_sentence}")
            result = f"Seed found: {mnemonic_sentence}"

        # Save the mnemonic sentence to a file
        with open("seed.txt", "w", encoding="utf-8") as file:
            file.write(mnemonic_sentence)

        # print this if there's any chance of Unicode-related display issues
        if any(ord(c) > 126 for c in mnemonic_sentence):
            print("HTML Encoded Seed:", mnemonic_sentence.encode("ascii", "xmlcharrefreplace").decode())
            logging.info(f"HTML Encoded Seed: {mnemonic_sentence.encode('ascii', 'xmlcharrefreplace').decode()}")

        if btcrseed.tk_root:  # if the GUI is being used
            btcrseed.show_mnemonic_gui(mnemonic_sentence, path_coin)

        retval = 0

    elif mnemonic_sentence is None:
        retval = 1  # An error occurred or Ctrl-C was pressed inside btcrseed.main()
        logging.error("An error occurred or Ctrl-C was pressed inside btcrseed.main()")
        result = "An error occurred or Ctrl-C was pressed inside btcrseed.main()"

    else:
        retval = 0  # "Seed not found" has already been printed to the console in btcrseed.main()
        logging.info("Seed not found")
        result = "Seed not found"

    # Use all available CPU threads
    num_workers = multiprocessing.cpu_count()  # Set the number of workers to the number of CPU threads
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process.join, 1.0) for process in multiprocessing.active_children()]
        concurrent.futures.wait(futures)

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    logging.info(f"Total execution time: {total_time:.2f} seconds")

    # Create a report file
    with open("execution_report.txt", "w", encoding="utf-8") as report_file:
        report_file.write(f"Execution started: {time.ctime(start_time)}\n")
        report_file.write(f"Execution ended: {time.ctime(end_time)}\n")
        report_file.write(f"Total execution time: {total_time:.2f} seconds\n")
        report_file.write(f"Result: {result}\n")

    sys.exit(retval)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
