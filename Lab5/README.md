# Lab 5: Static Code Analysis

**Assigned repo:** [SETAPESU26/L5_41_library_catalog_system](https://github.com/SETAPESU26/L5_41_library_catalog_system)  
**Author:** Akshansh Agrawal (PES2UG24CS045)

A library catalog script was analysed with Pylint, Bandit and Flake8, and the reported issues were fixed.

## Deliverables

| Deliverable | Location | Contents |
| --- | --- | --- |
| Cleaned code | [Code/library_catalog_system.py](Code/library_catalog_system.py) | The fixed script (18 issues fixed) |
| Issue table | [issues.md](issues.md) | Each issue with its tool, type, line, description and fix |
| Reflection | [reflection.md](reflection.md) | Answers to the four reflection questions |
| Reports (before) | [Reports/Before/](Reports/Before/) | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` on the original code |
| Reports (after) | [Reports/After/](Reports/After/) | The same three reports on the fixed code |
| Commits | Repo history | One commit for each tool's fixes (Bandit, Flake8, Pylint) |

## Results

| Tool | Before | After |
| --- | --- | --- |
| Pylint | 5.32/10 | 10.00/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues |
| Flake8 | 6 issues | No issues |

Two problems were not flagged by any tool and were fixed as well:

- A hardcoded librarian key was printed to the console. It is now read from the `LIBRARIAN_KEY` environment variable and never printed.
- Returning a book could raise its copy count above the number the library owns. Returning B02 took it from 1 copy to 2.

## Running

```bash
cd Lab5/Code
pip install pylint bandit flake8
python library_catalog_system.py
pylint library_catalog_system.py
bandit -r library_catalog_system.py
flake8 library_catalog_system.py
```
