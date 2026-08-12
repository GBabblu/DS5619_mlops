# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
142504001

**Seed:**
3720174563

## What was hardcoded, and what would switching it have required?

The original pipeline hardcoded the input file path.
It also hardcoded the input format.
The high-value threshold was hardcoded in the original pipeline.
Changing the threshold would have required editing the Python code.
Switching from CSV to JSON would have required modifying the Python code.
The refactored pipeline reads these values from the YAML configuration.
Therefore, the same pipeline can work with different configurations without changing the Python code.
