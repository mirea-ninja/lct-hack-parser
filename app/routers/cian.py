from fastapi import APIRouter, Depends
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
    status_code=status.HTTP_201_CREATED,
    description="Запустить парсинг данных и сообщить об этом пользователю",
    summary="Запуск парсинга данных",
    # responses={},
)
def parse(model: SearchBase, cian_service: CianService = Depends()):
    return cian_service.start_parse()
