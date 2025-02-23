""" Configuration file. """

# Safe dosage list
SAFE_DOSAGES = {
        "0.25% Plain Lidocaine": 4,
        "0.25% Lidocaine with 1:200000 Epinephrine": 7,
        "0.25% Plain Bupivacaine": 2,
        "0.25% Bupivacaine with 1:200000 Epinephrine": 7,
        "0.5% Plain Bupivacaine": 2,
        "0.5% Bupivacaine with 1:200000 Epinephrine": 3,
        "1% Plain Lidocaine": 4,
        "1% Lidocaine with 1:200000 Epinephrine": 7,
        "2% Plain Lidocaine": 4,
        "2% Lidocaine with 1:200000 Epinephrine": 7,
}
SAFE_DOSAGES_TABLE = {
            "Plain Lidocaine": 4,
            "Lidocaine with 1:200000 Epinephrine (Adult)": 7,
            "Lidocaine with 1:200000 Epinephrine (Child)*": 5,
            "Plain Bupivacaine": 2,
            "Bupivacaine with 1:200000 Epinephrine": 3,
}

# Threshold for determining limiting factor between anesthetic, apinephrine content
WEIGHT_THRESHOLD = 50

# Threshold for green/yellow/red differentials. Anything beyond yellow is red.
GREEN_THRESHOLD = .10
YELLOW_THRESHOLD = .15

# Main display settings
WEIGHT_MINIMUM = 10
WEIGHT_MAXIMUM = 120

AGE_MINIMUM = 1
AGE_MAXIMUM = 100

# Pediatrics settings
PEDS_WEIGHT_MINIMUM = 3
PEDS_WEIGHT_MAXIMUM = 50
