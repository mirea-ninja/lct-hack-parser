from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.models import ApartmentBase
from app.models.search import SearchBase
from app.services.auth import verify_access_token
from app.services.cian import CianService

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    "/parse",
    response_model=list[ApartmentBase],
    response_description="Парсинг данных успешно запущен",
    status_code=status.HTTP_200_OK,
    description="Запустить парсинг данных и сообщить об этом пользователю",
    summary="Запуск парсинга данных",
    # responses={},
)
def parse(search: SearchBase, cian_service: CianService = Depends()):
    try:
        return cian_service.start_parse(search=search)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT if isinstance(e, TimeoutError) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
  