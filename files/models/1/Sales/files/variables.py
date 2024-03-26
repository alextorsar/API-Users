"""
Python model 'variables.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import NonNegativeInteg
from pysd import Component

__pysd_version__ = "3.12.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 0.125,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="INITIAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="sales_force adjustment_time",
    units="months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sales_force_adjustment_time():
    return 20


@component.add(
    name="indicated sales_force",
    units="people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"budget": 1, "sales_person_salary": 1},
)
def indicated_sales_force():
    return budget() / sales_person_salary()


@component.add(
    name="budget",
    units="$/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"orders_booked": 1, "revenue_to_sales": 1},
)
def budget():
    return orders_booked() * revenue_to_sales()


@component.add(
    name="revenue to_sales", units="$/SKU", comp_type="Constant", comp_subtype="Normal"
)
def revenue_to_sales():
    return 10


@component.add(
    name="sales_person salary",
    units="$/Person-Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sales_person_salary():
    return 2000


@component.add(
    name="orders booked",
    units="SKU/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sales_force": 1, "sale_effectiveness": 1},
)
def orders_booked():
    return sales_force() * sale_effectiveness()


@component.add(
    name="sale effectiveness",
    units="SKU/Person-Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_sales_effectiveness": 1,
        "effect_of_delivery_delay_recognized": 1,
    },
)
def sale_effectiveness():
    return normal_sales_effectiveness() * effect_of_delivery_delay_recognized()


@component.add(
    name="normal sales_effectiveness",
    units="SKU/Person-Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_sales_effectiveness():
    return 350


@component.add(
    name="effect_of__delivery_delay_recognized",
    units="Unitless",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"delivery_delay_recognized": 1, "normal_delivery_delay_recognized": 1},
)
def effect_of_delivery_delay_recognized():
    return np.interp(
        delivery_delay_recognized() / normal_delivery_delay_recognized(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
        [1.15, 1.1, 1.0, 0.75, 0.5, 0.35, 0.3],
    )


@component.add(
    name="normal_delivery delay_recognized",
    units="months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_delivery_delay_recognized():
    return 2


@component.add(
    name="time_for delivery_delay recognition",
    units="months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_for_delivery_delay_recognition():
    return 5


@component.add(
    name="delivery delay_impending",
    units="months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"backlog": 1, "delivery_rate": 1},
)
def delivery_delay_impending():
    return backlog() / delivery_rate()


@component.add(
    name="effect_of_backlog on_delivery_rate",
    units="Unitless",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"backlog": 1, "normal_backlog": 1},
)
def effect_of_backlog_on_delivery_rate():
    return np.interp(
        backlog() / normal_backlog(),
        [0.9, 1.0, 1.7, 2.3, 3.5, 6.3, 10.0, 20.0],
        [0.0, 1.0, 3.5, 4.3, 5.0, 5.6, 6.0, 6.5],
    )


@component.add(
    name="normal backlog", units="SKU", comp_type="Constant", comp_subtype="Normal"
)
def normal_backlog():
    return 8000


@component.add(
    name="delivery rate",
    units="SKU/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_delivery_rate": 1, "effect_of_backlog_on_delivery_rate": 1},
)
def delivery_rate():
    return normal_delivery_rate() * effect_of_backlog_on_delivery_rate()


@component.add(
    name="normal delivery_rate",
    units="SKU/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_delivery_rate():
    return 4000


@component.add(
    name="net_hires",
    units="person/mo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_sales_force": 1,
        "sales_force": 1,
        "sales_force_adjustment_time": 1,
    },
)
def net_hires():
    return (indicated_sales_force() - sales_force()) / sales_force_adjustment_time()


@component.add(
    name="change_in delivery_delay recognized",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "delivery_delay_impending": 1,
        "delivery_delay_recognized": 1,
        "time_for_delivery_delay_recognition": 1,
    },
)
def change_in_delivery_delay_recognized():
    return (
        delivery_delay_impending() - delivery_delay_recognized()
    ) / time_for_delivery_delay_recognition()


@component.add(
    name="orders entered",
    units="sku/mo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"orders_booked": 1},
)
def orders_entered():
    return np.maximum(orders_booked(), 0)


@component.add(
    name="orders completed",
    units="sku/mo",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delivery_rate": 1},
)
def orders_completed():
    return np.maximum(delivery_rate(), 0)


@component.add(
    name="Sales Force",
    units="people",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_sales_force": 1},
    other_deps={"_integ_sales_force": {"initial": {}, "step": {"net_hires": 1}}},
)
def sales_force():
    return _integ_sales_force()


_integ_sales_force = NonNegativeInteg(
    lambda: net_hires(), lambda: 10, "_integ_sales_force"
)


@component.add(
    name="Delivery Delay Recognized",
    units="months",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_delivery_delay_recognized": 1},
    other_deps={
        "_integ_delivery_delay_recognized": {
            "initial": {},
            "step": {"change_in_delivery_delay_recognized": 1},
        }
    },
)
def delivery_delay_recognized():
    return _integ_delivery_delay_recognized()


_integ_delivery_delay_recognized = NonNegativeInteg(
    lambda: change_in_delivery_delay_recognized(),
    lambda: 2,
    "_integ_delivery_delay_recognized",
)


@component.add(
    name="Backlog",
    units="SKU",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_backlog": 1},
    other_deps={
        "_integ_backlog": {
            "initial": {},
            "step": {"orders_entered": 1, "orders_completed": 1},
        }
    },
)
def backlog():
    return _integ_backlog()


_integ_backlog = NonNegativeInteg(
    lambda: orders_entered() - orders_completed(), lambda: 8000, "_integ_backlog"
)
