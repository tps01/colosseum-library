"""Verify a supplied eye mask against saved PHY voltage captures.

Requires Colosseum Equipment and Shared. The DUT stimulus and scope capture
are prepared externally. See the topic README for CSV and mask requirements.
"""

import colosseum as col

from digital.ethernet.eye_reference import verify_eye_traces

SETTINGS = {
    "captures": FILL_IN_HERE,  # differential CSV paths and/or (positive, negative) CSV pairs
    "mask_path": FILL_IN_HERE,
    "period_s": FILL_IN_HERE,  # use None for captures already aligned to the mask axis
    "origin_s": FILL_IN_HERE,
    "max_sample_spacing_s": FILL_IN_HERE,
}


@col.measurement
def measure_eye_mask(*, key):
    return verify_eye_traces(**SETTINGS)


def main() -> None:
    measure_eye_mask(key="ethernet_eye_mask")
    col.shared.verify.verify_field(key="ethernet_eye_mask", field="passed", expected_val=True)


if __name__ == "__main__":
    main()
    col.endex()
