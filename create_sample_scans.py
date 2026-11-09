"""
Legacy Sample Scan Generator (Backwards-Compatibility Wrapper)
=============================================================
Delegates directly to generate_sample_data.py to avoid code duplication.
"""

from generate_sample_data import generate_synthetic_samples


def generate_breast_ultrasound_samples(output_dir: str = "sample_scans"):
    """Generates synthetic sample scans in the specified directory."""
    return generate_synthetic_samples(output_dir=output_dir)


if __name__ == "__main__":
    generate_breast_ultrasound_samples()
