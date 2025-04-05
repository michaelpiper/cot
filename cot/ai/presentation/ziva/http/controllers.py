from typing import List
from flask import jsonify

class ZiVAAPIController:
    @staticmethod
    def regulations_response(regulations: List[str]):
        return jsonify({"regulations": regulations})

    @staticmethod
    def fraud_response(is_fraud: bool, recipient: str):
        status = "fraud_detected" if is_fraud else "clean"
        return jsonify({"status": status, "recipient": recipient})