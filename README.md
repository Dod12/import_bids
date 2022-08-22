# Import BIDS

Simple CLI for importing EEG data to BIDS format.

## Installation

Clone the repo and run pip install on the root directory.

## Usage

```
usage: import-bids [-h] [--eog EOG CONFIG FILE] [--ref EOG CONFIG FILE]
                   [-m MONTAGE NAME | -t MONTAGE PATH | -d MONTAGE DIRECTORY | -l ELEC PATH] [-c CHANNEL NAME PATH]
                   [-a | -s CHANNEL NAME] [-e EVENT ID PATH] [-M METADATA PATH] [-f LINE FREQUENCY] [-v] [-vv]
                   [--dry-run] [-o] [-P] [-n N CPUS]
                   raw_dir bids_dir task

Tool to import EEG files to the BIDS data format.

positional arguments:
  raw_dir               Directory containing the raw data
  bids_dir              Output directory for the BIDS dataset
  task                  Task name in the run.

optional arguments:
  -h, --help            show this help message and exit
  --eog EOG CONFIG FILE
                        Path to EOG configuration file
  --ref EOG CONFIG FILE
                        Path to reference configuration file
  -m MONTAGE NAME, --montage MONTAGE NAME
                        Name of standard montage to use. Template will be loaded from MNE.
  -t MONTAGE PATH, --template MONTAGE PATH
                        Path to template file to load.
  -d MONTAGE DIRECTORY, --dig_dir MONTAGE DIRECTORY
                        Directory for subject digitization files.
  -l ELEC PATH, --location ELEC PATH
                        FieldTrip .elec file specifying electrode positions.
  -c CHANNEL NAME PATH, --channel_names CHANNEL NAME PATH
                        Path to file containing mapping between channel names and standard 1020 names.
  -a, --annotations     Get event times from annotations.
  -s CHANNEL NAME, --stim CHANNEL NAME
                        Get events from stimulus channel.
  -e EVENT ID PATH, --event_id EVENT ID PATH
                        Get event names from file mapping trigger values to event names. Must be a .tsv file with
                        trigger number in first column and event name in the second column.
  -M METADATA PATH, --metadata METADATA PATH
                        Path to metadata file. Must be a .tsv file with length equal to the number of events and the
                        subject id in the first column.
  -f LINE FREQUENCY, --line_freq LINE FREQUENCY
                        Line frequency for powerline noise. Defaults to 50.0 Hz.
  -v, --verbose         Verbose output. Equivalent to MNE log-level 'INFO'.
  -vv, --debug          Debug output. Equivalent to MNE log-level 'DEBUG'.
  --dry-run             Do not save the results
  -o, --overwrite       Overwrite existing files.
  -P, --progress        No not display progressbar.
  -n N CPUS, --n_parallel N CPUS
                        Number of parallel processes. Defaults to 1.
```
