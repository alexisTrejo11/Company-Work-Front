from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....core.entities.theater import Theater
from ....application.use_cases.theather_use_cases import (
    GetTheaterByIdUseCase, ListTheatersUseCase,
    CreateTheaterUseCase, UpdateTheaterUseCase,
    DeleteTheaterUseCase,GetTheatersByCinemaUseCase
)
from ...injection.depdencies import (
    get_theater_by_id_use_case, list_theaters_use_case,
    create_theater_use_case, update_theater_use_case,
    delete_theater_use_case, get_theaters_by_cinema_use_case
)

router = APIRouter(prefix="/api/v1/theaters", tags=["theaters"])

@router.get("/{theater_id}", response_model=Theater)
async def get_theater(
    theater_id: int,
    use_case: GetTheaterByIdUseCase = Depends(get_theater_by_id_use_case)
):
    theater = await use_case.execute(theater_id)
    if not theater:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found")
    return theater

@router.get("/", response_model=List[Theater])
async def list_theaters(
    page: int = 1,
    limit: int = 10,
    use_case: ListTheatersUseCase = Depends(list_theaters_use_case)
):
    page_params = {
        "offset": (page - 1) * limit,
        "limit": limit
    }
    return await use_case.execute(page_params=page_params)

@router.get("/cinema/{cinema_id}", response_model=List[Theater])
async def get_theaters_by_cinema(
    cinema_id: int,
    use_case: GetTheatersByCinemaUseCase = Depends(get_theaters_by_cinema_use_case)
):
    theaters = await use_case.execute(cinema_id)
    if not theaters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No theaters found for this cinema"
        )
    return theaters

@router.post("/", response_model=Theater, status_code=status.HTTP_201_CREATED)
async def create_theater(
    new_theater: Theater,
    use_case: CreateTheaterUseCase = Depends(create_theater_use_case)
):
    try:
        return await use_case.execute(new_theater)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{theater_id}", response_model=Theater)
async def update_theater(
    theater_id: int,
    update_theater: Theater,
    use_case: UpdateTheaterUseCase = Depends(update_theater_use_case)
):
    try:
        return await use_case.execute(theater_id, update_theater)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_theater(
    theater_id: int,
    use_case: DeleteTheaterUseCase = Depends(delete_theater_use_case)
):
    try:
        await use_case.execute(theater_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

