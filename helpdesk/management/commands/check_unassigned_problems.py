from django.core.management.base import BaseCommand
from django.utils import timezone
from helpdesk.models import Problem, Staff
from datetime import timedelta
from helpdesk.utils import send_sms_via_farazsms

class Command(BaseCommand):
    help = 'Check for unassigned problems and notify admin'

    def handle(self, *args, **kwargs):
        one_hour_ago = timezone.now() - timedelta(hours=1)
        unassigned_problems = Problem.objects.filter(expert__isnull=True, submission_date__lte=one_hour_ago)

        for problem in unassigned_problems:
            # Assuming admin is a staff member with role 'admin'
            admin = Staff.objects.filter(role='admin').first()
            if admin:
                message = f"Problem '{problem.title}' has been unassigned for over an hour."
                send_sms_via_farazsms(admin.phone_number, message)
                self.stdout.write(self.style.SUCCESS(f'Notified admin about problem: {problem.title}'))
# Add cron job in the server : EX : 0 * * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py check_unassigned_problems