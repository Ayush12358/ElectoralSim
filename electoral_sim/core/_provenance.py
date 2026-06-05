# Data provenance registry for bundled presets
# Calibration status: structural_demo | partially_calibrated | historically_calibrated | validation_only
PRESET_PROVENANCE = {
    "india": {
        "calibration": "structural_demo",
        "source": "Election Commission of India (synthetic positions)",
        "electoral_system": "FPTP",
        "n_constituencies": 543,
    },
    "usa": {
        "calibration": "structural_demo",
        "source": "Synthetic two-party positions",
        "electoral_system": "FPTP",
        "n_constituencies": 435,
    },
    "scotland": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, AMS 73 constituency + 56 list",
        "electoral_system": "FPTP",
    },
    "spain": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, D'Hondt PR in 52 provinces, 3% threshold",
        "electoral_system": "PR",
        "threshold": 0.03,
    },
    "sweden": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, Sainte-Lague PR, 29 counties, 4% threshold",
        "electoral_system": "PR",
        "threshold": 0.04,
    },
    "switzerland": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, PR with 26 cantons",
        "electoral_system": "PR",
        "n_constituencies": 26,
    },
    "uk": {
        "calibration": "structural_demo",
        "source": "Synthetic multi-party positions",
        "electoral_system": "FPTP",
        "n_constituencies": 650,
    },
    "germany": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, Sainte-Lagu\u00eb allocation",
        "electoral_system": "PR",
        "threshold": 0.05,
    },
    "australia_house": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP fallback for IRV)",
        "electoral_system": "FPTP",
        "n_constituencies": 151,
    },
    "australia_senate": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (PR fallback for STV)",
        "electoral_system": "PR",
        "n_constituencies": 8,
    },
    "mexico": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, 300 FPTP districts + 200 PR list",
        "electoral_system": "FPTP",
    },
    "netherlands": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, nationwide PR with 0.67% threshold",
        "electoral_system": "PR",
        "threshold": 0.0067,
    },
    "norway": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, Sainte-Lague PR, 19 counties, 4% threshold",
        "electoral_system": "PR",
        "threshold": 0.04,
    },
    "nz": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, MMP 72 electorate + 48 list seats",
        "electoral_system": "FPTP",
        "threshold": 0.05,
    },
    "south_africa": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, pure PR",
        "electoral_system": "PR",
        "allocation": "dhondt",
    },
    "brazil": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, open-list PR",
        "electoral_system": "PR",
        "allocation": "dhondt",
    },
    "chile": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, D'Hondt PR in 28 multi-member districts",
        "electoral_system": "PR",
    },
    "eu": {
        "calibration": "structural_demo",
        "source": "European Parliament 2024-2029 term (synthetic positions)",
        "electoral_system": "PR",
        "allocation": "dhondt",
        "n_seats": 720,
    },
    "france": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP simulation of two-round)",
        "electoral_system": "FPTP",
    },
    "canada": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, FPTP with 338 ridings",
        "electoral_system": "FPTP",
        "n_constituencies": 338,
    },
    "israel": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, nationwide PR with 3.25% threshold",
        "electoral_system": "PR",
        "threshold": 0.0325,
    },
    "ireland": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, STV with 39 multi-member constituencies",
        "electoral_system": "PR",
    },
    "japan": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions (FPTP base of parallel system)",
        "electoral_system": "FPTP",
    },
    "wales": {
        "calibration": "structural_demo",
        "source": "Synthetic party positions, AMS 40 constituency + 20 list",
        "electoral_system": "FPTP",
    },
}
