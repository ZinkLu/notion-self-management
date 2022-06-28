from dataclasses import dataclass


@dataclass
class ExternalFile:
    type: str
    url: str


@dataclass
class File(ExternalFile):
    expiry_time: str
