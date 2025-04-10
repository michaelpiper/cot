from dependency_injector import containers, providers
from .adapters import AsyncLangDetectAdapter
from .adapters import AsyncGoogleTranslateAdapter

class AsyncContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Adapters
    detector = providers.Singleton(AsyncLangDetectAdapter)
    translator = providers.Singleton(
        AsyncGoogleTranslateAdapter,
        api_key=config.google_api_key
    )