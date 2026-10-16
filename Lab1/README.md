# Lab 1: Requirements Engineering & UML Use Case Modelling

**System:** OpenAPI Mock Server Generator (Problem Statement #41)  
**Author:** Akshansh Agrawal (PES2UG24CS045)

## Deliverable

| File | Contents |
| --- | --- |
| [PES2UG24CS045_Lab1_SE.pdf](Requirements_and_UseCase/PES2UG24CS045_Lab1_SE.pdf) | System overview, actors, requirements table, use case description and UML use case diagram |

## Actors

| Actor | Type | Role |
| --- | --- | --- |
| API Developer | Primary | Uploads the OpenAPI spec and configures latency behaviour |
| QA Engineer | Primary | Sends requests to the mock endpoints while testing |
| CI/CD Pipeline | Secondary | Starts the mock server during automated test runs |
| System Administrator | Secondary | Handles access control, environment setup and server configuration |
| DevOps Engineer | Secondary | Monitors uptime and load during peak test runs |

## Requirements

| ID | Type | Requirement | Priority |
| --- | --- | --- | --- |
| FR-001 | Functional | Parse an OpenAPI 3.0 spec and create mock endpoints that return randomized, schema-compliant JSON | High |
| FR-002 | Functional | Validate uploaded specs and reject broken YAML/JSON with a line-numbered error | High |
| FR-003 | Functional | Let the developer set a minimum and maximum response delay per endpoint | Medium |
| FR-004 | Functional | Show the QA engineer a live list of active endpoints (path and method) | Medium |
| FR-005 | Functional | Generate randomized responses that still match schema types and required fields | High |
| NFR-001 | Non-functional | Sustain 1,000 requests per second with latency accurate to ±10 ms | High |
| NFR-002 | Non-functional | Stay available for health checks at least 99.5% of the time per session | Medium |

## Use Cases

- **UC-01** Upload Spec
- **UC-02** Parse & Validate Spec
- **UC-03** Generate Mock Endpoints
- **UC-04** Configure Latency (`<<extend>>` UC-03, because latency is optional)
- **UC-05** Send Request to Mock Endpoint (`<<include>>` UC-06, because validation always happens)
- **UC-06** Validate Response Against Schema

The report describes **UC-05** in full. It covers the preconditions, the main success scenario (upload, parse, generate, request, apply latency, build response, validate, return) and the alternate flow where schema validation fails and the system returns a 500 error, which is logged and shown on the dashboard.
