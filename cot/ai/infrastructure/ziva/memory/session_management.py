from ....domain.interfaces.session_repository import ISessionRepository, ISessionManager
from ....domain.models.session import BankingSession
      
class BankingSessionManager(ISessionManager):
    def __init__(self, repo: ISessionRepository):
        self.repo = repo
    async def get(self, session_id: str) -> BankingSession:
        # Check memory cache first
        if session := await self.repo.get(session_id):
            return BankingSession.from_session (session)
        return None
        
    async def save(self, session: BankingSession):
        await self.repo.save(
            session,
        )