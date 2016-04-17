import yaml
def get_config():
    with open ("sample_config.yml") as config:
        return yaml.load(config)
