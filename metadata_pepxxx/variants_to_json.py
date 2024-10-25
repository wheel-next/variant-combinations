import itertools
from typing import Generator


def get_combinations(data: dict) -> Generator:
    all_values = []
    key_map = []  # Keeps track of dotted notation keys
    
    # Extract the 'values' from the data, preserving order
    for provider_name, provider in data["providers"].items():
        for variable_name, variable in provider["variables"].items():
            # Create dotted key names like "nvidia.driver_version"
            dotted_key = f"{provider_name}.{variable_name}"
            if isinstance(variable["values"], list):
                all_values.append(variable["values"])
            else:
                all_values.append([variable["values"]])
            key_map.append(dotted_key)

    # Generate all possible combinations, including optional elements
    for r in range(len(all_values), 0, -1):
        for combo in itertools.combinations(all_values, r):
            for product in itertools.product(*combo):
                combination_dict = {}
                for idx, value in enumerate(product):
                    combination_dict[key_map[idx]] = value
                yield combination_dict
