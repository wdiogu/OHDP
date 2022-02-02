from concurrent.futures import process
import traceback as _traceback
import time as _time
import multiprocessing
from typing import DefaultDict
import inro.modeller as _m
from contextlib import contextmanager
import random

_m.TupleType = object
_m.ListType = list
_m.InstanceType = object
_trace = _m.logbook_trace
_write = _m.logbook_write
_MODELLER = _m.Modeller()
_bank = _MODELLER.emmebank
_util = _MODELLER.module("tmg2.utilities.general_utilities")


class AssignTransit(_m.Tool()):

    def _create_temp_attribute(
        self,
        scenario,
        attribute_id,
        attribute_type,
        description=None,
        default_value=0.0,
        assignment_type=None
    ):
        """
        Creates a temporary extra attribute in a given scenario
        """
        ATTRIBUTE_TYPES = ["NODE", "LINK", "TURN",
                           "TRANSIT_LINE", "TRANSIT_SEGMENT"]
        attribute_type = str(attribute_type).upper()
        # check if the type provided is correct
        if attribute_type not in ATTRIBUTE_TYPES:
            raise TypeError(
                "Attribute type '%s' provided is not recognized." % attribute_type
            )
        if len(attribute_id) > 18:
            raise ValueError(
                "Attribute id '%s' can only be 19 characters long with no spaces plus no '@'."
                % attribute_id
            )
        prefix = str(attribute_id)
        attrib_id = ""
        if assignment_type == "transit":
            temp_extra_attribute = self.process_transit_attribute(
                scenario, prefix, attribute_type, default_value)
        elif assignment_type == "traffic":
            temp_extra_attribute = self.process_traffic_attribute(
                scenario, prefix, attribute_type, default_value)
        else:
            raise Exception(
                "Attribute type is \'None\' or \'invalid\'."
                "Type can only be either \'transit\' or \'traffic\'.")
        attrib_id = temp_extra_attribute[1]
        msg = "Created temporary extra attribute %s in scenario %s" % (
            attrib_id,
            scenario.id,
        )
        if description:
            temp_extra_attribute[0].description = description
            msg += ": %s" % description
        _write(msg)
        return temp_extra_attribute[0]

    def process_transit_attribute(self, scenario, prefix, attribute_type, default_value):
        while True:
            if prefix.startswith("@"):
                transit_attrib_id = "%s" % (prefix)
            else:
                transit_attrib_id = "@%s" % (prefix)
            checked_extra_attribute = scenario.extra_attribute(
                transit_attrib_id)
            if checked_extra_attribute == None:
                temp_transit_attrib = scenario.create_extra_attribute(
                    attribute_type, transit_attrib_id, default_value
                )
                break
            elif (
                checked_extra_attribute != None
                and checked_extra_attribute.extra_attribute_type == attribute_type
            ):
                raise Exception(
                    "Attribute %s already exist or has some issues!" % transit_attrib_id
                )
            else:
                temp_transit_attrib = scenario.extra_attribute(transit_attrib_id).initialize(
                    default_value
                )
                break
        return temp_transit_attrib, transit_attrib_id

    def process_traffic_attribute(self, scenario, prefix, attribute_type, default_value):
        if prefix != "@tvph" and prefix != "tvph":
            while True:
                suffix = random.randint(1, 999999)
                if prefix.startswith("@"):
                    traffic_attrib_id = "%s%s" % (prefix, suffix)
                else:
                    traffic_attrib_id = "@%s%s" % (prefix, suffix)

                if scenario.extra_attribute(traffic_attrib_id) is None:
                    temp_traffic_attrib = scenario.create_extra_attribute(
                        attribute_type, traffic_attrib_id, default_value
                    )
                    break
        else:
            traffic_attrib_id = prefix
            if prefix.startswith("@"):
                traffic_attrib_id = "%s" % (prefix)
            else:
                traffic_attrib_id = "@%s" % (prefix)

            if scenario.extra_attribute(traffic_attrib_id) is None:
                temp_traffic_attrib = scenario.create_extra_attribute(
                    attribute_type, traffic_attrib_id, default_value
                )
                _write("Created extra attribute '@tvph'")
            else:
                temp_traffic_attrib = scenario.extra_attribute(
                    traffic_attrib_id).initialize(0)
        return temp_traffic_attrib, traffic_attrib_id
