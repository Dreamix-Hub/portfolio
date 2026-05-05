from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .database import Base, engine
from .routers import about, contact, education, projects, blogs

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    await engine.dispose()
    
    
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="../backend/app/templates")

app.include_router(about.router, prefix="/api/about", tags=["About"])
app.include_router(education.router, prefix="/api/education", tags=["Education"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(blogs.router, prefix="/api/blogs", tags=["Blogs"])

# exception handlers
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)

    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
