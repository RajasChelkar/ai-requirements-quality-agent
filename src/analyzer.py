import os
import json

from google import genai
from dotenv import load_dotenv
from ingestion import load_requirements
from pathlib import Path
from rag import retrieve_guidance, build_context
from quality_checks import check_traceability
from scoring import calculate_quality_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CACHE_FILE = PROJECT_ROOT / "Data" / "analysis_cache.json"

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def load_cache():
    """Load previously completed AI analyses."""

    if not CACHE_FILE.exists():
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache):
    """Save AI analyses to disk."""

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)

def analyze_requirement(requirement_text):
    # Retrieve relevant requirements-engineering guidance
    results = retrieve_guidance(requirement_text, top_k=3)
    guidance = build_context(results)

    prompt = f"""
You are a requirements engineering assistant.

Analyze the following system requirement using the
engineering guidance provided below.

Requirement:
{requirement_text}

Engineering Guidance:
{guidance}

Return ONLY valid JSON using exactly this structure:

{{
  "classification": "Functional or Non-Functional",
  "ambiguous": true,
  "ambiguous_terms": [],
  "quality_issues": [],
  "suggested_improvement": ""
}}

Rules:
- classification must be either "Functional" or "Non-Functional".
- ambiguous must be true or false.
- ambiguous_terms must be a list of strings.
- quality_issues must be a list of strings.
- suggested_improvement must be a string.
- Base the analysis on the provided engineering guidance.
- Do not invent engineering values, limits, frequencies,
  accuracy values, or other technical specifications.
- If a required technical value is missing, explicitly
  indicate that clarification is required.
- Return JSON only. Do not include markdown or explanations
  outside the JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\nRAW GEMINI RESPONSE:")
    print(repr(response.text))

    return json.loads(response.text)

def analyze_requirement_row(requirement, cache):
    """
    Perform AI-based quality analysis, deterministic
    traceability checks, and quality scoring.
    """

    requirement_id = requirement["Requirement_ID"]

    if requirement_id in cache:
        ai_result = cache[requirement_id]
        print(f"Using cached AI analysis for {requirement_id}")

    else:
        print(f"Calling Gemini for {requirement_id}...")

        try:
            ai_result = analyze_requirement(
                requirement["Requirement_Text"]
            )

            cache[requirement_id] = ai_result
            save_cache(cache)

        except Exception as error:
            print(f"Gemini analysis failed for {requirement_id}")

            ai_result = {
                "status": "AI analysis unavailable",
                "error": str(error)
            }

    # Deterministic traceability check
    traceability_result = check_traceability(requirement)

    # Calculate quality score only when AI analysis is available
    if "status" not in ai_result:
        quality_score = calculate_quality_score(
            ai_result,
            traceability_result
        )
    else:
        quality_score = None

    return {
        "requirement_id": requirement_id,
        "requirement_text": requirement["Requirement_Text"],
        "ai_analysis": ai_result,
        "traceability": traceability_result,
        "quality_score": quality_score
    }

if __name__ == "__main__":
    requirements_file = PROJECT_ROOT / "Data" / "Requirements.xlsx"

    requirements = load_requirements(requirements_file)

    cache = load_cache()

    results = []

    for _, requirement in requirements.iterrows():

        result = analyze_requirement_row(
            requirement,
            cache
        )

        results.append(result)

    print("\nAnalysis complete!")
    print(f"Requirements analyzed: {len(results)}")

    print("\nResults:\n")

    for result in results:
        print(result)
        print("-" * 80)