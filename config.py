""" Configuration file. """

# Safe dosage list
SAFE_DOSAGES = {
        "0.25% Plain Lidocaine": 4,
        "0.25% Plain Bupivacaine": 2,
        "0.25% Lidocaine with Epinephrine": 7,
        "0.5% Plain Bupivacaine": 2,
        "0.5% Bupivacaine with Epinephrine": 3,
        "1% Plain Lidocaine": 4,
        "1% Lidocaine with Epinephrine": 7,
        "2% Plain Lidocaine": 4,
        "2% Lidocaine with Epinephrine": 7,
}
SAFE_DOSAGES_TABLE = {
            "Plain Lidocaine": 4,
            "Lidocaine with Epinephrine": 7,
            "Plain Bupivacaine": 2,
            "Bupivacaine with Epinephrine": 3,
}

# Threshold for green/yellow/red differentials. Anything beyond yellow is red.
GREEN_THRESHOLD = .05
YELLOW_THRESHOLD = .10

# Main display settings
WEIGHT_MINIMUM = 10
WEIGHT_MAXIMUM = 120

# Pediatrics settings
PEDS_WEIGHT_MINIMUM = 3
PEDS_WEIGHT_MAXIMUM = 50
