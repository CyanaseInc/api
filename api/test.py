from django.db.models import Sum, Max
from datetime import date

def get_investment_summary(request):
    try:
        user_id = request.user.id
        
        # 1. Calculate total deposits
        total_deposits = Deposit.objects.filter(user_id=user_id).aggregate(total=Sum('deposit_amount'))['total'] or 0.0

        # 2. Get distinct investment options and their latest (highest id) record
        latest_ids = InvestmentTrack.objects.filter(user_id=user_id) \
            .values('investment_option_id') \
            .annotate(latest_id=Max('id')) \
            .values_list('latest_id', flat=True)

        latest_tracks = InvestmentTrack.objects.filter(id__in=latest_ids)

        net_worth = sum(track.closing_balance for track in latest_tracks)
        investment_performance = []

        for track in latest_tracks:
            today_deposits = Deposit.objects.filter(
                user_id=user_id,
                investment_option_id=track.investment_option_id,
                created__date=date.today()
            ).aggregate(total=Sum('deposit_amount'))['total'] or 0.0

            investment_performance.append({
                'investment_option_id': track.investment_option_id,
                'name': track.investment_option.name if track.investment_option else "Unknown",
                'closing_balance': float(track.closing_balance),
                'today_deposits': float(today_deposits),
                'date': track.created.strftime('%Y-%m-%d'),
            })

        return {
            'total_deposits': float(total_deposits),
            'net_worth': float(net_worth),
            'investment_performance': investment_performance
        }

    except Exception as e:
        raise Exception(f"Error retrieving investment data: {str(e)}")
