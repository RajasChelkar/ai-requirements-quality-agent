def calculate_quality_score(ai_analysis, traceability):
    """
    Calculate a deterministic requirements quality score.

    Maximum score: 100
    """

    score = 100

    # AI-based quality findings
    if ai_analysis.get("ambiguous", False):
        score -= 25

    quality_issues = ai_analysis.get("quality_issues", [])

    # Deduct points for quality issues, up to 30 points
    issue_penalty = min(len(quality_issues) * 10, 30)
    score -= issue_penalty

    # Deterministic traceability checks
    traceability_issues = traceability.get(
        "traceability_issues", []
    )

    # Deduct 20 points for missing traceability information
    traceability_penalty = min(
        len(traceability_issues) * 20,
        40
    )

    score -= traceability_penalty

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return score

if __name__ == "__main__":

    test_ai_analysis = {
        "ambiguous": True,
        "quality_issues": [
            "Incomplete",
            "Not verifiable"
        ]
    }

    test_traceability = {
        "traceability_issues": [
            "Missing Parent_ID"
        ]
    }

    score = calculate_quality_score(
        test_ai_analysis,
        test_traceability
    )

    print(f"Quality Score: {score}/100")