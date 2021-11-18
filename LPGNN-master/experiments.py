import os.path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from itertools import product
from collections.abc import Iterable

from random import sample
import numpy as np
import pandas as pd
from utils import print_args, JobManager


class HyperParams:
    def __init__(self, path_dir):
        try:
            self.df_lwd = pd.read_csv(
                os.path.join(path_dir, 'lwd.csv'), index_col=['dataset', 'feature', 'x_eps', 'y_eps']
            )
        except FileNotFoundError:
            self.df_lwd = None

        try:
            self.df_steps = pd.read_csv(os.path.join(path_dir, 'steps.csv'), index_col=['dataset', 'x_eps', 'y_eps'])
        except FileNotFoundError:
            self.df_steps = None

    def get(self, dataset, feature, x_eps, y_eps):
        hparams = self.get_lwd(dataset=dataset, feature=feature, x_eps=x_eps, y_eps=y_eps)
        hparams.update(self.get_steps(dataset=dataset, x_eps=x_eps, y_eps=y_eps))
        return hparams

    def get_lwd(self, dataset, feature, x_eps, y_eps):
        params = {}
        if self.df_lwd is not None:
            if feature == '1rnd': feature = 'rnd'
            x_eps = np.inf if np.isinf(x_eps) else 1
            y_eps = np.inf if np.isinf(y_eps) else 1
            params = self.df_lwd.loc[dataset, feature, x_eps, y_eps].to_dict()

        return params

    def get_steps(self, dataset, x_eps, y_eps):
        params = {}
        if self.df_steps is not None:
            params = self.df_steps.loc[dataset, x_eps, y_eps].to_dict()

        return params


class CommandBuilder:
    BEST_VALUE = None

    def __init__(self, args, hparams_dir=None, random=None):
        self.random = random
        self.default_options = f" -s {args.seed} -r {args.repeats} -o {args.output_dir} "
        if args.project:
            self.default_options += f" --log --log-mode collective --project-name {args.project} "
        self.hparams = HyperParams(path_dir=hparams_dir) if hparams_dir else None

    def build(self, dataset, feature, mechanism, model, x_eps, y_eps, forward_correction,
              x_steps, y_steps, learning_rate, weight_decay, dropout):

        cmd_list = []
        configs = self.product_dict(
            dataset=self.get_list(dataset),
            feature=self.get_list(feature),
            mechanism=self.get_list(mechanism),
            model=self.get_list(model),
            x_eps=self.get_list(x_eps),
            y_eps=self.get_list(y_eps),
            forward_correction=self.get_list(forward_correction),
            x_steps=self.get_list(x_steps),
            y_steps=self.get_list(y_steps),
            learning_rate=self.get_list(learning_rate),
            weight_decay=self.get_list(weight_decay),
            dropout=self.get_list(dropout),
        )

        if self.random:
            configs = sample(list(configs), self.random)

        for config in configs:
            config = self.fill_best_params(config)
            options = ' '.join([f' --{param} {value} ' for param, value in config.items()])
            command = f'python main.py {options} {self.default_options}'
            cmd_list.append(command)

        return cmd_list

    def fill_best_params(self, config):
        if self.hparams:
            best_params = self.hparams.get(
                dataset=config['dataset'],
                feature=config['feature'],
                x_eps=config['x_eps'],
                y_eps=config['y_eps'],
            )

            for param, value in config.items():
                if value == self.BEST_VALUE:
                    config[param] = best_params[param]
        return config

    @staticmethod
    def get_list(param):
        if not isinstance(param, Iterable) or isinstance(param, str):
            param = [param]
        return param

    @staticmethod
    def product_dict(**kwargs):
        keys = kwargs.keys()
        vals = kwargs.values()
        for instance in product(*vals):
            yield dict(zip(keys, instance))


def hyperopt(args):
    run_cmds = []
    cmdbuilder = CommandBuilder(args=args)
    datasets = ['cora', 'pubmed', 'facebook', 'lastfm']
    x_eps_list = [1, np.inf]
    y_eps_list = [1, np.inf]
    x_steps = {'cora': 16, 'pubmed': 16, 'facebook': 4, 'lastfm': 8}
    y_steps = {'cora': 8, 'pubmed': 2, 'facebook': 2, 'lastfm': 2}

    # LPGNN
    for dataset, x_eps, y_eps in product(datasets, x_eps_list, y_eps_list):
        run_cmds += cmdbuilder.build(
            dataset=dataset,
            feature='raw',
            mechanism='mbm',
            model='sage',
            x_eps=x_eps,
            x_steps=0 if np.isinf(x_eps) else x_steps[dataset],
            y_eps=y_eps,
            y_steps=0 if np.isinf(y_eps) else y_steps[dataset],
            forward_correction=True,
            learning_rate=[0.01, 0.001, 0.0001],
            weight_decay=[0.01, 0.001, 0.0001, 0],
            dropout=[0, 0.25, 0.5, 0.75]
        )


    # fully-private baselines
    for dataset, y_eps in product(datasets, y_eps_list):
        run_cmds += cmdbuilder.build(
            dataset=dataset,
            feature=['rnd', 'one', 'ohd'],
            mechanism='mbm',
            model='sage',
            x_eps=np.inf,
            x_steps=0,
            y_eps=y_eps,
            y_steps=0 if np.isinf(y_eps) else y_steps[dataset],
            forward_correction=True,
            learning_rate=[0.01, 0.001, 0.0001],
            weight_decay=[0.01, 0.001, 0.0001, 0],
            dropout=[0, 0.25, 0.5, 0.75]
        )

    run_cmds = list(set(run_cmds))  # remove duplicate runs
    return run_cmds


def experiment_lpgnn(args):
    run_cmds = []
    cmdbuilder = CommandBuilder(args=args, hparams_dir='./hparams')
    datasets = ['cora', 'pubmed', 'facebook', 'lastfm']

    ## LPGNN ALL CASES
    run_cmds += cmdbuilder.build(
        dataset=datasets,
        feature='raw',
        mechanism='mbm',
        model='sage',
        x_eps=[0.01, 0.1, 1, 2, 3, np.inf],
        x_steps=[0, 2, 4, 8, 16],
        y_eps=[0.5, 1, 2, 3, np.inf],
        y_steps=[0, 2, 4, 8, 16],
        forward_correction=True,
        learning_rate=CommandBuilder.BEST_VALUE,
        weight_decay=CommandBuilder.BEST_VALUE,
        dropout=CommandBuilder.BEST_VALUE
    )

    run_cmds = list(set(run_cmds))  # remove duplicate runs
    return run_cmds


def experiment_baselines(args):
    run_cmds = []
    cmdbuilder = CommandBuilder(args=args, hparams_dir='./hparams')
    datasets = ['cora', 'pubmed', 'facebook', 'lastfm']

    ## DIFFERENT GNN MODELS
    run_cmds += cmdbuilder.build(
        dataset=datasets,
        feature='raw',
        mechanism='mbm',
        model=['gcn', 'gat'],
        x_eps=[0.01, 0.1, 1, 2, 3, np.inf],
        x_steps=CommandBuilder.BEST_VALUE,
        y_eps=[0.5, 1, 2, 3, np.inf],
        y_steps=CommandBuilder.BEST_VALUE,
        forward_correction=True,
        learning_rate=CommandBuilder.BEST_VALUE,
        weight_decay=CommandBuilder.BEST_VALUE,
        dropout=CommandBuilder.BEST_VALUE
    )

    ## FULLY-PRIVATE BASELINES
    run_cmds += cmdbuilder.build(
        dataset=datasets,
        feature=['rnd', 'one', 'ohd'],
        mechanism='mbm',
        model='sage',
        x_eps=np.inf,
        x_steps=CommandBuilder.BEST_VALUE,
        y_eps=[1, np.inf],
        y_steps=CommandBuilder.BEST_VALUE,
        forward_correction=True,
        learning_rate=CommandBuilder.BEST_VALUE,
        weight_decay=CommandBuilder.BEST_VALUE,
        dropout=CommandBuilder.BEST_VALUE
    )

    ## BASELINE LDP MECHANISMS
    run_cmds += cmdbuilder.build(
        dataset=datasets,
        feature='raw',
        mechanism=['1bm', 'lpm', 'agm'],
        model='sage',
        x_eps=[0.01, 0.1, 1, 2, 3],
        x_steps=CommandBuilder.BEST_VALUE,
        y_eps=[1, np.inf],
        y_steps=CommandBuilder.BEST_VALUE,
        forward_correction=True,
        learning_rate=CommandBuilder.BEST_VALUE,
        weight_decay=CommandBuilder.BEST_VALUE,
        dropout=CommandBuilder.BEST_VALUE
    )

    ## NO LABEL CORRECTION
    run_cmds += cmdbuilder.build(
        dataset=datasets,
        feature='raw',
        mechanism='mbm',
        model='sage',
        x_eps=[1, np.inf],
        x_steps=CommandBuilder.BEST_VALUE,
        y_eps=[0.5, 1, 2, 3],
        y_steps=0,
        forward_correction=False,
        learning_rate=CommandBuilder.BEST_VALUE,
        weight_decay=CommandBuilder.BEST_VALUE,
        dropout=CommandBuilder.BEST_VALUE
    )

    run_cmds = list(set(run_cmds))  # remove duplicate runs
    return run_cmds


def experiment_generator(args):
    run_cmds = []

    if args.hyperopt:
        run_cmds += hyperopt(args)
    if args.LPGNN:
        run_cmds += experiment_lpgnn(args)
    if args.baselines:
        run_cmds += experiment_baselines(args)

    return run_cmds


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser, parser_create = JobManager.register_arguments(parser)
    parser.add_argument('-o', '--output-dir', type=str, default='./results', help="directory to store the results")
    parser_create.add_argument('--project', type=str, help='project name for wandb logging (omit to disable)')
    parser_create.add_argument('-s', '--seed', type=int, default=12345, help='initial random seed')
    parser_create.add_argument('-r', '--repeats', type=int, default=10, help="number of experiment iterations")
    parser_create.add_argument('--hyperopt', action='store_true')
    parser_create.add_argument('--LPGNN', action='store_true')
    parser_create.add_argument('--baselines', action='store_true')
    args = parser.parse_args()
    print_args(args)

    JobManager(args, cmd_generator=experiment_generator).run()


if __name__ == '__main__':
    main()
