import os

from cot.ai.infrastructure.ziva.adapters.external.translate import AsyncZivaTranslateAdapter

from .adapters.external.langdetect_adapter import AsyncZiVALangDetectAdapter
from ...core.adapters.repositories.mongo_multilingual_repo import AsyncMongoMultilingualRepository

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
    
    datasource = providers.Singleton(
        AsyncZiVADatasource, config={"DB_URL": os.getenv("MYSQLITE_DB_NAME")}
    )
    mongo_datasource = providers.Singleton( 
        AsyncZiVAMongoDatasource,
        config={"MONGO_URI":os.getenv("MONGO_URI")}
        
    )
    multilingual_repository = providers.Singleton(
        AsyncMongoMultilingualRepository,
        mongo_datasource
    )
    
    genai_generator = providers.Singleton(
        GemmaGenAIAdapter,
        api_key=AsyncContainer.config.google_api_key,
    )
    detector = providers.Singleton(
        AsyncZiVALangDetectAdapter,
        genai_generator
    )
    # Use Cases
    detect_uc = providers.Factory(
        AsyncDetectLanguageUseCase, 
        detector=detector
    )
    translator = providers.Singleton(
        AsyncZivaTranslateAdapter,
        genai_generator
    )
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
    request_account_use_case = providers.Singleton(
        RequestNewAccountUseCase, account_repo
    )
    inquiry_requirements_use_case = providers.Singleton(
        InquiryAccountRequirementsUseCase, account_repo
    )
    eligibility_use_case = providers.Singleton(
        AccountOpeningEligibilityUseCase, customer_repo
    )

    # Initialize controller
    account_opening_controller = providers.Factory(
        AccountOpeningController, 
        request_account_use_case, 
        eligibility_use_case
    )
