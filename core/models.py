from __future__ import annotations

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    lat: float
    lon: float


class LocationResult(BaseModel):
    input_address: str
    normalized_address: str
    point: GeoPoint
    provider: str = "dummy"
    extra: dict[str, Any] = Field(default_factory=dict)


class BuildingCandidate(BaseModel):
    building_id: str
    name: Optional[str] = None
    address: Optional[str] = None
    distance_m: Optional[float] = None
    extra: dict[str, Any] = Field(default_factory=dict)


class RooftopAreaEstimate(BaseModel):
    roof_area_m2_suggested: Optional[float] = None
    floor_area_m2: Optional[float] = None
    availability_ratio: Optional[float] = None
    confidence: Literal["low", "medium", "high"] = "low"
    note: Optional[str] = None
    candidates: list[BuildingCandidate] = Field(default_factory=list)


class ScenarioInput(BaseModel):
    greening_type: Literal["grass", "sedum", "shrub", "tree"]
    coverage_ratio: float = Field(ge=0.0, le=1.0)


class SimulationResult(BaseModel):
    roof_area_m2: float
    greening_type: str
    coverage_ratio: float

    green_area_m2: float
    co2_absorption_kg_per_year: float
    temp_reduction_c: float
    baseline_surface_temp_c: float
    after_surface_temp_c: float

    tree_equivalent_count: int

    engine_version: str
    coefficient_set_version: str
    meta: dict[str, Any] = Field(default_factory=dict)


class ReportArtifact(BaseModel):
    kind: Literal["pdf", "excel", "image"]
    filename: str
    content_type: str
    bytes_data: bytes
