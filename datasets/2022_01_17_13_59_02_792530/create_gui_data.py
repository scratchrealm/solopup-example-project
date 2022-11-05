import kachery_cloud as kcl
import yaml
import pickle
import numpy as np
from figurl.core.serialize_wrapper import _serialize


def main():
    dirname = '.'
    with open(f'{dirname}/config.yml', 'r') as f:
        config = yaml.safe_load(f)
    print('USING CONFIG')
    print(config)

    if 'video_uri' not in config:
        raise Exception('No video_uri in config')
    video_uri = config['video_uri']
    video_sr_hz = config['video_sr_hz']
    video_dims = config['video_dims']
    print(f'Video: {video_uri}')
    print(f'Video sampling rate (Hz): {video_sr_hz}')
    print(f'Video dims: {video_dims}')

    output_fname = f'{dirname}/gui_data.uri'

    spectrograms_fname = f'{dirname}/spectrograms.pkl'
    print(f'Loading {spectrograms_fname}')
    with open(spectrograms_fname, 'rb') as f:
        a = pickle.load(f)
    spectrogram_for_data: np.ndarray = a['spectrogram_for_gui']
    t: np.ndarray = a['t']
    sr_spectrogram = 1 / (t[1] - t[0])

    print(f'Spectrogram sampling rate (Hz): {sr_spectrogram}')

    print('Assembling data')
    data = {
        'type': 'neurostatslab.AnnotateVocalizations',
        'spectrogram': {
            'data': spectrogram_for_data.T,
            'samplingFrequency': sr_spectrogram
        },
        'video': {
            'uri': video_uri,
            'samplingFrequency': video_sr_hz,
            'width': video_dims[1],
            'height': video_dims[0]
        }
    }

    print('Storing data in kachery')
    gui_data_uri = kcl.store_json(_serialize(data, compress_npy=True))

    print(f'Writing {output_fname}')
    with open(output_fname, 'w') as f:
        f.write(gui_data_uri)

if __name__ == '__main__':
    main()