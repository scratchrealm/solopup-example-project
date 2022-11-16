import os
import yaml
import click
import json
import h5py
import numpy as np
from create_spectrograms import _find_singular_file_in_dir


@click.command(help="Initializes a dataset by creating or updating a config.yml file")
@click.argument('dirname')
def init_dataset(dirname: str):    
    h5_fname = _find_singular_file_in_dir(dirname, '.h5')
    print(f'USING H5: {h5_fname}')

    audio_sr_hz = _get_audio_sr_from_h5(h5_fname)
    print(f'Audio sampling rate (Hz): {audio_sr_hz}')

    # get first channel in order to compute duration
    print('Determining duration')
    with h5py.File(h5_fname, 'r') as f:
        ch1 = np.array(f['ai_channels/ai0'])
    duration_sec = len(ch1) / audio_sr_hz
    print(f'Audio duration (sec): {duration_sec}')

    print('Creating or updating config.yml')
    config_fname = f'{dirname}/config.yml'
    if os.path.exists(config_fname):
        with open(config_fname, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}    
    config['dataset_id'] = os.path.basename(dirname)
    config['audio_sr_hz'] = audio_sr_hz
    config['duration_sec'] = duration_sec

    with open(f'{dirname}/config.yml', 'w') as f:
        yaml.dump(config, f)

def _get_audio_sr_from_h5(h5_file: str):
    with h5py.File(h5_file, 'r') as f:
        d = json.loads(f['config'][()].decode('utf-8'))
        audio_sr_hz = d['microphone_sample_rate']
    return audio_sr_hz

if __name__ == '__main__':
    init_dataset()
