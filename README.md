# opti_fit
Scripts and data related to the finding of optimal thresholds for string matching. The full docs can be found [here](https://richardoberdieck.github.io/opti_fit/).

## How to run it
The code uses [hatch](https://hatch.pypa.io/) as a project manager, with the `pyproject.toml` file for configuration. To get started, install hatch and then run:

```
hatch run solve
```

This will execute the [main](./opti_fit/main.py) script that picks a model, a dataset and solves it with the default settings. If you would like to specify the details, you can pass them as arguments, e.g.:

```
hatch run solve --model='simple_hit_mip' --full_dataset=False --mps_filename='test.mps'
```
