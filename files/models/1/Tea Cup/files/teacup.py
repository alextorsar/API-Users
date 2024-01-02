"""
Python model 'teacup.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.12.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0.0,
    "final_time": lambda: 30.0,
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


@component.add(name="INITIAL TIME", comp_type="Constant", comp_subtype="Normal")
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(name="FINAL TIME", comp_type="Constant", comp_subtype="Normal")
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(name="TIME STEP", comp_type="Constant", comp_subtype="Normal")
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
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


@component.add(name="Characteristic Time", comp_type="Constant", comp_subtype="Normal")
def characteristic_time():
    return 10


@component.add(
    name="Heat Loss to Room",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "teacup_temperature": 1,
        "room_temperature": 1,
        "characteristic_time": 1,
    },
)
def heat_loss_to_room():
    """
    Heat Loss to Room
    """
    return (teacup_temperature() - room_temperature()) / characteristic_time()


@component.add(
    name="Room Temperature",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_room_temperature": 1},
    other_deps={
        "_integ_room_temperature": {"initial": {}, "step": {"heat_loss_to_room": 1}}
    },
)
def room_temperature():
    """
    Ambient Room Temperature
    """
    return _integ_room_temperature()


_integ_room_temperature = Integ(
    lambda: heat_loss_to_room(), lambda: 70, "_integ_room_temperature"
)


@component.add(
    name="Teacup Temperature",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_teacup_temperature": 1},
    other_deps={
        "_integ_teacup_temperature": {"initial": {}, "step": {"heat_loss_to_room": 1}}
    },
)
def teacup_temperature():
    """
    The average temperature of the tea and the cup
    """
    return _integ_teacup_temperature()


_integ_teacup_temperature = Integ(
    lambda: -heat_loss_to_room(), lambda: 180, "_integ_teacup_temperature"
)
