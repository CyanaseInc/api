# your_app/views.py or services.py
from rest_framework import request
from django.contrib.auth.models import User
from .models import GroupGoal, Group  # Import your models
import datetime
from dateutil.relativedelta import relativedelta  # For calculating end_date

class GoalService:
    def getGroupGoalById(self, request, lang, goalid):
        # Retrieve a group goal by ID
        try:
            goal = GroupGoal.objects.get(id=goalid)
            return {
                "id": goal.id,
                "group_id": goal.group.id,
                "group_name": goal.group.name,
                "goal_name": goal.goal_name,
                "target_amount": str(goal.target_amount),
                "current_amount": str(goal.current_amount),
                "currency": goal.currency.currency_code,
                "start_date": goal.start_date.isoformat(),
                "end_date": goal.end_date.isoformat() if goal.end_date else None,
                "status": goal.status,
                "created_at": goal.created_at.isoformat(),
                "updated_at": goal.updated_at.isoformat(),
            }
        except GroupGoal.DoesNotExist:
            return {"error": "Group goal not found"}

    def createGroupGoal(self, request, lang, user):
        current_datetime = datetime.datetime.now()
        goal_name = request.data.get("goal_name")
        goal_period = request.data.get("goal_period")  # e.g., "12" (months)
        goal_amount = request.data.get("goal_amount")  # e.g., "10000"
        deposit_type = request.data.get("deposit_type")  # e.g., "manual" or "auto"
        reminder_day = request.data.get("reminder_day")  # e.g., "Monday"
        reminder_time = request.data.get("reminder_time")  # e.g., "14:30"
        goal_type = request.data.get("goal_type")  # e.g., "Community Project"
        group_id = request.data.get("group_id")  # Assuming group_id is sent from frontend
        userid = request.user.id
        is_verified = request.user.userprofile.is_verified

        # Validation
        required_fields = {
            "goal_name": goal_name,
            "goal_period": goal_period,
            "goal_amount": goal_amount,
            "group_id": group_id,
        }
        missing_fields = [key for key, value in required_fields.items() if not value]
        if missing_fields:
            return {
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "success": False
            }

        if not is_verified:
            return {
                "message": "Your account is not verified. Please check your email and verify.",
                "success": False
            }

        try:
            # Convert goal_period to integer for date calculation
            goal_period_months = int(goal_period)
            start_date = current_datetime
            end_date = start_date + relativedelta(months=goal_period_months)

            # Create the group goal
            goal = GroupGoal.objects.create(
                group=Group.objects.get(id=int(group_id)),  # Fetch group by ID
                goal_name=goal_name,
                target_amount=goal_amount,
                current_amount=0.00,  # Default value
                currency_id=1,  # Default to currency ID 1 (adjust as needed)
                start_date=start_date,
                end_date=end_date,
                status='active',  # Default status
            )
            goal.save()
            goalid = goal.id
            goal_data = self.getGroupGoalById(request, lang, goalid)

            return {
                "message": f"You have successfully created a group goal '{goal_name}' of {goal_amount} within {goal_period} months",
                "success": True,
                "user_id": userid,
                "goalid": goalid,
                "goal": goal_data,
                "time_goal_was_created": current_datetime.isoformat(),
                "reminder_day": reminder_day,  # Included for frontend consistency
                "reminder_time": reminder_time,  # Included for frontend consistency
                "goal_type": goal_type,  # Included for group context
            }
        except Group.DoesNotExist:
            return {
                "message": "Group not found",
                "success": False
            }
        except ValueError as e:
            return {
                "message": f"Invalid goal period: {str(e)}",
                "success": False
            }
        except Exception as e:
            return {
                "message": f"Failed to create group goal: {str(e)}",
                "success": False
            }