import ruamel.yaml


def load_config(path):
    with open(path, 'r') as fp:
        return ruamel.yaml.round_trip_load(fp.read())


def save_config(config, path):
    with open(path, 'w') as fp:
        ruamel.yaml.round_trip_dump(config, fp)
