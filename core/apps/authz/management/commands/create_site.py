from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a Site record for app.mucho.com.br'

    def handle(self, *args, **kwargs):
        # Define the domain and name for the site
        domain = 'app.mucho.com.br'
        name = 'Mucho AI'

        # Check if the site already exists
        site, created = Site.objects.get_or_create(domain=domain, defaults={'name': name})

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created site: {domain}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Site {domain} already exists'))

        # Optionally, set the SITE_ID if needed
        settings.SITE_ID = site.id
