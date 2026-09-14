def is_missing(value):
    """
    Determine whether a requirements field should be
    treated as missing.
    """

    if value is None:
        return True

    value = str(value).strip()

    return value == "" or value in ["-", "—"]


def check_traceability(requirement):
    """
    Check deterministic traceability fields for a requirement.
    """

    issues = []

    parent_id = requirement["Parent_ID"]
    verification_method = requirement["Verification_Method"]

    if is_missing(parent_id):
        issues.append("Missing Parent_ID")

    if is_missing(verification_method):
        issues.append("Missing Verification_Method")

    return {
        "traceability_ok": len(issues) == 0,
        "traceability_issues": issues
    }


if __name__ == "__main__":
    import pandas as pd

    test_requirement = pd.Series({
        "Requirement_ID": "SYS-005",
        "Requirement_Text": "The system shall be lightweight and efficient.",
        "Parent_ID": "—",
        "Verification_Method": "Inspection"
    })

    result = check_traceability(test_requirement)

    print(result)