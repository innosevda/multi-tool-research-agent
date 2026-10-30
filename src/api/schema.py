from pydantic import BaseModel, ConfigDict

class PaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    file_path: str
    summary: str

    