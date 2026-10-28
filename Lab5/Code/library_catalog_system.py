"""Library catalog management module."""

import hashlib
import os
import secrets

catalog = {
    "B01": {"title": "Clean Code", "copies": 3, "total": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1, "total": 1},
    "B03": {"title": "Design Patterns", "copies": 2, "total": 2},
}


def issue_book(book_id, patron, active_issues=None):
    """Issue one copy of a book to a patron.

    Returns True if a copy was issued, False if the book is unknown
    or no copies are left.
    """
    if active_issues is None:
        active_issues = []
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return one copy of a book to the shelf.

    Returns False if the book is unknown or all copies are already in.
    """
    try:
        book = catalog[book_id]
    except KeyError:
        print("Unknown book id:", book_id)
        return False
    if book["copies"] >= book["total"]:
        print("All copies of", book_id, "are already on the shelf")
        return False
    book["copies"] += 1
    return True


def check_availability(book_id):
    """Return True if at least one copy of the book is on the shelf."""
    if catalog.get(book_id) is None:
        return False
    return catalog[book_id]["copies"] > 0


def calculate_fine(days_overdue, rate_per_day=2.0):
    """Return the fine for a book that is days_overdue days late."""
    if days_overdue < 0:
        raise ValueError("days_overdue cannot be negative")
    return days_overdue * rate_per_day


def generate_patron_hash(patron_id):
    """Return a SHA-256 hex digest of the patron id."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Return a random 4-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    """Write the catalog to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(catalog))
    print("Catalog backup exported to:", filename)


def main():
    """Run a short demo of the catalog operations."""
    librarian_key = os.environ.get("LIBRARIAN_KEY")
    issue_book("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian Key initialized:", librarian_key is not None)


if __name__ == "__main__":
    main()
