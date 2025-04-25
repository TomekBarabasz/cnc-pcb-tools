def read_yml(filename):
    from types import SimpleNamespace
    import yaml

    def dict_to_namespace(d):
        if isinstance(d, dict):
            return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})
        elif isinstance(d, list):
            return [dict_to_namespace(i) for i in d]
        else:
            return d
    with open(filename) as f:
        return dict_to_namespace( yaml.safe_load(f) )

