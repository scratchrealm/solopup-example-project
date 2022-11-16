# solopup-example-project

This is an example project.

See this [auto generated index of datasets](./index.md).

## Adding a dataset

Assume the ID of the dataset is `dataset1`

Create a new dataset directory `datasets/dataset1` and copy a .h5 audio file and a .avi video file into the directory.

---

Initialize the dataset using the following command from the root directory of the project

```bash
python scripts/init_dataset.py datasets/dataset1
```

This will create a `config.yml` file in the dataset directory including some meta information obtained from the .h5 file.

---

Create a .ogv video file in the directory using the following command (fill in `<filename>`).

```bash
cd datasets/dataset1
ffmpeg -i <filename>.avi -c:v libtheora -q:v 7 -c:a libvorbis -q:a 4 <filename>.ogv
```

If you encounter encoder errors with your version of ffmpeg, you can use singularity and instead run

```bash
# on the flatiron cluster, run "module load singularity"
singularity exec docker://jrottenberg/ffmpeg singularity ffmpeg -i <filename>.avi -c:v libtheora -q:v 7 -c:a libvorbis -q:a 4 <filename>.ogv
```

---

Store the .ogv video file in kachery and update `config.yml` for the dataset using the following command from the project root directory

```bash
python scripts/upload_video.py datasets/dataset1
```

This will upload the file and update `config.yml` with meta information associated with the video.

---

Create a `spectrograms.pkl` file

```bash
python scripts/create_spectrograms.py datasets/dataset1
```

---

Auto-detect the vocalization intervals

```bash
python scripts/auto_detect_vocalizations.py datasets/dataset1
```

---

Create the data for the figurl GUI

```bash
python scripts/create_gui_data.py datasets/dataset1
```

---

Add the name of the dataset directory to the list in the config.yml at the root of a project

---

Finally, update the index.md file (see below) and add/commit/push the new files to Github.

## Updating the auto-generated index

To auto-generate index.md based on the datasets listed in `config.yml` and the contents of `datasets/`, run

```bash
python scripts/generate_index_md.py .
```

Then add/commit/push the new files to Github.
