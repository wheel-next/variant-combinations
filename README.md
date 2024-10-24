# variant-combinations

variants.conf
* (human readable, likely TOML)
* key-value association of variable name and preferred values.
* variables are namespaced under provider to avoid confusion
* captures provider metadata (version, ???) for reproducibility

NOTE: combinations do not need to include all keys, but
combinations that include more keys are higher priority

NOTE: sorting in list of dicts in output is effectively priority

Schematic:

<img width="1152" alt="Screenshot 2024-10-24 at 1 05 15 PM" src="https://github.com/user-attachments/assets/c30f9c1a-1f0b-40f7-b714-0774a67893ca">
