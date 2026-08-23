<div align="center">

# Resonance AI

### Research Exploration, Synthesis & Originality Navigation Engine

### Autonomous Agentic Framework for Research Synthesis & Academic Manuscript Engineering

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Gemini API](https://img.shields.io/badge/Google%20GenAI-3.6%20%2F%203.7-4285F4.svg?style=flat-square&logo=googlecloud&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[Features](#-key-features) • [System Architecture](#-system-architecture) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Specs](#-api-endpoints)

</div>

---

## Overview

**Resonance AI** is an end-to-end research intelligence platform designed to streamline the academic workflow from raw ideology to published manuscript.

Powered by agentic LLM graphs and dynamic academic index integrations such as **OpenAlex**, Resonance AI extracts core **Research DNA**, identifies literature gaps, cross-references citations, and drafts section-by-section academic papers in both **Markdown** and **LaTeX** formats.

---

## Key Features

- **Research DNA Extraction**: Automatically distills raw project concepts into structured technical problems, proposed solutions, key innovations, and domain tags.

- **OpenAlex Academic Search Integration**: Automated literature discovery querying live academic databases to surface relevant prior works, citation metrics, and peer-reviewed papers.

- **Maturity-Based Gap Analysis**: Evaluates proposed research methodologies against existing literature to identify technical limitations and unexplored research vectors.

- **Modular Section Drafting**: Generates context-aware manuscript sections such as *Abstract*, *Introduction*, *Methodology*, and more using high-fidelity LLMs.

- **Dual Export Engine**: One-click generation and download for production-ready **LaTeX (`.tex`)** and **Markdown (`.md`)** manuscript files.

---

## System Architecture

Resonance AI operates on a decoupled backend architecture utilizing **LangGraph** / dynamic execution state pipelines coupled with the official **Google GenAI SDK**.

```text
              ┌──────────────────────────────────────────────┐
              │              User Input Interface            │
              │  (Raw Ideology, Target Problem, Method)      │
              └──────────────────────┬───────────────────────┘
                                     │
                                     ▼
              ┌──────────────────────────────────────────────┐
              │          FastAPI Backend Service             │
              └──────────────────────┬───────────────────────┘
                                     │
             ┌───────────────────────┴───────────────────────┐
             │                                               │
             ▼                                               ▼
┌──────────────────────────────┐               ┌──────────────────────────────┐
│     Research DNA Pipeline    │               │  OpenAlex Literature Search  │
│                              │               │                              │
│      Gemini 3.6 Flash        │               │    Scholarly Search API      │
└──────────────┬───────────────┘               └──────────────┬───────────────┘
               │                                              │
               └───────────────────────┬──────────────────────┘
                                       │
                                       ▼
              ┌──────────────────────────────────────────────┐
              │       Gap Analysis & Novelty Mapping         │
              │            (ResearchGapItem Schema)          │
              └──────────────────────┬───────────────────────┘
                                     │
                                     ▼
              ┌──────────────────────────────────────────────┐
              │       Academic Manuscript Generation         │
              │        (Abstract, Intro, Methods, etc.)      │
              │                                              │
              │             Gemini 3.7 Flash                 │
              └──────────────────────┬───────────────────────┘
                                     │
                                     ▼
              ┌──────────────────────────────────────────────┐
              │        Export Pipeline (LaTeX / Markdown)    │
              └──────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

- **Framework**: Python 3.11+, FastAPI, Uvicorn
- **AI Orchestration**: Google GenAI SDK (`google-genai`), LangChain Google GenAI (`langchain-google-genai`)
- **LLM Engine**:
  - Research / Analysis: `gemini-3.6-flash`
  - Manuscript Generation: `gemini-3.7-flash`
- **Data Schemas**: Pydantic v2
- **Literature Indexing**: OpenAlex API via custom asynchronous fetching service

### Frontend

- **Core**: React 18, TypeScript, Vite
- **Icons & Styling**: Tailwind CSS, Lucide React (`lucide-react`)
- **HTTP Client**: Native Fetch API / Axios

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js v18+ and `npm` / `pnpm`
- A valid **Google Gemini API Key** ([Get API Key](https://aistudio.google.com/))

---

### 1. Backend Setup

```bash
# Clone repository
git clone https://github.com/your-username/resonance-ai.git

cd resonance-ai/backend

# Set up virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
# Add your Gemini API key to .env
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Launch API backend server
uvicorn app.main:app --reload --port 8000
```

---

### 2. Frontend Setup

```bash
# Open frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Navigate to:

```text
http://localhost:5173
```

---

##  API Endpoints

### `POST /api/research/analyze`

Extracts Research DNA, queries OpenAlex for prior literature, and synthesizes research gaps.

#### Request Body

```json
{
  "raw_ideology": "Autonomous control system for satellite positioning during solar events",
  "target_problem": "Coronal Mass Ejections cause orbital drift in low Earth orbit assets",
  "proposed_method": "Real-time trajectory prediction using time-series ML models"
}
```

---

### `POST /api/paper/generate-section`

Generates a specific academic section given the research context.

#### Request Body

```json
{
  "section_name": "Abstract",
  "dna": {},
  "papers": [],
  "gaps": [],
  "custom_instructions": "Focus on computational efficiency"
}
```

---

## Research Workflow

```text
User Research Idea
        │
        ▼
Research DNA Extraction
        │
        ▼
OpenAlex Literature Discovery
        │
        ▼
Literature Analysis
        │
        ▼
Research Gap Identification
        │
        ▼
Novelty Mapping
        │
        ▼
Manuscript Section Generation
        │
        ├── Abstract
        ├── Introduction
        ├── Related Work
        ├── Methodology
        ├── Results
        ├── Discussion
        └── Conclusion
        │
        ▼
LaTeX / Markdown Export
```

---

## AI Pipeline

Resonance AI separates research intelligence from manuscript generation.

### Phase 1 — Research Intelligence

```text
Research Idea
     ↓
Research DNA
     ↓
Literature Retrieval
     ↓
Literature Context
     ↓
Gap Analysis
     ↓
Novelty Mapping
```

**Model:** `gemini-3.6-flash`

This stage focuses on structured reasoning, extraction, literature interpretation, and research-gap identification.

### Phase 2 — Manuscript Engineering

```text
Research Context
     ↓
Section Planning
     ↓
Context-Aware Generation
     ↓
Academic Refinement
     ↓
Final Manuscript
```

**Model:** `gemini-3.7-flash`

This stage focuses on high-quality academic writing, contextual consistency, structure, and manuscript-level reasoning.

---

## 📂 Project Structure

```text
resonance-ai/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── schemas/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│
├── LICENSE
└── README.md
```

---

## Environment Variables

Create a `.env` file inside the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

If your implementation uses both environment variable names, you may configure:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

> Never commit your `.env` file or expose your API key publicly.

---

## Performance Philosophy

Resonance AI uses model specialization rather than relying on a single LLM for the entire workflow.

```text
                 RESONANCE AI
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Research Intelligence     Manuscript Engineering
          │                       │
          ▼                       ▼
 Gemini 3.6 Flash           Gemini 3.7 Flash
          │                       │
          ▼                       ▼
 Fast structured reasoning   High-quality generation
```

This separation allows the system to optimize for both **latency** and **generation quality**.

---

## 🧪 Example Research Input

```text
Research Idea:
Autonomous control systems for satellite positioning during solar events.

Target Problem:
Coronal Mass Ejections can introduce disturbances that affect
orbital prediction and positioning accuracy for low Earth orbit assets.

Proposed Method:
Use real-time trajectory prediction with time-series machine
learning models combined with space-weather observations.
```

Resonance AI transforms this into:

```text
Research DNA
      ↓
Relevant Literature
      ↓
Research Gaps
      ↓
Novelty Opportunities
      ↓
Academic Manuscript
```

---

## 📄 Output Formats

Resonance AI supports:

| Format | Extension | Purpose |
|---|---|---|
| Markdown | `.md` | Research editing and collaboration |
| LaTeX | `.tex` | Academic publication workflows |

---

## Responsible Research

Resonance AI is designed as a **research synthesis and manuscript engineering assistant**, not as a replacement for academic judgment.

Generated content should be reviewed by researchers for:

- Factual correctness
- Citation accuracy
- Methodological validity
- Statistical validity
- Research novelty
- Ethical considerations
- Plagiarism and originality
- Publication requirements

AI-generated references and claims should always be independently verified against the original academic sources.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add or update tests where appropriate.
5. Commit your changes.
6. Open a pull request.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

---

## 🗺️ Roadmap

- [x] Research DNA extraction
- [x] OpenAlex literature discovery
- [x] Research gap analysis
- [x] Novelty mapping
- [x] Modular manuscript generation
- [x] Markdown export
- [x] LaTeX export
- [ ] Citation graph visualization
- [ ] Multi-agent peer review
- [ ] Automated citation verification
- [ ] Research quality scoring
- [ ] Semantic literature clustering
- [ ] Long-term research memory
- [ ] Multi-model routing
- [ ] Autonomous research planning

---

## 📜 License

Distributed under the MIT License.

See [`LICENSE`](LICENSE) for details.

---