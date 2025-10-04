from fastapi import APIRouter

from app.subscriptions.handlers import SubscriptionHandler

router = APIRouter()
handler = SubscriptionHandler()

router.add_api_route("/", handler.create, methods=["POST"], status_code=201)
router.add_api_route("/{subscription_id}", handler.get, methods=["GET"])
router.add_api_route("/{subscription_id}", handler.update, methods=["PUT"])
router.add_api_route("/{subscription_id}", handler.delete, methods=["DELETE"])
router.add_api_route("/list/", handler.lists, methods=["GET"])
router.add_api_route("/sum/", handler.sums, methods=["GET"])
