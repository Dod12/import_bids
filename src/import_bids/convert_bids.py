import os

import mne
import mne_bids
import pandas as pd
import yaml
from tqdm.auto import tqdm
import logging

from .setup_montage import setup_ideal_montage


def convert_bids(subject_id, raw_path, bids_path, task, line_freq, template_montage=None, dig_montage_path=None,
                 ch_names=None, ch_types=None, events_from_annotations=False, events_from_stim=False, event_id=None,
                 metadata=None, dry_run=False, overwrite=False):

    target_path = mne_bids.BIDSPath(root=bids_path, subject=subject_id, task=task)

    # Setup raw data
    raw_data = mne.io.read_raw(raw_path)
    raw_data.info["line_freq"] = line_freq

    if ch_names is not None:
        raw_data.rename_channels(ch_names)
    if ch_types is not None:
        raw_data.set_channel_types(ch_types)

    # Set channel types
    ch_types = dict()
    valid_channel_types = ["ecg", "eeg", "emg", "eog", "exci", "ias", "misc", "resp",
                           "seeg", "dbs", "stim", "syst", "ecog", "hbo", "hbr"]
    for ch_name in raw_data.ch_names:
        for ch_type in valid_channel_types:
            if ch_type in ch_name.lower():
                ch_types[ch_name] = ch_type
                break
            elif ch_name.lower() == "trigger":
                ch_types[ch_name] = "stim"
                break
    raw_data.set_channel_types(ch_types)

    # Set the correct montage
    if template_montage is not None:
        montage=template_montage
        raw_data.set_montage(template_montage)
    elif dig_montage_path is not None:
        montage = mne.channels.read_custom_montage(dig_montage_path)
        raw_data.set_dig_montage(montage)
    else:
        montage = None

    # Get events
    if events_from_annotations is not None:
        if event_id is not None:
            # Rename annotations according to the annotations dictionary
            annotations = raw_data.annotations.copy()
            descriptions = annotations.to_data_frame()["description"]
            for new, old in event_id.items():
                descriptions = descriptions.replace(str(old), new)
            annotations.description = descriptions.to_numpy()
            raw_data.set_annotations(annotations)
            events, event_id = mne.events_from_annotations(raw_data, event_id=event_id)
        else:
            events, event_id = mne.events_from_annotations(raw_data, event_id="auto")
    elif events_from_stim is not None:
        events = mne.find_events(raw_data)
    else:
        events = None

    if not dry_run:
        mne_bids.write_raw_bids(raw_data, target_path, events, event_id, montage=raw_data.get_montage(), overwrite=overwrite)
        if metadata is not None:
            logging.debug(metadata)
            metadata.to_csv(os.path.join(target_path.directory, "metadata.tsv"), sep="\t")


def convert_raws(args):

    raw_dir = args.raw_dir
    bids_dir = args.bids_dir
    task = args.task

    # Setup idealized montage if provided
    if args.dig_dir:
        montage = None
        montage_dir = {os.path.basename(filename).split(".")[0]: os.path.join(raw_dir, filename)
                       for filename in os.listdir(args.dig_dir) if not filename.startswith(".")}
    elif args.montage or args.template or args.location:
        montage = setup_ideal_montage(args.montage, args.template, args.location)
        montage_dir = None
    else:
        montage = None
        montage_dir = None

    if args.channel_names is not None:
        with open(args.channel_names, "r") as f:
            mappings = yaml.safe_load(f)
        ch_names = mappings["ch_names"]
        ch_types = mappings["ch_types"]
    else:
        ch_names = None
        ch_types = None

    # Load some constants from args
    events_from_annotations = args.annotations
    events_from_stim = args.stim

    if args.event_id is not None:
        with open(args.event_id, "r") as f:
            event_id = yaml.safe_load(f)

    if args.metadata is not None:
        metadata = pd.read_csv(args.metadata, sep="\t", header=0, index_col=0)
    else:
        metadata = None
    line_freq = args.line_freq
    verbose = args.verbose
    dry_run = args.dry_run
    overwrite = args.overwrite
    progress = args.progress
    if args.n_parallel != 1:
        logging.warning("--n_parallel is not implemented yet. Using single-threaded parallelism.")

    subject_files = [(os.path.join(raw_dir, filename), os.path.basename(filename).split(".")[0])
                     for filename in os.listdir(raw_dir) if not filename.startswith(".")]

    for raw_path, subject_id in tqdm(subject_files, disable=not progress):
        if verbose:
            print(subject_id)

        if montage_dir is not None:
            montage_path = montage_dir[subject_id]
        else:
            montage_path = None

        if metadata is not None:
            logging.debug(metadata)
            metadata = metadata[metadata["Subject"] == int(subject_id)]

        convert_bids(subject_id, raw_path, bids_dir, task, line_freq, montage, montage_path, ch_names, ch_types,
                     events_from_annotations, events_from_stim, event_id, metadata, dry_run, overwrite)
