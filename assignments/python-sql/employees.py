# 2025-11-30-16-12-32

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Float,
    ForeignKey,
    select,
    Result,
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List, Union, Tuple
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine("sqlite:///employees.db")

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String, nullable=False, unique=True)
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department"
    )


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String, nullable=False)
    age = mapped_column(Integer)
    salary = mapped_column(Float)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(back_populates="employees")


Base.metadata.create_all(engine)


def add_department(department: str) -> Department:
    department_existing = (
        session.query(Department).filter(Department.name == department).first()
    )
    department_new: Department
    if not department_existing:
        department_new = Department(name=department)
        session.add(department_new)
        session.commit()

        return department_new
    else:
        return department_existing


def add_department_input() -> None:
    input_department = str(input("Department name: "))

    add_department(input_department)


def add_employee() -> None:
    input_employee_name = str(input("Employee name: "))
    input_employee_age = int(input("Employee age: "))
    input_employee_salary = float(input("Employee salary: "))
    input_employee_department = str(input("Employee department: "))

    department = add_department(input_employee_department)

    session.add(
        Employee(
            name=input_employee_name,
            age=input_employee_age,
            salary=input_employee_salary,
            department=department,
        )
    )
    session.commit()


def update_employee_salary() -> None:
    input_employee_id = int(input("Employee id: "))

    employee_existing = (
        session.query(Employee).filter(Employee.id == input_employee_id).first()
    )

    if employee_existing:
        employee_existing.salary = float(input("New salary: "))
        session.commit()
    else:
        print(f"Emyloyee with id {input_employee_id} does not exist!")


def delete_employee() -> None:
    input_employee_id = float(input("Employee id: "))

    employee_existing = (
        session.query(Employee).filter(Employee.id == input_employee_id).first()
    )

    if employee_existing:
        session.delete(employee_existing)
        session.commit()
    else:
        print(f"Employee with id {input_employee_id} does not exist!")


def database_to_table(employees: Result[Tuple[Employee]]):
    # FIXME Mypy warning: "By default the bodies of untyped functions are not checked, consider using --check-untyped-defs". After an hour of searching I still don't know which function it's referring to.
    table: List[List[Union[int, str, float]]] = []
    for employee in employees.scalars():
        table += [
            [
                employee.id,
                employee.name,
                employee.age,
                employee.salary,
                employee.department.name,
            ]
        ]

    return table


def view_all_employees():
    # employees = session.query(Employee).order_by(Employee.id.desc()).all()

    employees = session.execute(select(Employee).join(Employee.department))

    print("\nAll employees sorted by id: ")

    table = database_to_table(employees)

    print(
        tabulate(
            table,
            headers=["id", "name", "age", "salary", "department"],
            tablefmt="orgtbl",
        )
    )


def count_employees_in_each_department() -> None:
    employees = session.execute(select(Employee).join(Employee.department))

    table = database_to_table(employees)

    df = pd.DataFrame(
        table,
        columns=["id", "name", "age", "salary", "department"],
    )

    employees_per_department = df["department"].value_counts()

    print(employees_per_department)

    employees_per_department.plot(kind="bar")
    plt.xlabel("Department")
    plt.ylabel("Count")
    plt.title("Employees per department")
    plt.show()


def menu() -> None:
    while True:
        print("\nEmployee Management System")
        print("1. Add department")
        print("2. Add employee")
        print("3. Update employee salary")
        print("4. Delete employee")
        print("5. View all employees")
        print("6. Show employee count by department")
        print("7. Exit")
        choice = int(input("Please enter a menu number: "))
        if choice == 1:
            add_department_input()
        elif choice == 2:
            add_employee()
        elif choice == 3:
            update_employee_salary()
        elif choice == 4:
            delete_employee()
        elif choice == 5:
            view_all_employees()
        elif choice == 6:
            count_employees_in_each_department()
        elif choice == 7:
            print("\nExiting.")
            session.close
            break
        else:
            print(
                f"\n'{choice}' is not a valid option, please enter a number between 1 and 7.\n"
            )


menu()
