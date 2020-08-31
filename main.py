#!/usr/bin/env python

import yaml
from modules import *
from pprint import pprint

# TODO write scheduler
# TODO write git module for running scripts from repostiories
# TODO generate run stats (time, errors, size)
# TODO add logger


def parse_yaml_actions(file_path: str) -> dict:
    main_input = []
    with open(file_path, 'r') as fp:
        try:
            main_input = yaml.safe_load(fp)
        except yaml.YAMLError as exc:
            print(exc)

    return main_input


def get_plan(actions: dict) -> list:
    plan = [check_module_integrity(globals()[action_type.title()](**context))
            for action in actions for action_type, context in action.items()]
    return plan


def main():
    actions = parse_yaml_actions('example.yml')
    print(f'[*] Initializing {len(actions)} actions\n')
    plan = get_plan(actions)

    input_data = None
    for call in plan:
        # Set input_data from previous call output_data
        if not call.input_data and input_data is not None:
            call.input_data = input_data

        call.output_data = input_data = call_path(**call.debug)

        if call.output_data.get('exit'):
            print(f'[*] Call to {call.path} failed!')
            exit(1)
        # pprint(call.output_data)


if __name__ == '__main__':
    main()
