from fastapi import FastAPI


app = FastAPI()
app_v1 = FastAPI(
title="My API v1",
description="The first version of my API",
)

app_v2 = FastAPI(
title="My API v2",
description="The second version of my API",
)


@app_v1.get("/products")
async def get_products_v1():
    return {"message": "Products API Version 1"}


@app_v2.get("/products")
async def get_products_v2():
    return {"message": "Products API Version 2"}

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)