from pydantic import BaseModel

class ChartAnalysisRequest(BaseModel):
    symbol: str
    exchange: str = "NAS"

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "NVDA",
                "exchange": "NAS"
            }
        } 