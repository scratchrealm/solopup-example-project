import os
import yaml
import json
from typing import List
import click


@click.command(help="Auto-generate index.md")
@click.argument('dirname')
def main(dirname: str):
    datasets_dirname = f'{dirname}/datasets'
    output_fname = f'{dirname}/index.md'

    markdown_lines: List[str] = []
    markdown_lines.append('# Datasets')
    folder_names = os.listdir(datasets_dirname)
    for folder_name in folder_names:
        ds_dirname = f'{datasets_dirname}/{folder_name}'
        if os.path.isdir(ds_dirname):
            print(f'======================')
            print(f'{folder_name}')
            config_fname = f'{ds_dirname}/config.yml'
            if os.path.exists(config_fname):
                with open(config_fname, 'r') as f:
                    config = yaml.safe_load(f)
                dataset_id = config['dataset_id']
                print(f'Dataset ID: {dataset_id}')
                markdown_lines.append('')
                markdown_lines.append(f'## {dataset_id}')
                gui_data_uri_fname = f'{ds_dirname}/gui_data.uri'
                if os.path.exists(gui_data_uri_fname):
                    with open (gui_data_uri_fname, 'r') as f:
                        gui_data_uri = f.read()
                else:
                    print('No gui_data.uri found')
                    gui_data_uri = None
                if gui_data_uri is not None:
                    vocalizations_gh_uri = f'gh://scratchrealm/solopup-example-project/main/datasets/{folder_name}/annotations.uri'
                    state = {'vocalizations': vocalizations_gh_uri}
                    state_json = json.dumps(state, separators=(',', ':'))
                    url = f'https://figurl.org/f?v=gs://figurl/neurostatslab-views-1dev6&d={gui_data_uri}&s={state_json}&label={dataset_id}'
                    markdown_lines.append('')
                    markdown_lines.append(f'[Open dataset for visualization and editing]({url})')
            else:
                print('No config.yml found')
    markdown_lines.append('')
    markdown_lines.append('---')
    markdown_lines.append('')
    markdown_lines.append('This file was auto-generated.')

    markdown = '\n'.join(markdown_lines)

    print(f'Writing {output_fname}')
    with open(output_fname, 'w') as f:
        f.write(markdown)

if __name__ == '__main__':
    main()