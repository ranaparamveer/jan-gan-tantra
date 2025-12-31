from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from wiki.models import Category, Solution, SuccessPath
from issues.models import Issue, IssueCluster
from govgraph.models import Department, Designation, Officer
import random
from datetime import timedelta
from django.utils import timezone
import meilisearch
from django.conf import settings
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Superuser if not exists (already done in start.sh, but safe to fetch)
        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        # 1. Create Categories
        categories = ['Water', 'Electricity', 'Roads', 'Sanitation', 'Police', 'Health']
        cat_objs = {}
        for cat_name in categories:
            cat, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': f'Issues related to {cat_name}',
                    'slug': slugify(cat_name)
                }
            )
            cat_objs[cat_name] = cat
        self.stdout.write(f'Created {len(categories)} categories')

        # 2. Create Solutions (How-To Guides)
        solutions_data = [
            {
                'title': 'File complaint for Dirty Water Supply',
                'cat': 'Water',
                'steps': ['Take photo of dirty water', 'Locate nearest Jal Board office', 'Submit form A-12', 'Get receipt'],
                'keywords': ['water', 'dirty', 'pollution', 'tanker']
            },
            {
                'title': 'Report Pothole on Main Road',
                'cat': 'Roads',
                'steps': ['Click photo with geotag', 'Upload to PWD app', 'Note complaint ID'],
                'keywords': ['road', 'pothole', 'broken', 'accident']
            },
            {
                'title': 'Street Light Not Working',
                'cat': 'Electricity',
                'steps': ['Find pole number', 'Call electricity helpline 1912', 'Register complaint'],
                'keywords': ['light', 'dark', 'street', 'unsafe']
            }
        ]
        
        for sol in solutions_data:
            Solution.objects.get_or_create(
                title=sol['title'],
                defaults={
                    'category': cat_objs[sol['cat']],
                    'steps': sol['steps'],
                    'problem_keywords': sol['keywords'],
                    'language': 'en',
                    'created_by': admin,
                    'success_rate': 0.85
                }
            )
        self.stdout.write(f'Created {len(solutions_data)} solutions')

        # 3. Create Gov Graph
        dept, _ = Department.objects.get_or_create(name='Municipal Corporation', state='Delhi', district='New Delhi', city='New Delhi')
        desig, _ = Designation.objects.get_or_create(title='Junior Engineer', department=dept, level=1, responsibilities=['Road maintenance', 'Basic civic amenities'])
        Officer.objects.get_or_create(
            name='Rajesh Kumar',
            defaults={
                'designation': desig,
                'contact_email': 'rajesh.je@mcd.gov.in',
                'contact_phone': '9876543210'
            }
        )
        self.stdout.write('Created Government Directory')

        # 4. Create Issues (Clustered around Delhi CP)
        # Center: 28.627684, 77.215571 (Connaught Place)
        base_lat, base_lon = 28.627684, 77.215571
        
        
        for i in range(200):
            # Random offset (approx 5km spread)
            lat = base_lat + (random.random() - 0.5) * 0.05
            lon = base_lon + (random.random() - 0.5) * 0.05
            
            cat_name = random.choice(categories)
            Issue.objects.create(
                title=f'Broken {cat_name} infrastructure',
                description=f'Severe issue with {cat_name} at this location. Needs urgent fix.',
                location=Point(lon, lat),
                category=cat_objs[cat_name],
                status=random.choice(['reported', 'in_progress', 'resolved']),
                reported_by=admin,
                upvotes=random.randint(0, 50)
            )
        self.stdout.write('Created 20 sample issues around Delhi')

        # 5. Index to MeiliSearch
        try:
            client = meilisearch.Client(settings.MEILI_URL, settings.MEILI_MASTER_KEY)
            index = client.index('solutions')
            
            # Prepare docs
            docs = []
            for s in Solution.objects.all():
                docs.append({
                    'id': s.id,
                    'title': s.title,
                    'steps': s.steps,
                    'keywords': s.problem_keywords,
                    'category': s.category.name
                })
            
            index.add_documents(docs)
            self.stdout.write('Indexed solutions to MeiliSearch')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'MeiliSearch indexing failed: {e}'))

        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))
