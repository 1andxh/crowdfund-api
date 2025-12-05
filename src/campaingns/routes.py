from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .service import CampaignService
from .schemas import Campaign, CampaignCreateModel, CampaignUpdateModel
from src.db.main import get_session
from typing import Annotated

campaign_router = APIRouter()
campaign_service = CampaignService()
Session = Annotated[AsyncSession, Depends(get_session)]


@campaign_router.get("/", response_model=list[Campaign])
async def get_all_campaign(session: Session):
    campaigns = await campaign_service.get_all_campaigns(session)
    return campaigns


@campaign_router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    session: Session,
):
    campaign = await campaign_service.get_campaign(
        campaign_id,
        session,
    )
    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No campaign record found"
        )
    return campaign


@campaign_router.post("/")
async def create_campaign(campaign: CampaignCreateModel, session: Session) -> dict:
    new_campaign = await campaign_service.create_campaign(campaign, session)
    # campaign = campaign_data.model_dump()
    # campaigns.append(campaign)
    # return campaign
    return {"new_campaign": new_campaign}


@campaign_router.patch("/{campaign_id}")
async def update_campaign(ca):
    pass


@campaign_router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(campaign_id: str, session: Session):
    campaign = await campaign_service.delete_campaign(campaign_id, session)
    if campaign:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Campaign not found or may have been already deleted",
    )
