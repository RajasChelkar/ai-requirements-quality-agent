## Workflow

The application follows a hybrid AI workflow that combines deterministic Python checks, Retrieval-Augmented Generation (RAG), and Gemini-based semantic analysis.


                    ┌─────────────────────┐
                    │  Requirements.xlsx  │
                    │      / CSV           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Requirement        │
                    │  Ingestion           │
                    │  (Pandas)            │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       Requirement Analysis     │
              └───────────────┬────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
      ┌──────────────────┐        ┌──────────────────┐
      │ Deterministic    │        │ RAG Knowledge    │
      │ Engineering      │        │ Base             │
      │ Checks           │        │                  │
      │                  │        │ • Ambiguity     │
      │ • Parent ID      │        │ • Verifiability  │
      │ • Verification   │        │ • Traceability   │
      │   Method         │        │ • Quality        │
      └────────┬─────────┘        └────────┬─────────┘
               │                           │
               │                           ▼
               │                 ┌──────────────────┐
               │                 │ Gemini LLM       │
               │                 │                  │
               │                 │ • Classification │
               │                 │ • Ambiguity     │
               │                 │ • Quality issues │
               │                 │ • Improvement    │
               │                 └────────┬─────────┘
               │                          │
               └────────────┬─────────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Structured Analysis │
                 │       Result        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Quality Score       │
                 │ + Traceability      │
                 │ + AI Findings       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Streamlit Dashboard │
                 │                     │
                 │ • Requirement view  │
                 │ • Quality scores    │
                 │ • Issues            │
                 │ • Suggestions       │
                 └─────────────────────┘


Step-by-step

1. Requirement ingestion

The user uploads an Excel or CSV file containing structured requirements. Pandas loads the data into a DataFrame for processing.

2. Deterministic validation

Python performs checks that do not require an LLM, such as checking whether a requirement has a Parent_ID and a Verification_Method.

This keeps objective validation rules deterministic and reproducible.

3. RAG retrieval

The requirement is converted into an embedding using a Sentence Transformer. ChromaDB searches the knowledge base for relevant requirements-engineering guidance.

The retrieved guidance is provided to Gemini as context.

4. AI-powered requirement analysis

Gemini analyzes the requirement using the retrieved engineering guidance. The model evaluates aspects such as:

Functional vs. Non-Functional classification
Ambiguous or subjective language
Quality issues
Completeness and verifiability concerns
Potential improved wording

The prompt explicitly instructs the model not to invent engineering values. When information is missing, the suggested improvement uses a clarification placeholder instead.

5. Structured result

Gemini returns the analysis in a structured JSON format. This allows the application to process the model output consistently rather than relying on free-form text.

6. Quality scoring

The application combines the AI analysis with deterministic traceability results to calculate a prototype quality score.

The score is intended as a demonstration of the workflow and is not an industry-standard requirements-quality metric.

7. Dashboard

Streamlit presents the results through an interactive dashboard, allowing the user to review individual requirements, quality issues, traceability problems, scores, and suggested improvements.

Human-in-the-loop

The AI does not automatically replace engineering requirements.

Suggested improvements are presented to the engineer for review. The engineer remains responsible for validating the technical meaning, constraints, and acceptance criteria before accepting any proposed change.

This reflects the intended role of the system: AI-assisted requirements engineering rather than fully automated requirements authoring.

## Application Preview

The application is implemented as an interactive Streamlit dashboard that allows engineers to upload requirements and review AI-assisted quality and traceability analysis.

### Dashboard Overview

![Dashboard Overview](docs/Dashboard%20Top.png)

### Individual Requirement Analysis

![Individual Requirement Analysis](docs/Individual%20analysis.png)

### Requirements Quality Overview

![Requirements Quality Overview](docs/Quality%20overview.png)
