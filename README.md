# AI Resume Screening System with Tracing

An AI-powered resume screening pipeline built with **LangChain** and **LangSmith**.
Given a resume and a job description, it extracts the candidate's skills,
matches them against job requirements, assigns a 0-100 fit score, and
generates a human-readable explanation for that score — with full
tracing and debugging support via LangSmith.

## Problem Statement

```
Input    -> Resume + Job Description
Process  -> Skill Extraction + Matching + Scoring
Output   -> Fit Score + Explanation
```

## Pipeline Architecture

```
Resume -> Extract -> Match -> Score -> Explain
```

Each step is a separate, modular LangChain chain built with **LCEL**
(LangChain Expression Language), so each stage can be tested, traced, and
debugged independently in LangSmith.

## Project Structure

```
ai-resume-screening/
├── main.py                     # Entry point - runs all 3 sample candidates
├── chains/
│   ├── extraction_chain.py     # Step 1: Skill/tool/experience extraction
│   ├── matching_chain.py       # Step 2: Match against job description
│   ├── scoring_chain.py        # Step 3: 0-100 fit score
│   ├── explanation_chain.py    # Step 4: Human-readable explanation
│   └── pipeline.py             # Orchestrates all 4 steps in sequence
├── prompts/
│   ├── extraction_prompt.py
│   ├── matching_prompt.py
│   ├── scoring_prompt.py
│   └── explanation_prompt.py
├── data/
│   ├── job_description.txt     # Sample Data Scientist job description
│   └── resumes/
│       ├── strong_candidate.txt
│       ├── average_candidate.txt
│       └── weak_candidate.txt
├── requirements.txt
├── .env.example
└── report.md                   # Assignment write-up / explanation doc
```

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your real keys:
   ```bash
   cp .env.example .env
   ```
   You'll need:
   - An **OpenAI API key** (https://platform.openai.com)
   - A **LangSmith API key** (https://smith.langchain.com) for tracing

3. Run the pipeline:
   ```bash
   python main.py
   ```

This runs all 3 sample candidates (Strong / Average / Weak) through the
full pipeline and prints the extraction, matching, scoring, and
explanation output for each. Results are also saved to `results.json`.

## Viewing Traces in LangSmith

Once you run `main.py` with `LANGCHAIN_TRACING_V2=true` set (already done
in `main.py`), log into [smith.langchain.com](https://smith.langchain.com)
and open the `ai-resume-screening-system` project. You'll see 3 separate
traced runs, one per candidate, with every pipeline step (extraction,
matching, scoring, explanation) visible as nested spans — useful for
debugging exactly where an incorrect output came from.

## Anti-Hallucination Design

Every prompt explicitly instructs the model not to assume or infer skills
that aren't present in the resume text, and to return empty values rather
than guess when information is missing. This is enforced at the prompt
level in `prompts/extraction_prompt.py` and `prompts/matching_prompt.py`.

## Scoring Logic

```
final_score = (skill_match_percentage * 0.7) + experience_score
```

Where `experience_score` is 30 points if the experience requirement is
met, 0 if not, and 15 if borderline. This weighting is intentionally
transparent and auditable — the score breakdown is always returned
alongside the final number.

## Tech Stack

- Python
- LangChain + LangChain Expression Language (LCEL)
- LangSmith (tracing & debugging)
- OpenAI API (gpt-4o-mini)

## Bonus Features Implemented

- Structured JSON output for all steps except the final explanation
- LangSmith tags per run (`resume-screening`, candidate name) for easy
  filtering in the dashboard
