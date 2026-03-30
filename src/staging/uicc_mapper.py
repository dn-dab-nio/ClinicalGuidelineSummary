from src.staging.uicc_validator import Json

def map_uicc_dtc(data: Json) -> str:
    age = data.age
    T = data.T
    N = data.N
    M = data.M

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
            if T in ["T1", "T1b", "T1a", "T2"]:
                return "Stage I"
            if ((T in ["T3", "T3a", "T3b"]) or (T in ["T1",  "T1b", "T1a", "T2"] and N == "N1")):
                return "Stage II"
    else:
        return "INVALID_AGE"

def map_uicc_mtc(data: Json) -> str:
    age = data.age
    T = data.T
    N = data.N
    M = data.M

    if None in [age, T, N, M]:
        return "INSUFFICIENT_INFORMATION"

    if M == "M1":
        return "Stage IVC"
    else:
        if T in ["T1b", "T1a", "T1"] and N == "N0":
            return "Stage I"
        if T in ["T2", "T3"] and N == "N0":
            return "Stage II"
        if N == "N1a":
            return "Stage III"
        if N == "N1b":
            return "Stage IVA"
        if T == "T4a":
            return "Stage IVA"
        if T == "T4b":
            return "Stage IVB"


def map_uicc_utc(data: Json) -> str:
    age = data.age
    T = data.T
    N = data.N
    M = data.M

    if None in [age, T, N, M]:
        return "INSUFFICIENT_INFORMATION"

    if M == "M1":
        return "Stage IVC"
    else:
        if T in ["T1", "T1a", "T1b", "T2", "T3a"] and N == "N0":
            return "Stage IVA"
        if T in ["T1", "T1a", "T1b", "T2", "T3a"] and N in ["N1", "N1a"]:
            return "Stage IVB"
        if T in ["T3b","T4a", "T4b"]:
            return "Stage IVB"

def map_uicc(patient_description: Json) -> dict:

    cancer_group = patient_description.cancer_type.group

    if cancer_group == "Differentiated thyroid carcinoma":
        stage = map_uicc_dtc(patient_description)
    elif cancer_group == "Medullary thyroid carcinoma":
        stage = map_uicc_mtc(patient_description)
    elif cancer_group == "Anaplastic thyroid carcinoma":
        stage = map_uicc_utc(patient_description)
    else:
        stage =  "INSUFFICIENT_INFORMATION"

    patient_description = patient_description.model_dump()
    patient_description["Stage"] = stage
    return patient_description

