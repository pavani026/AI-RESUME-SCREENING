# Assignment Report: AI Resume Screening System with Tracing

## 1. Objective

Build an AI-powered resume screening system that scores candidates against
a job description and explains its reasoning, using LangChain for pipeline
construction and LangSmith for tracing/debugging.

## 2. Approach

The system is built as 4 independent, chainable steps, each implemented as
its own LangChain chain using LCEL (`prompt | llm | parser`):

1. **Skill Extraction** - Reads raw resume text and extracts skills, tools,
   and estimated years of experience as structured JSON.
2. **Matching** - Compares the extracted candidate data against the job
   description's required/preferred skills, producing matched skills,
   missing skills, and a match percentage.
3. **Scoring** - Converts the matching results into a single 0-100 fit
   score using a transparent weighted formula (70% skill match,
   30% experience fit).
4. **Explanation** - Generates a plain-language explanation of why the
   candidate received that score, citing specific matched/missing skills.

These 4 chains are composed in `chains/pipeline.py` into a single
`ResumeScreeningPipeline` class, where each step's output becomes the
next step's input - matching the required flow:

```
Resume -> Extract -> Match -> Score -> Explain -> Tracing
```

## 3. Why This Design

- **Modularity**: Separating extraction, matching, scoring, and
  explanation into independent chains means each can be tested,
  debugged, and improved without touching the others - useful since
  the assignment specifically requires a `prompts/`, `chains/`, `main.py`
  structure.
- **Explainability by construction**: Rather than asking the LLM to
  output a score directly, scoring is based on a fixed formula applied
  to matching results, and a separate explanation step describes that
  reasoning in plain language. This keeps the score auditable rather
  than being an opaque LLM judgment.
- **Anti-hallucination by prompt design**: Both the extraction and
  matching prompts explicitly instruct the model not to assume skills
  that aren't written in the resume - directly addressing the
  assignment's "Do NOT assume skills not present in the resume" rule.

## 4. Sample Results

Three resumes were run against a sample Data Scientist job description:

| Candidate | Expected Outcome |
|---|---|
| Strong Candidate | High skill match (Python, ML, AWS, Spark, NLP all present) -> high score |
| Average Candidate | Partial match (core Python/SQL/Scikit-learn present, but missing cloud/deep learning skills) -> medium score |
| Weak Candidate | Minimal overlap (web development background, not data science) -> low score |

Exact scores depend on the LLM's output at run time - see `results.json`
after running `main.py`, and the corresponding LangSmith traces for the
full reasoning chain.

## 5. Debugging Notes (LangSmith)

While testing, one run produced an incorrect output where the matching
step listed a skill as "matched" that was only loosely related to a
required skill (a soft synonym match that was too generous). This was
caught by inspecting the matching chain's span in LangSmith and comparing
its output against the candidate's actual extracted skills list. The
matching prompt was then tightened with the instruction to only count
"exact or clearly synonymous matches" rather than broadly related terms,
which is reflected in the current version of `prompts/matching_prompt.py`.

## 6. Limitations

- Resumes are provided as plain text files rather than parsed from PDFs/
  DOCX - parsing real resume file formats was out of scope for this
  assignment but would be a natural next step (e.g. using `pypdf` or
  `python-docx` to extract text before feeding it into the extraction
  chain).
- Match scoring is currently based only on explicit skill keyword overlap;
  it does not account for skill proficiency level or recency.

## 7. Tech Stack

Python, LangChain (LCEL), LangSmith, OpenAI API (gpt-4o-mini).
