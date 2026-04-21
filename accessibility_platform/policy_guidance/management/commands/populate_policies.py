from django.core.management.base import BaseCommand
from policy_guidance.models import PolicyFramework
from datetime import date

class Command(BaseCommand):
    help = 'Populate policy frameworks with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing policies
        PolicyFramework.objects.all().delete()
        
        policies = [
            {
                'framework_name': 'WCAG 2.2 Level A',
                'framework_type': 'wcag',
                'region': 'Global',
                'effective_date': date(2023, 10, 5),
                'description': 'Web Content Accessibility Guidelines (WCAG) 2.2 Level A requirements. These are the basic accessibility features that must be present for users with disabilities.',
                'reference_url': 'https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_overview&levels=a'
            },
            {
                'framework_name': 'WCAG 2.2 Level AA',
                'framework_type': 'wcag',
                'region': 'Global',
                'effective_date': date(2023, 10, 5),
                'description': 'Web Content Accessibility Guidelines (WCAG) 2.2 Level AA requirements. This is the internationally recognized standard for web accessibility compliance.',
                'reference_url': 'https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_overview&levels=aa'
            },
            {
                'framework_name': 'WCAG 2.2 Level AAA',
                'framework_type': 'wcag',
                'region': 'Global',
                'effective_date': date(2023, 10, 5),
                'description': 'Web Content Accessibility Guidelines (WCAG) 2.2 Level AAA requirements. The highest level of accessibility conformance.',
                'reference_url': 'https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_overview&levels=aaa'
            },
            {
                'framework_name': 'Section 508 (Revised)',
                'framework_type': 'section_508',
                'region': 'United States',
                'effective_date': date(2018, 1, 18),
                'description': 'U.S. Federal accessibility standard requiring federal agencies to make their electronic and information technology accessible to people with disabilities.',
                'reference_url': 'https://www.section508.gov/'
            },
            {
                'framework_name': 'ADA Title III',
                'framework_type': 'ada',
                'region': 'United States',
                'effective_date': date(2010, 9, 15),
                'description': 'Americans with Disabilities Act Title III requires places of public accommodation to provide accessible websites and digital services.',
                'reference_url': 'https://www.ada.gov/'
            },
            {
                'framework_name': 'EN 301 549',
                'framework_type': 'en_301_549',
                'region': 'European Union',
                'effective_date': date(2021, 3, 1),
                'description': 'European standard for digital accessibility requirements applicable to ICT products and services, including websites, mobile applications, and software.',
                'reference_url': 'https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf'
            },
            {
                'framework_name': 'Accessible Canada Act (ACA)',
                'framework_type': 'other',
                'region': 'Canada',
                'effective_date': date(2019, 7, 11),
                'description': 'Canadian federal legislation aimed at identifying, removing, and preventing barriers to accessibility in areas under federal jurisdiction.',
                'reference_url': 'https://laws-lois.justice.gc.ca/eng/acts/A-0.6/'
            },
            {
                'framework_name': 'Disability Discrimination Act',
                'framework_type': 'other',
                'region': 'Australia',
                'effective_date': date(1992, 3, 1),
                'description': 'Australian anti-discrimination law that makes it unlawful to discriminate against people with disabilities, including in access to websites and digital services.',
                'reference_url': 'https://www.humanrights.gov.au/our-work/disability-rights'
            },
            {
                'framework_name': 'UK Public Sector Accessibility Regulations',
                'framework_type': 'other',
                'region': 'United Kingdom',
                'effective_date': date(2018, 9, 23),
                'description': 'UK regulations requiring public sector websites and mobile apps to meet accessibility standards based on WCAG 2.1 Level AA.',
                'reference_url': 'https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps'
            },
            {
                'framework_name': 'WCAG 2.1 Level A',
                'framework_type': 'wcag',
                'region': 'Global',
                'effective_date': date(2018, 6, 5),
                'description': 'Web Content Accessibility Guidelines (WCAG) 2.1 Level A requirements.',
                'reference_url': 'https://www.w3.org/WAI/WCAG21/quickref/?levels=a'
            },
            {
                'framework_name': 'WCAG 2.1 Level AA',
                'framework_type': 'wcag',
                'region': 'Global',
                'effective_date': date(2018, 6, 5),
                'description': 'Web Content Accessibility Guidelines (WCAG) 2.1 Level AA requirements.',
                'reference_url': 'https://www.w3.org/WAI/WCAG21/quickref/?levels=aa'
            },
        ]
        
        created_count = 0
        for policy_data in policies:
            try:
                PolicyFramework.objects.create(**policy_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {policy_data["framework_name"]}'))
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create {policy_data["framework_name"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {created_count} out of {len(policies)} policies!'))
