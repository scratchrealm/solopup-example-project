from typing import List
import os
import yaml
import h5py
import numpy as np
from matplotlib.pyplot import specgram
import pickle


def main():
    dirname = '.'
    with open(f'{dirname}/config.yml', 'r') as f:
        config = yaml.safe_load(f)
    print('USING CONFIG')
    print(config)

    duration_sec = config['duration_sec']
    audio_sr_hz = config['audio_sr_hz']
    
    h5_fname = _find_singular_file_in_dir(dirname, '.h5')
    print(f'USING H5: {h5_fname}')

    print('Extracting audio signals')
    with h5py.File(h5_fname, 'r') as f:
        ch1 = np.array(f['ai_channels/ai0'])
        ch2 = np.array(f['ai_channels/ai1'])
        ch3 = np.array(f['ai_channels/ai2'])
        ch4 = np.array(f['ai_channels/ai3'])
        X = np.stack([ch1, ch2, ch3, ch4]).T

        # crop to duration
        X = X[0:int(duration_sec * audio_sr_hz)]

        num_channels = X.shape[1]

    print('Computing spectrograms')
    spectrograms = []
    for channel_ind in range(num_channels):
        s, f, t, im = specgram(X[:, channel_ind], NFFT=512, noverlap=256, Fs=audio_sr_hz)
        sr_spectrogram = 1 / (t[1] - t[0])
        spectrograms.append(s)
    print(f'Spectrogram sampling rate (Hz): {sr_spectrogram}')
    spectrogram_for_gui = sum(spectrograms)

    print('Auto detecting maxval')
    maxval = _auto_detect_spectrogram_maxval(spectrogram_for_gui, sr_spectrogram=sr_spectrogram)
    minval = 0
    print(f'Absolute spectrogram max: {np.max(spectrogram_for_gui)}')
    print(f'Auto detected spectrogram max: {maxval}')

    print('Scaling spectogram data')
    # Nf x Nt
    spectrogram_for_gui = np.floor((spectrogram_for_gui - minval) / (maxval - minval) * 255).astype(np.uint8)

    output_fname = f'{dirname}/spectrograms.pkl'
    print(f'Writing {output_fname}')
    with open(output_fname, 'wb') as fb:
        pickle.dump({
            'spectrograms': spectrograms,
            'f': f,
            't': t,
            'spectrogram_for_gui': spectrogram_for_gui
        }, fb)

def _auto_detect_spectrogram_maxval(spectrogram: np.array, *, sr_spectrogram: float):
    Nf = spectrogram.shape[0]
    Nt = spectrogram.shape[1]
    chunk_num_samples = int(15 * sr_spectrogram)
    chunk_maxvals: List[float] = []
    i = 0
    while i + chunk_num_samples < Nt:
        chunk = spectrogram[:, i:i + chunk_num_samples]
        chunk_maxvals.append(np.max(chunk))
        i += chunk_num_samples
    v = np.median(chunk_maxvals)
    return v

def _find_singular_file_in_dir(dirname: str, extension: str):
    fnames = os.listdir(dirname)
    f_fnames = [f for f in fnames if f.endswith(extension)]
    if len(f_fnames) == 0:
        raise Exception(f'No {extension} file found in directory: {dirname}')
    if len(f_fnames) > 1:
        raise Exception(f'More than one {extension} file found in directory: {dirname}')
    return f'{dirname}/{f_fnames[0]}'

if __name__ == '__main__':
    main()
