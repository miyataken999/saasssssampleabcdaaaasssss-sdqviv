import os
import subprocess
import logging
from fastapi import FastAPI, Request, HTTPException
import requests
import json
from datetime import datetime
import importlib
import os
import pkgutil
from mysite.libs.utilities import validate_signature, no_process_file
#from mysite.database.database import ride,create_ride
from controllers.gra_04_database.rides import test_set_lide


logger = logging.getLogger(__name__)

"""
router 
"""
def include_routers(app):
    package_dir = "/home/user/app/routers"
    if not os.path.exists(package_dir):
        logger.error(f"Package directory {package_dir} does not exist.")
        return

    for module_info in pkgutil.iter_modules([package_dir]):
        try:
            if module_info.ispkg:
                sub_package_dir = os.path.join(package_dir, module_info.name)
                for sub_module_info in pkgutil.iter_modules([sub_package_dir]):
                    module_name = (
                        f"routers.{module_info.name}.{sub_module_info.name}"
                        if sub_module_info.ispkg
                        else f"routers.{module_info.name}.{sub_module_info.name}"
                    )
                    module = importlib.import_module(module_name)
                    if hasattr(module, "router"):
                        app.include_router(module.router)
            else:
                module_name = f"routers.{module_info.name}"
                module = importlib.import_module(module_name)
                if hasattr(module, "router"):
                    app.include_router(module.router)
        except ModuleNotFoundError as e:
            logger.error(f"Module not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


def setup_webhook_routes(app: FastAPI):
    from polls.routers import register_routers

    register_routers(app)    
    @app.post("/webhook")
    async def webhook(request: Request):
        logger.info("[Start] ====== LINE webhook ======")
        try:
            body = await request.body()
            received_headers = dict(request.headers)
            body_str = body.decode("utf-8")
            logger.info("Received Body: %s", body_str)
            body_json = json.loads(body_str)
            events = body_json.get("events", [])

            for event in events:
                if event["type"] == "message" and event["message"]["type"] == "text":
                    user_id = event["source"]["userId"]
                    text = event["message"]["text"]
                    logger.info("------------------------------------------")
                    logger.info(f"User ID: {user_id}, Text: {text}")
                    test_set_lide(text,"a1")
                    no_process_file(text, "ai")
                    

            for event in events:
                if event["type"] == "message" and event["message"]["type"] == "text":
                    user_id = event["source"]["userId"]
                    text = event["message"]["text"]
                    logger.info(event)
                    logger.info(f"User ID: {user_id}, Text: {text}")
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    title = text[:10]
                    user_id_with_timestamp = f"{now}_{title}_{user_id}"
                    no_process_file(text, user_id_with_timestamp)
                    test_set_lide(text, user_id_with_timestamp)

            logger.info("Received Headers: %s", received_headers)
            logger.info("Received Body: %s", body.decode("utf-8"))

            line_signature = received_headers.get("x-line-signature")
            if not line_signature:
                raise HTTPException(status_code=400, detail="X-Line-Signature header is missing.")

            if not validate_signature(body.decode("utf-8"), line_signature, os.getenv("ChannelSecret")):
                raise HTTPException(status_code=400, detail="Invalid signature.")

            if not os.getenv("WEBHOOK_URL") or not os.getenv("WEBHOOK_URL").startswith("https://"):
                raise HTTPException(status_code=400, detail="Invalid webhook URL")

            headers = {
                "Content-Type": "application/json",
                "X-Line-Signature": line_signature,
                "Authorization": f"Bearer {os.getenv('ChannelAccessToken')}",
            }

            logger.info("Forwarding to URL: %s", os.getenv("WEBHOOK_URL"))
            logger.info("Forwarding Headers: %s", headers)
            logger.info("Forwarding Body: %s", body.decode("utf-8"))

            response = requests.post(os.getenv("WEBHOOK_URL"), headers=headers, data=body)
            responses = requests.post(os.getenv("WEBHOOKGAS"), headers=headers, data=body)
            logger.info("Response Code: %s", response.status_code)
            logger.info("Response Content: %s", response.text)
            logger.info("Response Headers: %s", response.headers)

            return {"status": "success", "response_content": response.text}, response.status_code

        except Exception as e:
            logger.error("Error: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))
