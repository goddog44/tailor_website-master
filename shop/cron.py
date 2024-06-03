from django.core.management import call_command
from django_crontab.crontab import Crontab # type: ignore

def my_backup():
  try:
    call_command('dbbackup')
  except:
    pass