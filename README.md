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
