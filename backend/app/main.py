from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from .database import Base, engine
from .routers import (
    about,
    contact,
    education,
    projects,
    blogs,
    admin_blogs,
    admin_projects
)
from .auth import login

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # now alembic will handle schema creation and other changes in the columns, attributes and the constraints
    # startup
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    await engine.dispose()
    
    
app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="../backend/app/templates")

app.include_router(about.router, prefix="/api/about", tags=["About"])
app.include_router(education.router, prefix="/api/education", tags=["Education"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(admin_projects.router, prefix="/api/admin/projects", tags=["Admin Projects"])
app.include_router(blogs.router, prefix="/api/blogs", tags=["Blogs"])
app.include_router(admin_blogs.router, prefix="/api/admin/blogs", tags=["Admin Blogs"])
app.include_router(login.router, prefix="/api/auth/login", tags=["Login"])

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
