from abc import ABC, abstractmethod
from enum import Enum

class DmsCoordinate:
    """
    Represents a geographical coordinate in Degrees, Minutes, Seconds (DMS) format.
    """
    def __init__(self, lat_degrees: int, lat_minutes: int, lat_seconds: int,
                 lon_degrees: int, lon_minutes: int, lon_seconds: int):
        
        self.lat_degrees = lat_degrees
        self.lat_minutes = lat_minutes
        self.lat_seconds = lat_seconds
        self.lon_degrees = lon_degrees
        self.lon_minutes = lon_minutes
        self.lon_seconds = lon_seconds

    @staticmethod
    def _check_value(value: int, min_value: int, max_value: int, name: str) -> None:
        """
        Validates a coordinate component to ensure it is within an acceptable range
        and has the correct type.

        :param value: The value to check (e.g., degrees, minutes, or seconds)
        :param min_value: Minimum acceptable value
        :param max_value: Maximum acceptable value
        :param name: Name of the coordinate component (used for error messages)
        :raises TypeError: If any parameter has the wrong type
        :raises ValueError: If value is out of bounds or name is empty
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int):
            raise TypeError("Parameters 'min_value' and 'max_value' must be integer numbers")
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string")
        if not name.strip():
            raise ValueError('Parameter name can not be empty')
        
        if not isinstance(value, int):
            raise TypeError(f"'{name}' must be an integer number")

        if not min_value <= value <= max_value:
            raise ValueError(f"'{name}' must be in range [{min_value};{max_value}]")

    @property
    def lat_degrees(self) -> int:
        """Returns the degrees component of latitude."""
        return self.__lat_degrees
    
    @lat_degrees.setter
    def lat_degrees(self, value) -> None:
        """Sets value for the degrees component of latitude."""
        self._check_value(value, -90, 90, 'Degrees component of latitude')
        self.__lat_degrees = value

    @property
    def lat_minutes(self) -> int:
        """Returns the minutes component of latitude."""
        return self.__lat_minutes
    
    @lat_minutes.setter
    def lat_minutes(self, value) -> None:
        """Sets value for the minutes component of latitude."""
        self._check_value(value, 0, 59, 'Minutes component of latitude')
        self.__lat_minutes = value

    @property
    def lat_seconds(self) -> int:
        """Returns the seconds component of latitude."""
        return self.__lat_seconds
    
    @lat_seconds.setter
    def lat_seconds(self, value) -> None:
        """Sets value for the seconds component of latitude."""
        self._check_value(value, 0, 59, 'Seconds component of latitude')
        self.__lat_seconds = value

    @property
    def lon_degrees(self) -> int:
        """Returns the degrees component of longitude."""
        return self.__lon_degrees
    
    @lon_degrees.setter
    def lon_degrees(self, value) -> None:
        """Sets value for the degrees component of longitude."""
        self._check_value(value, -180, 180, 'Degrees component of longitude')
        self.__lon_degrees = value

    @property
    def lon_minutes(self) -> int:
        """Returns the minutes component of longitude."""
        return self.__lon_minutes
    
    @lon_minutes.setter
    def lon_minutes(self, value) -> None:
        """Sets value for the minutes component of longitude."""
        self._check_value(value, 0, 59, 'Minutes component of longitude')
        self.__lon_minutes = value

    @property
    def lon_seconds(self) -> int:
        """Returns the seconds component of longitude."""
        return self.__lon_seconds
    
    @lon_seconds.setter
    def lon_seconds(self, value) -> None:
        """Sets value for the seconds component of longitude."""
        self._check_value(value, 0, 59, 'Seconds component of longitude')
        self.__lon_seconds = value


class Coordinate(ABC):
    """
    Interface for coordinate types providing latitude and longitude in decimal degrees.
    """
    @abstractmethod
    def get_latitude(self) -> float:
        pass

    @abstractmethod
    def get_longitude(self) ->  float:
        pass


class DmsCoordinateAdapter(Coordinate):
    """
    Adapter class that converts coordinates from DMS to decimal degrees format.
    """


    class CoordType(Enum):
        LONGITUDE = 1
        LATITUDE = 2

    def __init__(self, dms: DmsCoordinate):
        # Check type
        if not isinstance(dms, DmsCoordinate):
            raise TypeError("Parameter 'dms' must be an instance of DmsCoordinate")
        self.__dms = dms
    
    def get_latitude(self) -> float:
        return self._dms_to_degrees(
            self.__dms.lat_degrees, 
            self.__dms.lat_minutes,
            self.__dms.lat_seconds,
            self.CoordType.LATITUDE
        )

    def get_longitude(self) ->  float:
        return self._dms_to_degrees(
            self.__dms.lon_degrees, 
            self.__dms.lon_minutes,
            self.__dms.lon_seconds,
            self.CoordType.LONGITUDE
        )

    @classmethod
    def _dms_to_degrees(cls, degrees: int, minutes: int, seconds: int, coord_type: CoordType) -> float:
        """
        Converts DMS (Degrees, Minutes, Seconds) to decimal degrees format.

        :param degrees: Degree component of the coordinate
        :param minutes: Minute component of the coordinate
        :param seconds: Second component of the coordinate
        :param coord_type: Type of coordinate (LATITUDE or LONGITUDE)
        :return: Coordinate in decimal degrees
        """
        # Check parameters' types
        if not all(isinstance(item, int) for item in (degrees, minutes, seconds)):
            raise TypeError('degrees, minutes and seconds must be integer numbers')
        if not isinstance(coord_type, cls.CoordType):
            raise TypeError('coord_type must be an instance of CoordType')
            
        # Set max value for degrees
        if coord_type == cls.CoordType.LONGITUDE:
            max_value = 180
        elif coord_type == cls.CoordType.LATITUDE:
            max_value = 90
        else:
            raise ValueError('Unknown type of coordinate')
        # Check values
        if abs(degrees) > max_value:
            raise ValueError(f'degrees must be in range [{-max_value};{max_value}]')
        if not (0 <= minutes < 60 and 0 <= seconds < 60):
            raise ValueError('minutes and seconds must be in range [0;60)')
        if abs(degrees) == max_value and (minutes or seconds):
            raise ValueError(f'Wrong coordinate value. It must be in range [{-max_value};{max_value}]')
        
        return round(degrees + minutes / 60 + seconds / 3600, 4)
    

def display_coordinates(coord: Coordinate):
    """
    Prints the latitude and longitude in decimal degrees format.

    :param coord: An object that implements the Coordinate interface.
    """
    print("Decimal Coordinates:")
    print(f"  Latitude:  {coord.get_latitude()}°")
    print(f"  Longitude: {coord.get_longitude()}°")
    
def main():
    # Create a legacy DMS coordinate instance
    legacy_dms = DmsCoordinate(50, 26, 23, 30, 31, 53)

    # Wrap the legacy coordinate with the adapter
    adapted_coord = DmsCoordinateAdapter(legacy_dms)

    # Display the converted coordinate in decimal format
    display_coordinates(adapted_coord)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()