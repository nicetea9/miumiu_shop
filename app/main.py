from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.api.exception_handlers import register_exception_handlers
from app.api.routers import categories, orders, products
from app.infrastructure.db.models import Base
from app.infrastructure.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Miu Miu Shop API",
    description="API для управления товарами, категориями и заказами в магазине Miu Miu.",
    version="2.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Miu Miu Shop API"}


# # Serve custom Swagger UI with prefill script
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    swagger_html = get_swagger_ui_html(openapi_url=app.openapi_url, title=f"{app.title} - Docs")
    # insert our small script before </body> so it executes correctly
    content = swagger_html.body.decode() if isinstance(swagger_html.body, (bytes, bytearray)) else str(swagger_html.body)
    if "</body>" in content:
        content = content.replace("</body>", '\n<script src="/static/swagger_prefill.js"></script>\n</body>')
    else:
        content += '\n<script src="/static/swagger_prefill.js"></script>'
    return HTMLResponse(content=content, status_code=swagger_html.status_code, headers=swagger_html.headers)
