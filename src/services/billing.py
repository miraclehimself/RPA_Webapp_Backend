from src.models.billing import db, Subscriptions


subscriptionData = {
  "FREE": {
    "name": "FREE",
    "user_limit": 2,
    "prod_robot": 2,
    "dev_robot": 2,
    "on_demand_robot": 2,
    "period": "MONTHLY",
    "amount": 0.00,
    "status": "ACTIVE"
  }
}

def subsriptionByWorkspace(workspace_id):
  return Subscriptions.query.filter_by(workspace_id=workspace_id).first()

def addSubscription(plan, workspace):
  sub = Subscriptions(workspace=workspace, **subscriptionData[plan])
  db.session.add(sub)
  db.session.commit()
  return sub
