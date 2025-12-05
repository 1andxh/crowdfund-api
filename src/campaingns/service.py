from src.campaingns.models import Campaign
from src.campaingns.schemas import CampaignCreateModel, CampaignUpdateModel
from sqlmodel import select, desc
from datetime import datetime as dt
from sqlmodel.ext.asyncio.session import AsyncSession

# from .models import Campaign


# Session = AsyncSession()
class CampaignService:
    async def get_all_campaigns(self, session: AsyncSession):
        statement = select(Campaign).order_by(desc(Campaign.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_campaign(self, id: str, session: AsyncSession):
        statement = select(Campaign).where(Campaign.id == id)
        result = await session.exec(statement)
        return result.first()

    async def create_campaign(
        self, campaign: CampaignCreateModel, session: AsyncSession
    ):
        campaign_detail = campaign.model_dump()
        new_campaign = Campaign(**campaign_detail)
        session.add(new_campaign)
        await session.commit()
        return new_campaign

    async def update_campaign(
        self, id: str, campaign: CampaignUpdateModel, session: AsyncSession
    ):
        campaign_to_update = await self.get_campaign(id, session)
        if campaign_to_update is not None:
            update = campaign.model_dump()
            for k, v in update.items():
                setattr(campaign_to_update, k, v)

    async def delete_campaign(self, id: str, session: AsyncSession):
        campaign_to_delete = await self.get_campaign(id, session)
        if campaign_to_delete is not None:
            await session.delete(campaign_to_delete)
            await session.commit()
            return True
        return
