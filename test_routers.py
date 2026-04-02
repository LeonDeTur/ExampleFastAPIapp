from fastapi import APIRouter, Query

from test_service import test_service

test_router = APIRouter(prefix="/test_router", tags=["test_router"])


# @test_router.get("/test_getter")
# def test_get_from_router(a: int = Query(), b: int = Query()):
#     """
#     Parametres:
#     a: num a
#     b: num b

#     Returns:
#     a + b
#     """

#     return a + b


@test_router.post("/test_adder", response_model=int, status_code=200)
def test_add(elements_to_add: list[int]):

    return test_service.extract_operation("+", *elements_to_add)
