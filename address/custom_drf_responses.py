from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


register_response = {
    "201": openapi.Response(
        description="test",
        examples={
            "application/json": {"username": "string"}
        }
    )
}
