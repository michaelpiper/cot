import os

from .nlp.entity_extration import EntityExtrationHandler
from .nlp.multilingual import MultilingualController

from ...domain.entities.locale import Locale, LocaleSettings
from .nlp.language_processor import LanguageProcessor

from .use_cases.target_language_doc import GenerateTargetLanguageDocUseCase

from ...domain.entities.language import Language

from .adapters.external.translate import AsyncZivaTranslateAdapter
from .rag.retriever import ZiVAVectorRetriever

from .adapters.external.langdetect_adapter import AsyncZiVALangDetectAdapter
from ...core.adapters.repositories.mongo_multilingual_repo import (
    AsyncMongoMultilingualRepository,
)

from .adapters.datasources.ziva_mongo_datasource import AsyncZiVAMongoDatasource

from .adapters.external.intent_detector import ZiVAIntentDetector

from .use_cases.account import (
    AccountOpeningEligibilityUseCase,
    InquiryAccountRequirementsUseCase,
    RequestNewAccountUseCase,
)
from ...core.controllers.account_opening_controller import AccountOpeningController
from ...infrastructure.ziva.adapters.repositories.chat_repository import (
    ZiVAChatRepository,
)
from ...infrastructure.ziva.adapters.repositories.entity_repository import (
    ZiVAEntityRepository,
)
from .adapters.datasources.ziva_db_datasource import AsyncZiVADatasource
from ...core.dependencies import AsyncContainer
from .use_cases import AsyncHandleTranslationUseCase, AsyncDetectLanguageUseCase
from dependency_injector import providers
from ...core.adapters.external.genai_adapter import GemmaGenAIAdapter
from .adapters.repositories.mock_account_repository import (
    MockAccountRepository,
    MockCustomerRepository,
)


class ZiVAContainer(AsyncContainer):
    banking_terms = {
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
    supported_languges = [
        Language("Nigeria Pidgin", "pcm", "ISO 639-3, no ISO 639-1 exists"),
        Language("Yoruba", "yo", ""),
        Language("English", "en", ""),
        Language("French", "fr", ""),
        Language("Arabic", "ar", ""),
        Language("Hindi (India)", "hi", ""),
    ]
    locales = {
        "en_US": Locale("en_US"),
        "en_NG": Locale("en_NG"),
        "fr_FR": Locale("fr_FR"),
        "ar_AE": Locale("ar_AE"),
        "yo_NG": Locale("yo_NG"),
    }
    locale_settings = {
        "en_US": LocaleSettings(
            locale=locales["en_US"],
            currency="USD",
            timezone="America/New_York",
        ),
        "en_NG": LocaleSettings(
            locale=locales["en_NG"],
            currency="NGN",
            timezone="Africa/Lagos",
        ),
        "fr_FR": LocaleSettings(
            locale=locales["fr_FR"],
            currency="EUR",
            timezone="Europe/Paris",
        ),
        "ar_AE": LocaleSettings(
            locale=locales["ar_AE"],
            currency="AED",
            timezone="Asia/Dubai",
        ),
        "yo_NG": LocaleSettings(
            locale=locales["yo_NG"],
            currency="NGN",
            timezone="Africa/Lagos",
        ),
    }
    datasource = providers.Singleton(
        AsyncZiVADatasource, config={"DB_URL": os.getenv("MYSQLITE_DB_NAME")}
    )
    mongo_datasource = providers.Singleton(
        AsyncZiVAMongoDatasource, config={"MONGO_URI": os.getenv("MONGO_URI")}
    )
    multilingual_repository = providers.Singleton(
        AsyncMongoMultilingualRepository, mongo_datasource
    )

    genai_generator = providers.Singleton(
        GemmaGenAIAdapter,
        api_key=AsyncContainer.config.google_api_key,
    )
    detector = providers.Singleton(AsyncZiVALangDetectAdapter, genai_generator)
    # Use Cases
    detect_uc = providers.Factory(AsyncDetectLanguageUseCase, detector=detector)
    translator = providers.Singleton(AsyncZivaTranslateAdapter, genai_generator)
    translate_uc = providers.Factory(
        AsyncHandleTranslationUseCase,
        translator=translator,
        repository=multilingual_repository,
    )

    entity_repo = providers.Singleton(ZiVAEntityRepository, datasource)
    chat_repo = providers.Singleton(ZiVAChatRepository, datasource)
    # Initialize mock repositories
    account_repo = providers.Singleton(
        MockAccountRepository,
    )
    customer_repo = providers.Singleton(
        MockCustomerRepository,
    )

    intent_detector = providers.Singleton(
        ZiVAIntentDetector,
    )

    # Initialize use cases
    request_account_uc = providers.Singleton(RequestNewAccountUseCase, account_repo)
    inquiry_requirements_uc = providers.Singleton(
        InquiryAccountRequirementsUseCase,
        account_repo,
    )
    eligibility_uc = providers.Singleton(
        AccountOpeningEligibilityUseCase,
        customer_repo,
    )

    generate_target_lang_doc_uc = providers.Singleton(
        GenerateTargetLanguageDocUseCase,
    )
    # Initialize controller
    account_opening_controller = providers.Factory(
        AccountOpeningController,
        request_account_uc,
        eligibility_uc,
    )
    multilingual_controller = providers.Factory(
        MultilingualController,
    )
    entity_extration_controller = providers.Factory(
        EntityExtrationHandler,
    )

    # Initialize controller
    rag = providers.Factory(
        ZiVAVectorRetriever,
        os.getenv("ZIVA_MONGO_URI"),
    )
    nlp = providers.Factory(
        LanguageProcessor,
        multilingual_controller,
        entity_extration_controller,
    )
