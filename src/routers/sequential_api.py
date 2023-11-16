from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.models import TickerInput
from src.providers.sequential import distributor, sequential 
from src.utils import check_ticker

from multiprocessing import Queue
from threading import Thread

router = APIRouter()


@router.get("/forecast")
def get_forecast(user_input: TickerInput) -> JSONResponse:
    """

    :param user_iput: 
    :type user_input: TickerInput
    :rtype JSONResponse
    """
    check_ticker(ticker=user_input.ticker)
    forecasted_data, rate = distributor(user_input.ticker)

    return JSONResponse({
        'status': 'ok',
        'forecasted_data': f'{forecasted_data}',
        'rate': rate,
    })


@router.post("/train") 
def post_trian(user_input: TickerInput) -> JSONResponse:
    """

    :param user_iput: 
    :type user_input: TickerInput
    :rtype JSONResponse
    """
    check_ticker(ticker=user_input.ticker)

    training_thread = Thread(target=sequential, args=(user_input.ticker,))
    training_thread.start()

    return JSONResponse({
        'status': 'ok',
        'message': f'{user_input.ticker} model created'
    })
