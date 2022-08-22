#!python

import argparse
import os
import logging

from mne import set_log_level
from .convert_bids import convert_raws


parser = argparse.ArgumentParser("import-bids", description="Tool to import EEG files to the BIDS data format.")

# Input and output dirs
parser.add_argument('raw_dir', metavar="raw_dir", type=os.path.abspath, help="Directory containing the raw data")
parser.add_argument('bids_dir', metavar="bids_dir", type=os.path.abspath,
                    help="Output directory for the BIDS dataset")

parser.add_argument('task', type=str, help="Task name in the run.")

parser.add_argument('--eog', metavar="EOG CONFIG FILE", type=os.path.abspath, action="store",
                    help="Path to EOG configuration file")

parser.add_argument('--ref', metavar="EOG CONFIG FILE", type=os.path.abspath, action="store",
                    help="Path to reference configuration file")

# We need to handle template and scanned dig montages separately
montage_parser = parser.add_mutually_exclusive_group(required=False)
montage_parser.add_argument('-m', '--montage', metavar="MONTAGE NAME", type=str, action='store',
                            help="Name of standard montage to use. Template will be loaded from MNE.")
montage_parser.add_argument('-t', '--template', metavar="MONTAGE PATH", type=os.path.abspath, action='store',
                            help="Path to template file to load.")
montage_parser.add_argument('-d', '--dig_dir', metavar="MONTAGE DIRECTORY", type=os.path.abspath, action='store',
                            help="Directory for subject digitization files.")
montage_parser.add_argument('-l', '--location', metavar="ELEC PATH", type=os.path.abspath, action='store',
                            help="FieldTrip .elec file specifying electrode positions.")
parser.add_argument('-c', '--channel_names', metavar="CHANNEL NAME PATH", type=os.path.abspath, action='store',
                    help="Path to file containing mapping between channel names and standard 1020 names.")

# Event handling
event_parser = parser.add_mutually_exclusive_group(required=False)
event_parser.add_argument('-a', '--annotations', action="store_true", default=True,
                          help="Get event times from annotations.")
event_parser.add_argument('-s', '--stim', metavar="CHANNEL NAME", type=str, action="store",
                          help="Get events from stimulus channel.")
parser.add_argument('-e', '--event_id', metavar="EVENT ID PATH", type=os.path.abspath, action="store",
                    help="Get event names from file mapping trigger values to event names. Must be a .tsv file with"
                         " trigger number in first column and event name in the second column.")

# Metadata about all subjects
parser.add_argument('-M', '--metadata', metavar="METADATA PATH", type=os.path.abspath, action="store",
                    help="Path to metadata file. Must be a .tsv file with length equal to the number of events"
                         " and the subject id in the first column.")
parser.add_argument('-f', '--line_freq', metavar="LINE FREQUENCY", type=float, default=50.0,
                    help="Line frequency for powerline noise. Defaults to 50.0 Hz.")

parser.add_argument('-v', '--verbose', action="store_true", default=False,
                    help="Verbose output. Equivalent to MNE log-level 'INFO'.")
parser.add_argument('-vv', '--debug', action="store_true", default=False,
                    help="Debug output. Equivalent to MNE log-level 'DEBUG'.")
parser.add_argument('--dry-run', action="store_true", default=False, help="Do not save the results")
parser.add_argument('-o', '--overwrite', action="store_true", default=False, help="Overwrite existing files.")
parser.add_argument('-P', '--progress', action="store_true", default=True, help="No not display progressbar.")
parser.add_argument('-n', '--n_parallel', metavar="N CPUS", action="store", type=int, default=1,
                    help="Number of parallel processes. Defaults to 1.")


def main(*args):
    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        set_log_level("DEBUG")
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
        set_log_level("INFO")
    else:
        logging.basicConfig(level=logging.WARNING)
        set_log_level("WARNING")
    convert_raws(args)
