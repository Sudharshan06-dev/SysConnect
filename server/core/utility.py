#HELPERS FUNCTION
from fastapi.responses import JSONResponse
from core.schemas import DefaultResponse


##Common Utility Function for Responses ##
def create_response(status_code: int, message: str, status: str):
    return JSONResponse(status_code=status_code, content=DefaultResponse(title=status, message=status[message]).dict())