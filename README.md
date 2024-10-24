# variant-combinations

variants.conf
* (human readable, likely TOML)
* key-value association of variable name and preferred values.
* variables are namespaced under provider to avoid confusion
* captures provider metadata (version, ???) for reproducibility

NOTE: combinations do not need to include all keys, but
combinations that include more keys are higher priority

NOTE: sorting in list of dicts in output is effectively priority
