from fastapi import FastAPI

app = FastAPI()

prices_db: list[float] = [15.50, 99.99, 45.00, 250.00, 12.00, 500.25, 75.10]

employee_db: dict[int, str] = {
    1001: "Alice Johnson:",
    1002: "Bob Smith",
    1003: "Charlie Davis"
}
#Problem 1
@app.get("/prices")
def get_filter_price(
    min_price: Optional[float] = Query(
        None,
        ge=0.0,
        title="Minimum Price",
        description="Lower bound for price filtering (inclusive). Must be greater than or equal to 0.0. "
    ),
    max_price: Optional[float] = Query(
         None,
         le=1000.0,
         title="Maximum Price",
         description="Upper bound for price filtering (inclusive). Must be less than or equal to 1000.0. "
     )
):
    filtered = prices_db.copy()

    if min_price is not None:
        filter = [p for p in filtered if p >= min_price]
    if max_price is not None:
        filter = [p for p in filtered if p <= max_price]


    return {
        "filter_price": filter,
        "count": len(filtered)
    }


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