from dataclasses import dataclass
from enum import Enum
from typing import List


class DefinitionOptions(Enum):
    SITE_CODE = 'site_code'
    LOCATION = 'location'
    DEVICE_TYPE = 'device_type'
    DEVICE_ROLE = 'device_role'

    def __str__(self):
        return self.value


class DeviceTypes(Enum):
    ROUTER = 'rtr'
    SWITCH = 'sw'
    FIREWALL = 'fw'

    def __str__(self):
        return self.value


class DeviceRoles(Enum):
    DATA_CENTER = 'dc'
    TOP_OF_RACK = 'tor'
    BACKBONE = 'bb'
    CORE = 'core'
    EDGE = 'edge'

    def __str__(self):
        return self.value


class PatternDefinition:
    def __init__(self, options: List[DefinitionOptions], seperator: str = '_'):
        self.options = options
        self.sep = seperator


def _build_hostname(definition, sep='-', upper: bool = False, lower: bool = False, **kwargs):
    def map_function(item):
        if isinstance(item, Enum):
            return item.value

        return item

    _values = []
    for option in definition.options:
        _values.append(kwargs.get(option.value))

    _mapped_values = list(map(map_function, _values))

    _hostname = f'{sep}'.join(_mapped_values)

    if lower and upper:
        raise Exception("Invalid Option, Must be upper or lower")

    if lower:
        return _hostname.lower()

    elif upper:
        return _hostname.upper()

    else:
        return _hostname

    # return f'{location}-{site_code}-{device_type}'.lower()


def main():
    device_configs = [
        {
            "location": "mco",
            "device_role": DeviceRoles.BACKBONE,
            "device_type": DeviceTypes.ROUTER,
        },
        {
            "location": "mco",
            "device_role": DeviceRoles.BACKBONE,
            "device_type": DeviceTypes.SWITCH,
        }
    ]


    definition = PatternDefinition(
        options=[
            DefinitionOptions.LOCATION,
            DefinitionOptions.DEVICE_ROLE,
            DefinitionOptions.DEVICE_TYPE,
            DefinitionOptions.SITE_CODE,
        ]
    )

    for index, config in enumerate(device_configs):
        hostname = _build_hostname(
            definition=definition,
            lower=True,
            site_code=str(index + 1),
            **config
        )

        print(hostname)


if __name__ == "__main__":
    main()
