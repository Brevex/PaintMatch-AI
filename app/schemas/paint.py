from pydantic import BaseModel, ConfigDict


class PaintBase(BaseModel):
    name: str
    color: str
    surface_type: str | None = None
    environment: str | None = None
    finish_type: str | None = None
    features: str | None = None
    line: str | None = None


class PaintCreate(PaintBase):
    pass


class PaintUpdate(PaintBase):
    name: str | None = None
    color: str | None = None


class Paint(PaintBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
