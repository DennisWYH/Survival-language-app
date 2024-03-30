from django.core.management.base import BaseCommand
from django.utils import timezone
from card.models import User, UserScore, UserCardAnswer
from datetime import datetime, timedelta


def grade_to_score(grade):
    mapping = {
        "4": 400,
        "5": 500,
        "6a": 600,
        "6a+": 625,
        "6b": 650,
        "6b+": 675,
        "6c": 700,
        "6c+": 725,
        "7a": 750,
        "7a+": 775,
        "8": 800,
    }
    return mapping.get(grade, 0)

class Command(BaseCommand):
    help = 'Calculate and store user scores'

    def handle(self, *args, **options):
        for user in User.objects.all():
            two_months_ago = datetime.now() - timedelta(days=60)
            answers = UserCardAnswer.objects.filter(user=user, timestamp__gte=two_months_ago)
            scores = sorted([grade_to_score(answer.card.grade) for answer in answers], reverse=True)[:10]
            score = sum(scores)/len(scores) if scores else 0
            UserScore.objects.create(user=user, score=score, date=timezone.now().date())