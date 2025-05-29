"""
powerplant_dispatcher.py

This module defines a system for calculating the most cost-efficient way to dispatch power 
across a set of power plants, based on fuel prices, plant efficiencies, and load requirements.

Classes:
    FieldName:
        Provides constant keys used for referencing data fields in input dictionaries.

    Fuel:
        Parses and stores current fuel prices and wind availability from the input data.

    PowerPlant:
        Models a single power plant with relevant technical parameters.

    ResumePowerPlant:
        Responsible for computing power generation and dispatching load based on
        cost optimization logic.

Usage:
    Given an input JSON-like dictionary with keys "load", "fuels", and "powerplants",
    instantiate a `ResumePowerPlant` object and call `compute_production_plan()` to get 
    the production plan.

Example:
    data = {
        "data": {
            "load": 480,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
                {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150}
            ]
        }
    }

    dispatcher = ResumePowerPlant(data)
    production_plan = dispatcher.compute_production_plan()

Notes:
    - Wind turbines are prioritized with zero cost but variable output.
    - Fossil fuel plants include CO2 emission costs in their cost calculation.
    - Plants that cannot operate at their minimum generation level due to low remaining load
      are skipped or assigned 0.0 production.

Author: Francisco Rodriguez Alfaro
Version: 1.0
"""

import numpy as np
from .exceptions import ExceptionCalculatingOptimizedData, ExceptionCostResume, ExceptionSortedPlants

class FieldName:
    """
    Constant field names used in data objects for consistent access.
    """
    load = "load"
    gas = "gas(euro/MWh)"
    kerosine = "kerosine(euro/MWh)"
    co2 = "co2(euro/ton)"
    wind = "wind(%)"

    name = "name"
    type = "type"
    efficiency = "efficiency"
    pmin = "pmin"
    pmax = "pmax"

    potencia = "potencia"  # Custom field: power produced
    coste = "coste"        # Custom field: cost of production


class Fuel:
    """
    Stores fuel prices and wind availability from the input payload.

    Attributes:
        gas (float): Price of gas in euro/MWh.
        kerosine (float): Price of kerosine in euro/MWh.
        co2 (float): Price of CO2 emissions in euro/ton.
        wind (float): Wind availability as a percentage (0–100).
    """

    def __init__(self, data_object_fuels):
        self.gas = data_object_fuels.get(FieldName.gas)
        self.kerosine = data_object_fuels.get(FieldName.kerosine)
        self.co2 = data_object_fuels.get(FieldName.co2)
        self.wind = data_object_fuels.get(FieldName.wind)


class PowerPlant:
    """
    Represents a power plant with its technical specifications.

    Attributes:
        name (str): Name of the power plant.
        type (str): Type of power plant (e.g., gasfired, turbojet, windturbine).
        efficiency (float): Fuel-to-electricity conversion efficiency.
        pmin (float): Minimum power generation in MWh.
        pmax (float): Maximum power generation in MWh.
    """

    def __init__(self, data_object_powerplant):
        self.name = data_object_powerplant.get(FieldName.name)
        self.type = data_object_powerplant.get(FieldName.type)
        self.efficiency = data_object_powerplant.get(FieldName.efficiency)
        self.pmin = data_object_powerplant.get(FieldName.pmin)
        self.pmax = data_object_powerplant.get(FieldName.pmax)


class ResumePowerPlant:
    """
    Calculates cost-effective power dispatch from a set of power plants.

    Class Attributes:
        factor_emision_co2 (float): CO2 emission factor applied to fossil fuel generation.

    Instance Attributes:
        load (float): Total load (MWh) to be satisfied.
        fuels (Fuel): Fuel pricing and wind conditions.
        powerplants (list[PowerPlant]): List of available power plants.
    """

    load = None
    fuels = None
    powerplants = None
    factor_emision_co2 = 0.3  # CO2 tons per MWh

    def __init__(self, data):
        """
        Initializes the dispatch engine with the input dataset.
        """
        data_object = data.get("data")
        self.load = data_object.get(FieldName.load)
        self.fuels = ResumePowerPlant.get_fuels(data_object.get("fuels"))
        self.powerplants = ResumePowerPlant.get_powerplants(data_object.get("powerplants"))

    @staticmethod
    def get_fuels(data_object_fuels):
        """Creates a Fuel instance from the fuels data dictionary."""
        return Fuel(data_object_fuels)

    @staticmethod
    def get_powerplants(data_object_powerplants):
        """Creates a list of PowerPlant objects from input data."""
        return [PowerPlant(plant) for plant in data_object_powerplants]

    def calculate_power_costs(self):
        """
        Calculates the potential production and cost for each plant.

        Returns:
            list[PowerPlant]: Plants with added attributes for 'potencia' and 'coste'.
        """
        summary = []

        for plant in self.powerplants:
            if plant.type == "windturbine":
                potencia = plant.pmax * (self.fuels.wind / 100)
                coste = 0
            else:
                # Determine the base fuel cost
                if plant.type == "gasfired":
                    fuel_cost = self.fuels.gas
                elif plant.type == "turbojet":
                    fuel_cost = self.fuels.kerosine
                else:
                    fuel_cost = 0  # Unknown type

                potencia = 0
                coste = (fuel_cost / plant.efficiency) + (self.factor_emision_co2 * self.fuels.co2)

            setattr(plant, FieldName.potencia, potencia)
            setattr(plant, FieldName.coste, coste)
            summary.append(plant)

        return summary

    def compute_production_plan(self):
        """
        Dispatches power generation starting from the cheapest sources.

        Returns:
            list[dict]: List of {"name": str, "p": float} per plant.
        """        
        try:
            summary = self.calculate_power_costs()
        except:
            raise ExceptionCostResume("Error calculating plant costs")
        
        try:
            # Prioritize wind turbines, then fossil plants
            wind_plants = sorted(
                filter(lambda x: x.type == "windturbine", summary),
                key=lambda x: x.coste
            )
            fossil_plants = sorted(
                filter(lambda x: x.type != "windturbine", summary),
                key=lambda x: (-x.efficiency, x.pmin)
            )
            sorted_plants = wind_plants + fossil_plants
        except:
            raise ExceptionSortedPlants("Error sorting plants by cost")

        remaining_load = self.load
        result = []
        temp_result = []

        try:
            def can_assign_value(index, sorted_plants, remaining_load, value):
                """
                Checks if assigning 'value' to the current plant allows satisfying
                the remaining load given the minimum requirement of the next plant.
                """
                remaining_after_value = remaining_load - value
                if int(remaining_after_value) == 0:
                    return True

                if len(sorted_plants) <= index + 1:
                    return False

                next_plant = sorted_plants[index + 1]
                min_required = next_plant.pmin

                if value <= remaining_load - min_required:
                    return True

                return False

            for index, plant in enumerate(sorted_plants):
                if plant.type == "windturbine" and plant.potencia <= 0:
                    continue

                if plant.type == "windturbine":
                    plant.pmin = plant.potencia
                    plant.pmax = plant.potencia

                plant.pmin = float(plant.pmin)
                plant.pmax = float(plant.pmax)

                for value in np.arange(plant.pmax, plant.pmin - 1, -1):
                    if can_assign_value(index, sorted_plants, remaining_load, value):
                        remaining_load -= value
                        if remaining_load < 0:
                            value += remaining_load
                            remaining_load = 0

                        temp_result.append({
                            "name": plant.name,
                            "p": round(value, 2)
                        })
                        break

            for plant in sorted_plants:
                obj = { "name": plant.name, "p": 0.0 }
                for row in temp_result:
                    if obj["name"] == row["name"]:
                        obj["p"] = row["p"]
                result.append(obj)

        except:
            raise ExceptionCalculatingOptimizedData("Error calculating optimized data")

        return result
