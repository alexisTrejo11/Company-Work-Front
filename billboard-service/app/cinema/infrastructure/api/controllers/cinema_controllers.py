from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ....core.entities.cinema import Cinema
from ....application.use_case.cinema_use_cases import (
    GetCinemaByIdUseCase, GetActiveCinemasUseCase, 
    CreateCinemaUseCase, DeleteCinemaUseCase
)
from ...injection.depedencies import (
    get_cinema_by_id_use_case, get_active_cinemas_use_case,
    create_cinema_use_case, delete_cinema_use_case,
)

router = APIRouter(prefix="/api/v1/cinemas")

@router.get("/{cinema_id}", response_model=Cinema)
async def get_cinema_by_id(
    cinema_id: int,
    use_case: Annotated[GetCinemaByIdUseCase, Depends(get_cinema_by_id_use_case)]
):
    try:
        cinema = await use_case.execute(cinema_id)
        return cinema
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cinema not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/active/", response_model=list[Cinema])
async def get_cinemas_in_exhibition(
    use_case: Annotated[GetActiveCinemasUseCase, Depends(get_active_cinemas_use_case)]
):
    try:
        cinemas = await use_case.execute()
        return cinemas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/", response_model=Cinema, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    cinema: Cinema,
    use_case: Annotated[CreateCinemaUseCase, Depends(create_cinema_use_case)]
):
    try:
        created_cinema = await use_case.execute(cinema)
        return created_cinema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/{cinema_id}", response_model=Cinema, status_code=status.HTTP_200_OK)
async def update_cinemas(
    cinema: Cinema,
    use_case: Annotated[CreateCinemaUseCase, Depends(create_cinema_use_case)]
):
    try:
        created_cinema = await use_case.execute(cinema)
        return created_cinema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cinema(
    cinema_id: int,
    use_case: Annotated[DeleteCinemaUseCase, Depends(delete_cinema_use_case)]
):
    try:
        await use_case.execute(cinema_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))