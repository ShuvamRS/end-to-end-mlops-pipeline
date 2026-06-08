from __future__ import annotations

import uuid
from pathlib import Path
from typing import Dict, Any

import bentoml
from fastapi import FastAPI
from PIL import Image

MODEL_VERSION = "v0.0.1"
DATA_FOLDER_PATH = Path("extra-data/extra_data")

app = FastAPI()

bento_model = bentoml.keras.get("celestial_bodies_classifier_model")
preprocess = bento_model.custom_objects["preprocess"]
postprocess = bento_model.custom_objects["postprocess"]
model = bento_model.load_model()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/setup")
async def setup(_: Dict[str, Any]) -> Dict[str, str]:
    return {"model_version": MODEL_VERSION}


@app.post("/webhook")
async def webhook() -> Dict[str, str]:
    return {"status": "Unknown event"}


@app.post("/predict")
async def predict(data: Dict[str, Any]) -> Dict[str, Any]:
    task = data["tasks"][0]

    # Label Studio stores imported image URLs with a prefix before the original filename.
    filename = "".join(task["data"]["image"].split("-")[1:])
    image_path = DATA_FOLDER_PATH / filename

    image = Image.open(image_path)
    preprocessed_image = preprocess(image)
    model_prediction = model.predict(preprocessed_image)

    result = postprocess(model_prediction)
    prediction = result["prediction"]
    score = float(result["probabilities"][prediction])

    return {
        "results": [
            {
                "model_version": MODEL_VERSION,
                "score": score,
                "result": [
                    {
                        "value": {"choices": [prediction]},
                        "id": str(uuid.uuid4()),
                        "from_name": "choice",
                        "to_name": "image",
                        "type": "choices",
                    }
                ],
            }
        ]
    }
