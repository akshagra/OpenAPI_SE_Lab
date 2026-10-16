# Lab 3: Component Modelling & Architectural Pattern Selection

**System:** OpenAPI Mock Server Generator (Problem Statement #41)  
**Author:** Akshansh Agrawal (PES2UG24CS045)

## Deliverables

| Deliverable | File | Contents |
| --- | --- | --- |
| Component Diagram | [PES2UG24CS045_SE_Lab3_Diagram.pdf](Component_Diagram/PES2UG24CS045_SE_Lab3_Diagram.pdf) | UML component diagram of the layered architecture with provided and required interfaces |
| Written Justification | [PES2UG24CS045_SE_Lab3_Justification.pdf](Written_Justification/PES2UG24CS045_SE_Lab3_Justification.pdf) | Why a layered architecture was chosen, plus its security and performance benefits |

## Architecture: Layered

| Layer | Components | Responsibility |
| --- | --- | --- |
| Presentation | Dashboard UI | Upload specs, view live endpoints, configure latency |
| Business / Application | Spec Manager, Mock Engine, Response Validator | Parse and validate the spec, generate endpoints and apply latency, check responses against the schema |
| Data | Data Store | Store specs, endpoint configuration and request logs |

**Interfaces in the diagram:** `ISpecUpload`, `IEndpointConfig`, `IParsedSpec`, `IValidateResponse`, `IStoreSpec` and `IPersistence`. Requests move down through the layers and responses move back up. The UI never talks to the Data Store directly.

## Justification Summary

1. **Matches the request lifecycle.** Parsing, endpoint generation, response building and validation each map to one business-layer component.
2. **Each layer can be tested and changed on its own.** Business components can be tested without the UI, and the Data Store can change from a file to a database without touching the Mock Engine.

- **Security:** The Data layer can only be reached through the Business layer, so access checks and input validation happen in one place. Broken or malicious specs are rejected before they are stored.
- **Performance:** The Mock Engine can cache parsed specs and generated endpoints in memory, which helps it reach the 1,000 requests per second target (NFR-001).
