import os
from ...infrastructure.ziva.config import ZiVAContainer
from ...infrastructure.ziva.engine import ZiVAEngine

container = ZiVAContainer()
    # Initialize DI container
container.wire(modules=[__name__])
container.config.from_dict({
    "locale": 'en',
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "mongo_uri": os.getenv("MONGO_URI"),
    "sqlite_database_name": os.getenv("MYSQLITE_DB_NAME"),
    "capabilities" : [
        "1️⃣ Account Opening",
        "2️⃣ Account Reactivation",
        "3️⃣ Account Restriction",
        "4️⃣ Balance Enquiry",
        "5️⃣ Money Transfer",
        "6️⃣ Airtime Purchase",
        "7️⃣ Data Purchase",
        "8️⃣ Bills Payment",
        "9️⃣ Block Card",
        "🔟 Account Statement",
        "🔹 Log Complaints",
        "🔹 ATM/Branch Locator",
        "🔹 Agent Locator",
        "🔹 Reset PIN",
        "🔹 Loan Request",
    ],
    "banking_terms": {
        "account": {
            "en": "account",
            "fr": "compte",
            "es": "cuenta",
        },
        "transfer": {
            "en": "transfer",
            "fr": "virement",
            "es": "transferencia",
        },
    }
})
engine = ZiVAEngine(container)