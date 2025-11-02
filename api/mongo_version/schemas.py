"""Pydantic schemas for MongoDB earthquake data validation."""
from pydantic import BaseModel, Field
from typing import Optional


class EarthquakeMongoBase(BaseModel):
    """Base schema for earthquake data in MongoDB."""
    magnitude: float = Field(..., ge=0, le=10, description="Earthquake magnitude (0-10)")
    depth: float = Field(..., gt=0, description="Depth in kilometers (must be positive)")
    sig: int = Field(..., gt=0, description="Significance value (must be positive)")
    Year: int = Field(..., ge=1900, le=2100, description="Year of earthquake")
    Month: int = Field(..., ge=1, le=12, description="Month of earthquake (1-12)")

    # Optional fields from the dataset
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude (-180 to 180)")
    cdi: Optional[int] = Field(None, ge=0, le=9, description="Community Decimal Intensity (0-9)")
    mmi: Optional[int] = Field(None, ge=1, le=9, description="Modified Mercalli Intensity (1-9)")
    nst: Optional[int] = Field(None, ge=0, description="Number of seismic stations")
    dmin: Optional[float] = Field(None, ge=0, description="Minimum distance to station")
    gap: Optional[float] = Field(None, ge=0, le=360, description="Azimuthal gap (0-360)")
    tsunami: Optional[int] = Field(None, ge=0, le=1, description="Tsunami occurrence (0 or 1)")

    # Additional fields
    region: Optional[str] = Field(None, max_length=100, description="Geographic region")
    Date: Optional[str] = Field(None, description="Date of earthquake")
    Time: Optional[str] = Field(None, description="Time of earthquake")
    Updated: Optional[str] = Field(None, description="Last update timestamp")
    Timezone: Optional[str] = Field(None, description="Timezone information")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "magnitude": 6.5,
                "depth": 10.0,
                "sig": 500,
                "Year": 2024,
                "Month": 3,
                "latitude": 35.5,
                "longitude": -120.5,
                "cdi": 5,
                "mmi": 6,
                "nst": 20,
                "dmin": 0.5,
                "gap": 45.0,
                "tsunami": 0,
                "region": "California"
            }
        }


class EarthquakeMongoCreate(EarthquakeMongoBase):
    """Schema for creating a new earthquake document in MongoDB."""
    pass


class EarthquakeMongoUpdate(BaseModel):
    """Schema for updating an earthquake document in MongoDB (all fields optional)."""
    magnitude: Optional[float] = Field(None, ge=0, le=10)
    depth: Optional[float] = Field(None, gt=0)
    sig: Optional[int] = Field(None, gt=0)
    Year: Optional[int] = Field(None, ge=1900, le=2100)
    Month: Optional[int] = Field(None, ge=1, le=12)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    cdi: Optional[int] = Field(None, ge=0, le=9)
    mmi: Optional[int] = Field(None, ge=1, le=9)
    nst: Optional[int] = Field(None, ge=0)
    dmin: Optional[float] = Field(None, ge=0)
    gap: Optional[float] = Field(None, ge=0, le=360)
    tsunami: Optional[int] = Field(None, ge=0, le=1)
    region: Optional[str] = Field(None, max_length=100)
    Date: Optional[str] = None
    Time: Optional[str] = None
    Updated: Optional[str] = None
    Timezone: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "magnitude": 7.0,
                "depth": 15.0
            }
        }


class EarthquakeMongoResponse(EarthquakeMongoBase):
    """Schema for earthquake response from MongoDB (includes _id)."""
    id: str = Field(..., alias="_id", description="MongoDB document ID")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "magnitude": 6.5,
                "depth": 10.0,
                "sig": 500,
                "Year": 2024,
                "Month": 3,
                "latitude": 35.5,
                "longitude": -120.5,
                "tsunami": 0
            }
        }


class DeleteResponse(BaseModel):
    """Response schema for delete operations."""
    message: str
    deleted_id: Optional[str] = None
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "message": "Earthquake deleted successfully",
                "deleted_id": "507f1f77bcf86cd799439011"
            }
        }
