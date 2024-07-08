# opti_fit

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/RichardOberdieck/opti_fit/automatic_checks.yaml?branch=main) ![GitHub License](https://img.shields.io/github/license/RichardOberdieck/opti_fit)


Scripts and data related to the finding of optimal thresholds for string matching. The full docs can be found [here](https://richardoberdieck.github.io/opti_fit/).

## How to run it
The code uses [hatch](https://hatch.pypa.io/) as a project manager, with the `pyproject.toml` file for configuration. There are four command-line scripts that are defined to run the analysis:

- `hatch run simple`: Solves the simple hit, payment or combined models
- `hatch run relaxed`: Solves the relaxed hit or payment model
- `hatch run combination`: Solve the algorithm combination model
- `hatch run compare`: Compares the different solvers

To get started, install `hatch` and run one of the commands, e.g.:

```
hatch run simple
```

This will execute the [run_simple_model.py](./opti_fit/run_simple_model.py) script that picks a model, a dataset and solves it with the default settings. If you would like to specify the details, you can pass them as arguments, e.g.:

```
hatch run simple --model_type='hit' --full_dataset=False --to_file=True
```

For more information, please check the help, e.g.:

```
hatch run simple --help
```

If you would like to run all the experiments as they appear in the [Results](https://richardoberdieck.github.io/opti_fit/results/) section of the docs, you can run:

```
runs.sh
```

## How to contribute

We highly welcome contributions, please simply make a pull request and we will review as quickly as possible.
