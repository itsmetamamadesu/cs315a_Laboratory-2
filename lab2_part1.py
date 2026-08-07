# TORRE, JIBRIELLE R.
# LAB 2 - PART 1(lab2_part1.py)
# BSCS 3-A/CSIT 315a

from fastapi import FastAPI, Query, Path
from typing import Optional, List, Dict, Any

app = FastAPI()

prices_db: list[float] = [15.50, 99.99, 45.00, 250.00, 12.00, 500.25, 75.10]

employee_db: dict[int, str] = {
    1001: "Dean is Gay",
    1002: "Meow Meow",
    1003: "Chrissie Boy",
    1004: "Soulja Boy",
    1005: "Jay-Z",
    1006: "Kanye West",
    1007: "Kendrick Lamar",
    1008: "Drake",
    1009: "Travis Scott"
}
#Problem 1
@app.get("/prices")
def get_filter_price(min_price: Optional[float] = Query(None, ge=0.0), max_price: Optional[float] = Query(None, le=1000.0)):
    if min_price and max_price is not None:
        filter = [p for p in prices_db if p >= min_price and p <= max_price]
        return {"filter_price": filter, "count": len(filter)}


#Problem 2
@app.get("/employee/{emp_id}")
def get_employee(
    emp_id: int = Path(
        ...,
        ge=1000,
        lt=10000,
        title="Employee ID Key",
        description="4-digit employee ID key. Must be between 1000 and 9999."
    )
):
    if emp_id in employee_db:
        return {
            "emp_id": emp_id,
            "name": employee_db[emp_id]
        }
    return {"error": "Employee record not found."}