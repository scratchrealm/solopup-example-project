import os
import yaml
import click
import kachery_cloud as kcl
from create_spectrograms import _find_singular_file_in_dir
import cv2


@click.command(help="Upload .ogv file to kachery and populate the relevant field in config.yml")
@click.argument('dirname')
def upload_video(dirname: str):    
    ogv_fname = _find_singular_file_in_dir(dirname, '.ogv')
    print(f'USING VIDEO: {ogv_fname}')

    vid = cv2.VideoCapture(ogv_fname)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = vid.get(cv2.CAP_PROP_FPS)
    print(f'height/width: {height}/{width}')
    print(f'fps: {fps}')

    print('Uploading')
    uri = kcl.store_file(ogv_fname, label=os.path.basename(ogv_fname))

    print('Updating video_uri, video_dims, and video_sr_hz in config.yml')
    with open(f'{dirname}/config.yml', 'r') as f:
        config = yaml.safe_load(f)
    config['video_uri'] = uri
    config['video_dims'] = [height, width]
    config['video_sr_hz'] = fps

    with open(f'{dirname}/config.yml', 'w') as f:
        yaml.dump(config, f)

if __name__ == '__main__':
    upload_video()
