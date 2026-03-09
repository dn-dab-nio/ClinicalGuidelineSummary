#tu będzie działo się sprawdzanie, czy JSON
#wygenerowany jest poprawny, kompletny i zgodny z systemem.

def validate_json(data):
    keys = ["age", "T", "N", "M", "cancer_type"]
    for key in keys:
        if key not in data:
            return False, f"{key} is missing!!!"

    if data["age"] is not None and not isinstance(data["age"], int):
        return False, f"{data['age']}: Age is invalid!!!"

    if data["T"] not in valid_T:
        return False, f"{data['T']}: T is invalid!!!"

    if data["N"] not in valid_N:
        return False, f"{data['N']}: N is invalid!!!"

    if data["M"] not in valid_M:
        return False, f"{data['M']}: M is invalid!!!"

    if data["cancer_type"]["group"] not in valid_groups:
        return False, f"{data["cancer_type"]["group"]}: Group is invalid!!!"

    return True, "Valid"

valid_T = ["T1", "T1a", "T1b", "T2", "T3", "T3a", "T3b", "T4", "T4a", "T4b"]
valid_N = ["N0", "N0a", "N0b", "N1", "N1a", "N1b", "NX"]
valid_M = ["M0", "M1"]

valid_groups = ["Differentiated thyroid carcinoma",
                "Medullary thyroid carcinoma",
                "Anaplastic thyroid carcinoma"
]

