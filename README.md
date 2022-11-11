# solopup-example-project

This is an example project.

See this [auto generated index of datasets](./index.md).

## Adding a dataset

Assume the ID of the dataset is `dataset1`

Create a new dataset directory `datasets/dataset1` and copy a .h5 audio file and a .avi video file into the directory.

Create a .ogv video file in the directory using the following command (fill in `<filename>`).

```bash
cd datasets/dataset1
ffmpeg -i <filename>.avi -c:v libtheora -q:v 7 -c:a libvorbis -q:a 4 <filename>.ogv
```

Store the .ogv video file in kachery using the following command (fill in `<filename>`) and make a note of the kachery URI.

```bash
kachery-cloud-store <filename>.ogv
```

Create a new `config.yml` file in the directory and set the appropriate fields using the config file for one of the existing datasets as a template.

Create a `spectrograms.pkl` file

```bash
python scripts/create_spectrograms.py datasets/dataset1
```

Auto-detect the vocalization intervals

```bash
python scripts/auto_detect_vocalizations.py datasets/dataset1
```

Create the data for the figurl GUI

```bash
python scripts/create_gui_data.py datasets/dataset1
```

Finally, update the index.md file (see below) and add/commit/push the new files to Github.

## Updating the auto-generated index

To auto-generate index.md based on the contents of `datasets/`, fill in the fields of `config.yml` and then run

```bash
python scripts/generate_index_md.py .
```

Then add/commit/push the new files to Github.