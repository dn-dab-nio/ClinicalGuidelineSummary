from src.staging.uicc_extractor import tnm_extract

def map_uicc_dtc(data):
    age = data["age"]
    T = data["T"]
    N = data["N"]
    M = data["M"]

    if None in [age, T, N, M]:
        return "INSUFFICIENT_INFORMATION"

    if age < 55:
        if M == "M1":
            return "Stage II"
        else:
            return "Stage I"
    elif age >= 55:
        if M == "M1":
            return "Stage IVB"
        else:
            if T == "T4b":
                return "Stage IVA"
            if T == "T4a":
                return "Stage III"
            if T in ["T1b", "T1a", "T2"]:
                return "Stage I"
            if (T == "T3" or (T in ["T1", "T2"] and N == "N1")):
                return "Stage II"
    else:
        return "INVALID_AGE"

def map_uicc_mtc(data):
    age = data["age"]
    T = data["T"]
    N = data["N"]
    M = data["M"]

    if None in [age, T, N, M]:
        return "INSUFFICIENT_INFORMATION"

    if M == "M1":
        return "Stage IVC"
    else:
        if T in ["T1b", "T1a", "T1"] and N == "N0":
            return "Stage I"
        if T in ["T2", "T3"] and N == "N0":
            return "Stage II"
        if T in ["T1","T2", "T3"] and N == "N1a":
            return "Stage III"
        if T in ["T1","T2", "T3"] and N == "N1b":
            return "Stage IVA"
        if T == "T4a":
            return "Stage IVA"
        if T == "T4b":
            return "Stage IVB"


def map_uicc_utc(data):
    age = data["age"]
    T = data["T"]
    N = data["N"]
    M = data["M"]

    if None in [age, T, N, M]:
        return "INSUFFICIENT_INFORMATION"

    if M == "M1":
        return "Stage IVC"
    else:
        if T in ["T1", "T2", "T3a"] and N == "N0":
            return "Stage IVA"
        if T in ["T1", "T2", "T3a"] and N == "N1":
            return "Stage IVB"
        if T in ["T3b","T4a", "T4b"]:
            return "Stage IVB"

def map_uicc(patient_description):
    json_classification = tnm_extract(patient_description)

    cancer_group = json_classification["Cancer_type"]["group"]

    if cancer_group == "Differentiated thyroid carcinoma":
        stage = map_uicc_dtc(json_classification)
    elif cancer_group == "Medullary thyroid carcinoma":
        stage = map_uicc_mtc(json_classification)
    elif cancer_group == "Anaplastic thyroid carcinoma":
        stage = map_uicc_utc(json_classification)
    else:
        return "INSUFFICIENT_INFORMATION"

    json_classification["stage"] = stage
    return json_classification



