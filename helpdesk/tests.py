from django.test import TestCase

# Notification For Manager (Problems not assigned to the experts)
@background(schedule=60)
def check_unassigned_problems():
    time_threshold = timezone.now() - datetime.timedelta(hours=1) #After an hour
    unassigned_problems = Problem.objects.filter(
        expert__isnull=True, 
        submission_date__lte=time_threshold,
        admin_notified=False
    )

    for problem in unassigned_problems:
        admin_staff = Staff.objects.filter(role='admin').first()
        if admin_staff:
            message = f"Problem '{problem.title}' has not been picked by an expert for over an hour."
            send_sms_via_farazsms(admin_staff.phone_number, message)
            problem.admin_notified = True
            problem.save()
