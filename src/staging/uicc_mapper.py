from src.validation.validator import Json


def map_uicc_dtc(data: Json) -> str:
    if None in (data.age, data.T, data.N, data.M):
        return "INSUFFICIENT_INFORMATION"

    if data.age < 55:
        return "Stage II" if data.M == "M1" else "Stage I"

    if data.M == "M1":
        return "Stage IVB"

    T = data.T
    N = data.N

    if T == "T4b":
        return "Stage IVA"
    if T == "T4a":
        return "Stage III"

    if T in {"T3", "T3a", "T3b"} or (T in {"T1", "T1b", "T1a", "T2"} and N == "N1"):
        return "Stage II"

    if T in {"T1", "T1b", "T1a", "T2"}:
        return "Stage I"

    return "INSUFFICIENT_INFORMATION"

def map_uicc_mtc(data: Json) -> str:
    if None in (data.age, data.T, data.N, data.M):
        return "INSUFFICIENT_INFORMATION"

    if data.M == "M1":
        return "Stage IVC"

    T = data.T
    N = data.N

    if T in ["T1b", "T1a", "T1"] and N == "N0":
        return "Stage I"
    if T in ["T2", "T3"] and N == "N0":
        return "Stage II"
    if N == "N1a":
        return "Stage III"
    if N == "N1b" or T == "T4a":
        return "Stage IVA"
    if T == "T4b":
        return "Stage IVB"

    return "INSUFFICIENT_INFORMATION"


def map_uicc_utc(data: Json) -> str:
    if None in (data.age, data.T, data.N, data.M):
        return "INSUFFICIENT_INFORMATION"

    if data.M == "M1":
        return "Stage IVC"

    T = data.T
    N = data.N

    if T in {"T1", "T1a", "T1b", "T2", "T3a"} and N == "N0":
        return "Stage IVA"
    if T in {"T1", "T1a", "T1b", "T2", "T3a"} and N in {"N1", "N1a"}:
        return "Stage IVB"
    if T in {"T3b", "T4a", "T4b"}:
        return "Stage IVB"

    return "INSUFFICIENT_INFORMATION"


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

    result = patient_description.model_dump()
    result["Stage"] = stage
    return result

