"""
main.py - Entry point for the AI Resume Screening System.

Loads sample resumes + job description, runs each through the full
pipeline (Extract -> Match -> Score -> Explain), and prints results.
LangSmith tracing is enabled via environment variables (see .env.example).
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from chains.pipeline import ResumeScreeningPipeline

load_dotenv()  # Loads OPENAI_API_KEY, LANGCHAIN_API_KEY, etc. from .env

# --- LangSmith tracing setup (mandatory per assignment) ---
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ.setdefault("LANGCHAIN_PROJECT", "ai-resume-screening-system")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")

CANDIDATES = {
    "Strong Candidate": "strong_candidate.txt",
    "Average Candidate": "average_candidate.txt",
    "Weak Candidate": "weak_candidate.txt",
}


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    # Temperature 0 keeps outputs consistent/deterministic for scoring tasks.
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    pipeline = ResumeScreeningPipeline(llm)

    job_description = load_text(os.path.join(DATA_DIR, "job_description.txt"))

    results = []
    for label, filename in CANDIDATES.items():
        resume_text = load_text(os.path.join(RESUME_DIR, filename))

        print(f"\n{'=' * 60}")
        print(f"Running pipeline for: {label}")
        print("=" * 60)

        result = pipeline.run(resume_text, job_description, run_name=label)
        results.append(result)

        print(json.dumps(result, indent=2))

    # Save all results to a single file for the submission report.
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll results saved to {output_path}")
    print("Check your LangSmith dashboard for the 3 traced runs "
          "(Strong / Average / Weak Candidate).")


if __name__ == "__main__":
    main()
