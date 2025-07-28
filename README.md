# Adobe India Hackathon 2025 – Service 1B

Persona-Driven Document Intelligence

## 🧑‍💻 TEAM INFORMATION

**Team Name:** Stairway to Compliation
**Team Members:**

* Abhinivesh Mitra – [f20221311@hyderabad.bits-pilani.ac.in](mailto:f20221311@hyderabad.bits-pilani.ac.in)
* Rishit Raj – [f20220431@hyderabad.bits-pilani.ac.in](mailto:f20220431@hyderabad.bits-pilani.ac.in)
* Paarth Prakash – [f20220558@hyderabad.bits-pilani.ac.in](mailto:f20220558@hyderabad.bits-pilani.ac.in)

**Institution:** BITS Pilani, Hyderabad Campus
**Hackathon:** Adobe India Hackathon 2025 – Challenge 1B
**Submission Date:** July 28, 2025
**Contact:** [f20221311@hyderabad.bits-pilani.ac.in](mailto:f20221311@hyderabad.bits-pilani.ac.in)

---

## 💡 CHALLENGE STATEMENT

**Challenge:** Persona-Driven Document Intelligence

* **Problem:** Transform document collections into persona-specific insights by extracting and ranking content based on user roles and job requirements, delivering contextually relevant information for different professional personas.

* **Solution Approach:** Advanced semantic embedding-based analysis with persona-specific query expansion and weighted relevance scoring (70% query match + 30% persona fit) using offline-capable transformer models with extensible persona framework.

---

## ✨ INNOVATION HIGHLIGHTS

* **Offline-First Architecture:** Full processing without internet dependencies using embedded 87.6MB transformer model
* **Dynamic Persona System:** Extensible, add custom personas beyond 5 pre-configured examples
* **Weighted Semantic Scoring:** 70/30 relevance algorithm (query + persona fit) for optimal content ranking
* **Real-Time Query Expansion:** Dynamic keyword enhancement per persona via vocabulary templates
* **Zero-Dependency Processing:** Self-contained (no external calls), schema validation built in
* **Multi-Collection Parallelism:** Independent processing of multiple document collections
* **Performance Excellence:** 5.10s avg processing (90% faster than requirement)

---

## 🚀 OVERVIEW

This repository contains our Challenge 1B solution for Adobe India Hackathon 2025. Service 1B transforms document collections into persona-specific insights through advanced semantic analysis, delivering schema-compliant outputs for multiple job roles with complete offline processing and extensible persona framework.

---

## 📄 WHAT IT DOES

* Processes multiple document collections simultaneously with persona-driven analysis
* Generates semantic embeddings using all-MiniLM-L6-v2 model (87.6MB, included)
* Ranks document sections by relevance: 70% query match + 30% persona fit
* Outputs challenge1b\_output.json with extracted sections and subsection analysis
* Fully offline processing with embedded models (no internet required)
* Complete schema validation for hackathon compliance
* Extensible persona system for custom role definitions

---

## 🔹 KEY FEATURES

* **Extensible Persona Framework:** Add unlimited custom personas (beyond 5 pre-configured)
* **Lightning-Fast Processing:** Avg 5.10s per collection (tested: 10.20s for 2)
* **Hackathon Compliant:** Under 60s/collection, CPU-only, no network
* **Self-Contained:** 87.6MB model included
* **Multi-Collection:** 2–10 collections at once
* **Schema Validation:** 100% output compliance
* **Offline Intelligence:** Zero external dependencies

---

## 📁 DIRECTORY STRUCTURE

```
service-1b/
├── app/
│   ├── main.py                 # Entry point
│   ├── config/
│   │   └── settings.py         # Config
│   ├── models/round1b/
│   │   └── embedding_model/    # 87.6MB model
│   │       ├── model.safetensors
│   │       ├── config.json
│   │       ├── tokenizer.json
│   │       └── 1_Pooling/
│   ├── services/round1b/       # Core logic
│   │   ├── collection_processor.py
│   │   ├── persona_matcher.py
│   │   ├── embedding_generator.py
│   │   ├── challenge1b_input_handler.py
│   │   ├── challenge1b_output_formatter.py
│   │   └── document_loader.py
│   └── utils/                  # Utilities
│       ├── file_handler.py
│       ├── json_validator.py
│       └── logger.py
├── collections/
│   ├── Collection 1/
│   │   ├── challenge1b_input.json
│   │   ├── challenge1b_output.json
│   │   └── E0CCG5S312_outline.json
│   └── Collection 2/
│       ├── challenge1b_input.json
│       ├── challenge1b_output.json
│       └── E0H1CM114_outline.json
├── scripts/
│   ├── download_models.py
│   └── setup_collections.py
├── Dockerfile
├── requirements.txt
└── .gitignore
```

---

## 📥 INPUT FORMAT (`challenge1b_input.json`)

```json
{
  "challenge_info": {
    "challenge_id": "challenge_001",
    "test_case_name": "QA_Engineering_Analysis"
  },
  "documents": [
    {"filename": "E0CCG5S312.pdf", "title": "Agile Testing Certification Guide"}
  ],
  "persona": {
    "role": "Quality Assurance Engineer"
  },
  "job_to_be_done": {
    "task": "Prepare for agile testing certification and understand comprehensive testing methodologies for enterprise software development"
  }
}
```

---

## 📤 OUTPUT FORMAT (`challenge1b_output.json`)

```json
{
    "metadata": {
        "input_documents": [
            "E0CCG5S312.pdf"
        ],
        "persona": "Quality Assurance Engineer",
        "job_to_be_done": "Prepare for agile testing certification and understand comprehensive testing methodologies for enterprise software development"
    },
    "extracted_sections": [
        {
            "document": "E0CCG5S312.pdf",
            "section_title": "Chapter 3: Agile Testing Methods, Techniques, and Tools",
            "importance_rank": 1,
            "page_number": 11
        },
        {
            "document": "E0CCG5S312.pdf",
            "section_title": "Chapter 2: Fundamental Agile Testing Principles, Practices, and Processes",
            "importance_rank": 2,
            "page_number": 11
        },
        {
            "document": "E0CCG5S312.pdf",
            "section_title": "2. Introduction to Foundation Level Agile Tester Extension",
            "importance_rank": 3,
            "page_number": 7
        }
    ],
    "subsection_analysis": [
        {
            "document": "E0CCG5S312.pdf",
            "refined_text": "Chapter 3: Agile Testing Methods, Techniques, and Tools",
            "page_number": 11
        },
        {
            "document": "E0CCG5S312.pdf",
            "refined_text": "Chapter 2: Fundamental Agile Testing Principles, Practices, and Processes",
            "page_number": 11
        }
    ]
}
```

---

## ⚡ QUICK START

**Prerequisites:**

* Docker Desktop
* Git
* 1GB+ free disk

**Setup:**

```bash
git clone https://github.com/abhiniveshmitra/service-1b.git
cd service-1b
docker build --platform=linux/amd64 -t adobe-service-1b .
```

**Run Service 1B:**

```bash
docker run --rm -v "${PWD}/collections:/app/collections" --network none adobe-service-1b
```

**Expected Output:**

* Each collection processed in \~5s with persona-specific analysis
* Schema-validated `challenge1b_output.json` files generated
* Complete processing under 60 seconds total

---

## 🔄 PROCESSING PIPELINE

1. **Collection Discovery:** Scans `collections/` for folders with `challenge1b_input.json`
2. **Input Validation:** Validates Challenge 1B specification compliance
3. **Document Loading:** Loads pre-extracted PDF outlines (JSON)
4. **Persona Analysis:** Role-specific query expansion & weighting
5. **Semantic Embedding:** 384-d vectors via local model
6. **Relevance Ranking:** 70% query + 30% persona weighting
7. **Output Generation:** Schema-compliant output JSON
8. **Validation:** Auto schema validation (hackathon compliance)

---

## 🧑‍🔬 PERSONA SYSTEM (EXTENSIBLE)

Our system supports unlimited custom personas. Pre-configured examples:

* **QA Engineer:** Testing procedures, quality assurance, validation protocols, certification paths
* **Data Scientist:** Machine learning, analytics, statistical analysis, modeling techniques
* **Digital Transformation Consultant:** Digital strategy, process improvement, technology adoption
* **Product Manager:** Product requirements, roadmap planning, user experience, business strategy
* **Software Engineer:** Technical implementation, system architecture, development practices

**Adding Custom Personas:**

1. Define persona-specific keywords in `persona_matcher.py`
2. Add vocabulary templates as needed
3. Rebuild Docker image for deployment

---

## 🌟 PERFORMANCE METRICS

* **Processing Speed:** 5.10s avg/collection (tested)
* **Memory Usage:** <1GB peak
* **Model Size:** 87.6MB (10x under limit)
* **Semantic Accuracy:** 384-dim embeddings, cosine similarity
* **Schema Validation:** 100% pass
* **Network:** None (fully offline)

---

## ✅ HACKATHON COMPLIANCE

| Technical Requirement              | Status |
| ---------------------------------- | ------ |
| ≤ 60 seconds per collection        | ✅      |
| Model size ≤ 1GB                   | ✅      |
| Multi-Collection (2-10)            | ✅      |
| CPU-only, no GPU                   | ✅      |
| Network isolation (--network none) | ✅      |
| Docker linux/amd64                 | ✅      |
| Persona-Driven Analysis (5+)       | ✅      |
| Schema Compliance                  | ✅      |
| Input/Output Format                | ✅      |
| Offline Processing                 | ✅      |

---

## 🔗 RESOURCES

* Repo: [https://github.com/abhiniveshmitra/service-1b](https://github.com/abhiniveshmitra/service-1b)
* Model: all-MiniLM-L6-v2 (87.6MB)
* Support: GitHub Issues tab
* Docs: Inline code comments + test samples

---

## 🚀 FINAL STATUS

This Service 1B implementation delivers a production-ready, extensible, and offline-first persona-driven document intelligence system—optimized for Adobe India Hackathon 2025 requirements.
