import tempfile, json, os
from os import path

import itertools as it
import functools as func

import biobox_cli.util.functional as fn

def behave_feature_file(biobox):
    """
    Returns the fullpath for the corresponding feature file for the given biobox type.
    """
    from pkg_resources import resource_filename
    file_ = biobox + '.feature'
    return path.abspath(resource_filename(__name__, path.join('verification', file_)))

def tmp_feature_dir():
    """
    Returns the fullpath of a 'biobox_verify' directory created in the current
    working directory.
    """
    return path.abspath(path.join(os.getcwd(), 'biobox_verify'))

def run(biobox_type, image, task):
    """
    Runs the behave cucumber features for the given biobox and tast given by
    the passed arguments. Creates a directory in the current working directory,
    where the verfication files are created. Returns a dictionary of the behave
    output.
    """
    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()

    cmd = "{file} --define IMAGE={image} --define TASK={task} --define TMPDIR={tmp_dir} --outfile {tmp_file} --format json.pretty --no-summary --stop"
    args = {'file':     behave_feature_file(biobox_type),
            'tmp_dir':  tmp_feature_dir(),
            'image':    image,
            'tmp_file': tmp_file,
            'task':     task}

    behave_main(cmd.format(**args))

    with open(tmp_file, 'r') as f:
        return json.loads(f.read())

def is_failed(behave_data):
    """
    Parses a behave dictionary and returns true if any verifications have
    failed.
    """
    return "failed" in map(lambda i: i['status'], behave_data)

def is_failed_scenario(scenario):
    """
    Returns true if a behave feature scenario has failed.
    """
    return is_failed(filter(fn.is_not_none, (map(fn.get("result"), scenario['steps']))))

def get_scenarios(behave_data):
    return reduce(lambda acc, x: acc + x['elements'], behave_data, [])

def get_failing_scenarios(behave_data):
    """
    Returns all failing scenarios from a behave dictionary
    """
    return filter(is_failed_scenario, get_scenarios(behave_data))

def scenario_name(scenario):
    return scenario["name"]
