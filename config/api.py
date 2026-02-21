from accounts.api import router as accounts_router
from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited
from ninja import NinjaAPI

api = NinjaAPI(
    title="My Booking API",
    version="1.0.0",
    description="API for managing professional appointments and services.",
)

try:
    from django.http import HttpResponse
    from ninja.openapi.docs import Redoc

    @api.get("/redoc", include_in_schema=False)
    def redoc(request):
        return HttpResponse(Redoc().render_page(request, api))
except ImportError:
    pass  # Falha silenciosa se Redoc não estiver disponível internamente dessa forma


# Swagger UI customizado com dark mode
@api.get("/docs-dark", include_in_schema=False)
def swagger_dark(request):
    return render(
        request,
        "swagger_dark.html",
        {
            "openapi_url": api.openapi_url,
            "api": api,
        },
    )


api.add_router("/auth", accounts_router, tags=["Authentication"])
api.add_router("/services", "services.api.router", tags=["Services"])
api.add_router("/business", "business.api.router", tags=["Business Settings"])
api.add_router("/professionals", "professionals.api.router", tags=["Professionals"])
api.add_router("/appointments", "appointments.api.router", tags=["Appointments"])


@api.exception_handler(Ratelimited)
def ratelimited(request, exc):
    return api.create_response(
        request,
        {"message": "Muitas solicitações. Tente novamente mais tarde."},
        status=429,
    )
