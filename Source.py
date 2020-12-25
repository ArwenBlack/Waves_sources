import csv
from dataclasses import dataclass
from typing import List


@dataclass
class Source:
    # source_atribute: str
    id_s: int
    year_s: int
    validity_s: int
    focal_depth_s: float
    primary_magnitude_s: float
    country_s: str
    latitude_s: float
    longitude_s: float
    house_damaged_s: float
    house_destroyed_s: float


def parse_source(filename: str) -> List[Source]:
    source_info = list()
    data_records: List[Source] = list()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            if (i == 0):
                source_info = row[1:]
            else:
                data_records += [
                    Source(id_s=row[0], year_s=row[1], validity_s=row[7], focal_depth_s=row[8], primary_magnitude_s=row[9],
                           country_s=row[11],
                           latitude_s=row[14], longitude_s=row[15], house_damaged_s=row[29], house_destroyed_s=row[31])]

    return data_records
