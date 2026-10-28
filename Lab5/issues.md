# Issues Found and Fixed

Tools: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python 3.14).
Line numbers refer to the original `Code/library_catalog_system.py`.
Reports are in `Reports/Before/` and `Reports/After/`.

## Summary

| Tool   | Before                         | After            |
|--------|--------------------------------|------------------|
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues    |
| Flake8 | 6 issues                       | No issues        |
| Pylint | 5.32/10 (22 messages)          | 10.00/10         |

## Issue Table

High and medium severity first.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Shell command injection (Bandit B605, High) | Security | 58 | `os.system("echo ... " + filename)` passes the filename to a shell, so a filename like `x; del *` would run arbitrary commands. | Removed the shell call and used `print()` to show the message. |
| 2 | Weak MD5 hash (Bandit B324, High) | Security | 47 | MD5 is broken and should not be used to hash patron identifiers. | Switched to `hashlib.sha256`. |
| 3 | Use of `eval` (Bandit B307 Medium, Pylint W0123) | Security | 40-43 | `calculate_fine` evaluated an expression string passed in by the caller, so arbitrary code could run. | Replaced the expression string with a numeric `rate_per_day=2.0` argument and compute `days_overdue * rate_per_day`. Negative days raise `ValueError`. |
| 4 | Hardcoded secret printed to output | Security (not flagged by tools) | 62, 70 | `librarian_key = "MASTER_LIB_ACCESS_TOKEN_2026"` is hardcoded in source and printed to the console. | Read it from the `LIBRARIAN_KEY` environment variable and print only whether it is set. |
| 5 | Mutable default argument (Pylint W0102) | Bug | 15 | `active_issues=[]` is created once and shared by every call, so issue records leak between calls. | Default changed to `None` and a new list is created inside the function. |
| 6 | Bare `except: pass` (Bandit B110, Flake8 E722, Pylint W0702) | Bug / Security | 24-27 | Every error was silently swallowed, including typos and `KeyboardInterrupt`. | Catch only `KeyError`, report the unknown id, and return `False`. |
| 7 | Returns can exceed copies owned | Logic bug (not flagged by tools) | 23-25, 64 | `return_book("B02")` raised B02 from 1 to 2 copies even though the library owns only 1 and none was issued. The tools did not flag this. It showed up in the exported catalog. | Added a `total` field per book. `return_book` refuses a return when `copies >= total`. |
| 8 | Weak random PIN (Bandit B311, Low) | Security | 51 | `random.randint` is predictable and not suitable for PINs. | Used `secrets.randbelow(9000) + 1000`. |
| 9 | File opened without `with` / encoding (Pylint R1732, W1514) | Bug | 55-57 | The file is not closed if `write` fails, and the encoding depends on the platform. | `with open(filename, "w", encoding="utf-8") as f:`. |
| 10 | Unused import `csv` (Flake8 F401, Pylint W0611) | Style | 6 | Imported but never used. | Removed. |
| 11 | Unused variables `late_fee`, `days` (Flake8 F841, Pylint W0612) | Style | 31, 41 | Assigned but never used. `days` was actually used by the `eval` string, so this was a hidden dependency. | Removed `late_fee`. `days` went away with the `eval` fix. |
| 12 | `== None` comparison (Flake8 E711, Pylint C0121) | Style | 32 | Should use identity comparison. | `is None`. |
| 13 | Non-snake_case name `issueBook` (Pylint C0103) | Style | 15 | Violates PEP 8 naming. | Renamed to `issue_book` and updated the caller. |
| 14 | Missing docstrings (Pylint C0116) | Style | 15, 23, 30, 40, 46, 50, 54, 61 | Functions had no documentation. | Added a docstring to every function. |
| 15 | `%` formatting (Pylint C0209) | Style | 19 | Older formatting style. | Changed to an f-string. |
| 16 | Simplifiable if / else after return (Pylint R1703, R1705) | Style | 34-37 | `if x: return True else: return False`. | `return catalog[book_id]["copies"] > 0`. |
| 17 | No final newline (Flake8 W292, Pylint C0304) | Style | 73 | File did not end with a newline. | Added one. |
| 18 | `main()` called at import time | Style | 73 | Importing the module ran the demo and wrote a file. | Wrapped it in `if __name__ == "__main__":`. |

## Commits

1. `Fix security issues reported by Bandit`: issues 1, 2, 3, 4, 6, 7, 8
2. `Fix style issues reported by Flake8`: issues 10, 11, 12, 17
3. `Fix code quality issues reported by Pylint`: issues 5, 9, 13, 14, 15, 16, 18
