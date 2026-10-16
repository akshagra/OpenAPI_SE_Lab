# OpenAPI_SE_Lab

Software Engineering lab work for **Problem Statement #41: OpenAPI Mock Server Generator**.

**Author:** Akshansh Agrawal  
**SRN:** PES2UG24CS045

## Problem Statement

An OpenAPI Mock Server Generator reads an existing OpenAPI 3.0 spec and turns it into a working fake API, so developers and testers don't have to wait for a real backend before they start working.

The system:

- Parses and validates an uploaded OpenAPI 3.0 spec (YAML or JSON) and rejects broken files with a line-numbered error.
- Generates mock HTTP endpoints for every path in the spec.
- Returns randomized responses that still match the schema's types and required fields.
- Lets the developer set a minimum and maximum response delay per endpoint to simulate real network conditions.
- Runs inside a CI/CD pipeline, giving test suites a stable target when the real backend is incomplete or down.

Its main users are API Developers and QA Engineers. A CI/CD Pipeline, a System Administrator and a DevOps Engineer are supporting actors.

## Labs

| Lab | Topic | Summary | Deliverables |
| --- | --- | --- | --- |
| [Lab 1](Lab1/) | Requirements Engineering & UML Use Case Modelling | Identifies the five actors, lists the functional and non-functional requirements (FR-001 to FR-005, NFR-001 and NFR-002), describes six use cases in detail, and draws the UML use case diagram. | [Requirements & Use Case report](Lab1/Requirements_and_UseCase/) |
| [Lab 2](Lab2/) | Agile Backlog Creation & Sprint Simulation | Builds a prioritized, story-pointed product backlog, runs it across two simulated sprints with boards and a burndown chart, and reflects on how accurate the estimates were and how much the team could deliver. | [Backlog, sprints & reflection report](Lab2/Agile_Backlog_and_Sprint/) |
| [Lab 3](Lab3/) | Component Modelling & Architectural Pattern Selection | Models the system as a three-layer architecture (Presentation, Business, Data) in a UML component diagram, and explains why a layered pattern was chosen, including its security and performance benefits. | [Component diagram](Lab3/Component_Diagram/), [Written justification](Lab3/Written_Justification/) |
| [Lab 4](Lab4/) | VibeCoding | Uses an AI coding assistant to fix and extend a Pygame Fruit Ninja game: reliable fast-swipe slicing, a Game Over screen, replay at Easy/Medium/Hard, and sound effects. | [Videos](Lab4/Videos/), [Code](Lab4/Code/), [Chat history](Lab4/Chat_History/) |

## Repository Structure

```
OpenAPI_SE_Lab/
├── Lab1/
│   └── Requirements_and_UseCase/
│       └── PES2UG24CS045_Lab1_SE.pdf
├── Lab2/
│   └── Agile_Backlog_and_Sprint/
│       └── PES2UG24CS045_Lab2_SE.pdf
├── Lab3/
│   ├── Component_Diagram/
│   │   └── PES2UG24CS045_SE_Lab3_Diagram.pdf
│   └── Written_Justification/
│       └── PES2UG24CS045_SE_Lab3_Justification.pdf
├── Lab4/
│   ├── Videos/
│   ├── Code/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── game/
│   │       ├── fruit.py
│   │       ├── game_engine.py
│   │       └── sounds.py
│   └── Chat_History/
├── LICENSE
└── README.md
```

Each lab folder has its own README with more detail.
