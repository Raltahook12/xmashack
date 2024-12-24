import os
from urllib.parse import quote_plus

import pandas as pd
import uvicorn
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from const import PREDICTION_DIR, STATIC_DIR, TEMPLATES_DIR, TRAIN_DIR
from model.predict_script import predict

from model.prepare_predict import prepare_predict
from model.prepare_train import prepare_train
from model.train_script import train_model

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get(
    path="/",
    response_class=HTMLResponse,
)
async def read_root(request: Request):
    """
    Рендеринг главной страницы.

    :param request: параметры запроса
    :return: html-страницу
    """
    return templates.TemplateResponse(
        "index.html", {"request": request},
    )


@app.get(
    path="/train",
    response_class=HTMLResponse,
)
async def train_page(request: Request):
    """
    Страница обучения.

    :param request: параметры запроса
    :return: html-страницу
    """
    return templates.TemplateResponse(
        "train.html", {"request": request},
    )


@app.get(
    path="/predict",
    response_class=HTMLResponse,
)
async def predict_page(request: Request):
    """
    Страница предсказания

    :param request: параметры запроса
    :return: html-страницу
    """
    return templates.TemplateResponse("predict.html", {"request": request})


@app.post(path="/upload-train")
async def upload_train_file(
        file: UploadFile = File(...),
):
    """
    Загрузка файла для обучения.

    :param file: загружаемый файл
    :return: сообщение об успешной загрузке файла
    """
    file_path = os.path.join(TRAIN_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return JSONResponse(
                content={"error": "Неподдерживаемый формат файла."},
                status_code=400,
            )
        df = prepare_train(df)
        train_model(df)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    return JSONResponse(content={"message": "Файл успешно загружен."})


@app.post(path="/upload-predict")
async def upload_predict_file(
        file: UploadFile = File(...),
        download: bool = Form(False),
):
    """
    Загрузка файла для предсказания.

    :param file: загружаемый файл
    """
    original_filename = file.filename
    file_path = os.path.join(PREDICTION_DIR, original_filename)
    processed_file_path = os.path.join(
        PREDICTION_DIR,
        original_filename,
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        if original_filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif original_filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return JSONResponse(
                content={"error": "Неподдерживаемый формат файла."},
                status_code=400,
            )
        df = prepare_predict(df)
        target = predict(df)
        print(target)
        df['Прогноз модели'] = target
        df.to_excel(
            processed_file_path.replace('csv', 'xlsx'),
            index=False,
        )
        print(processed_file_path)

        if download:
            return FileResponse(
                processed_file_path,
                media_type='application/octet-stream',
                filename=quote_plus(original_filename + '.xlsx'),
                headers={
                    "Content-Disposition": f"attachment; filename={original_filename}",
                }
            )
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"message": "Файл успешно загружен."})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
