**all access endpoint**
GET /campaigns (Browse campaigns)
GET /campaigns/{id} (View campaign)
GET /campaigns/{id}/contributions (See donations)
POST /campaigns/{id}/contributions (Donate)

**protected endpoints:**
POST /campaigns (Create campaign)
PUT /campaigns/{id} (Update campaign)
DELETE /campaigns/{id} (Delete campaign)
POST /campaigns/{id}/updates (Post update)
GET /users/me/campaigns (My campaigns)
POST /withdrawals (Withdraw funds)
