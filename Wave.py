import csv
from dataclasses import dataclass
from typing import List


@dataclass()
class Wave:
    id_s: int
    id_w: int
    year_w: int
    month_w: int
    day_w: int
    country_w: str
    state_w: str
    latitude_w: float
    longitude_w: float
    max_height_w: float
    house_damaged_w: float
    house_destroyed_w: float


def parse_wave(filename: str) -> List[Wave]:
    wave_info= list()
    data_records: List[Wave] = list()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            if (i==0):
                wave_info = row[1:]
            else:
                data_records+= [
                    Wave(id_s=row[0], id_w=row[1], year_w=row[2], month_w=row[3], day_w=row[4], country_w=row[6], state_w=row[7],
                         latitude_w=row[9], longitude_w=row[10], max_height_w=row[17], house_damaged_w=row[25], house_destroyed_w=row[27]
                         )]

    return data_records