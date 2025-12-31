"""
Government Directory Scraper
Scrapes public government directories to populate Gov-Graph
"""
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from govgraph.models import Department, Designation, Officer


class DirectoryScraper:
    """
    Base scraper for government directories
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; JGT-Bot/1.0; +https://jan-gan-tantra.org)'
        })
    
    def scrape_nic_directory(self, state_code='DL'):
        """
        Scrape National Informatics Centre (NIC) directory
        
        Args:
            state_code: State code (e.g., 'DL' for Delhi, 'MH' for Maharashtra)
        
        Returns:
            List of officer data dictionaries
        """
        # Note: This is a template - actual NIC structure varies by state
        url = f"https://directory.nic.in/{state_code.lower()}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            officers = []
            
            # Example parsing logic (adjust based on actual HTML structure)
            for row in soup.find_all('tr', class_='officer-row'):
                officer_data = {
                    'name': row.find('td', class_='name').text.strip(),
                    'designation': row.find('td', class_='designation').text.strip(),
                    'department': row.find('td', class_='department').text.strip(),
                    'email': row.find('td', class_='email').text.strip(),
                    'phone': row.find('td', class_='phone').text.strip(),
                }
                officers.append(officer_data)
            
            return officers
        
        except Exception as e:
            print(f"Error scraping NIC directory: {e}")
            return []
    
    def scrape_municipal_directory(self, city='delhi'):
        """
        Scrape municipal corporation directory
        
        Args:
            city: City name (e.g., 'delhi', 'mumbai')
        
        Returns:
            List of officer data dictionaries
        """
        # Municipal corporation websites vary significantly
        # This is a template for Delhi Municipal Corporation
        
        urls = {
            'delhi': 'https://www.mcdonline.gov.in/contact-us',
            'mumbai': 'https://portal.mcgm.gov.in/irj/portal/anonymous/contactus',
        }
        
        url = urls.get(city.lower())
        if not url:
            print(f"No URL configured for city: {city}")
            return []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            officers = []
            
            # Parse contact information
            # Note: Structure varies by city
            for contact in soup.find_all('div', class_='contact-card'):
                officer_data = {
                    'name': contact.find('h3').text.strip() if contact.find('h3') else '',
                    'designation': contact.find('p', class_='designation').text.strip() if contact.find('p', class_='designation') else '',
                    'department': 'Municipal Corporation',
                    'email': contact.find('a', href=lambda x: x and 'mailto:' in x).text.strip() if contact.find('a', href=lambda x: x and 'mailto:' in x) else '',
                    'phone': contact.find('span', class_='phone').text.strip() if contact.find('span', class_='phone') else '',
                }
                if officer_data['name']:
                    officers.append(officer_data)
            
            return officers
        
        except Exception as e:
            print(f"Error scraping municipal directory: {e}")
            return []
    
    def import_officers(self, officers_data, source='scraped'):
        """
        Import scraped officer data into database
        
        Args:
            officers_data: List of officer dictionaries
            source: Data source identifier
        
        Returns:
            Number of officers imported
        """
        imported_count = 0
        
        for data in officers_data:
            try:
                # Get or create department
                dept, _ = Department.objects.get_or_create(
                    name=data['department'],
                    defaults={'level': 'municipal'}
                )
                
                # Get or create designation
                designation, _ = Designation.objects.get_or_create(
                    title=data['designation'],
                    defaults={'department': dept}
                )
                
                # Create or update officer
                officer, created = Officer.objects.update_or_create(
                    email=data['email'],
                    defaults={
                        'name': data['name'],
                        'designation': designation,
                        'phone': data['phone'],
                        'is_verified': False,  # Requires manual verification
                    }
                )
                
                if created:
                    imported_count += 1
                    print(f"Imported: {officer.name} - {designation.title}")
            
            except Exception as e:
                print(f"Error importing officer {data.get('name')}: {e}")
        
        return imported_count


class Command(BaseCommand):
    help = 'Scrape government directories to populate Gov-Graph'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='nic',
            help='Directory source: nic, municipal'
        )
        parser.add_argument(
            '--state',
            type=str,
            default='DL',
            help='State code for NIC directory'
        )
        parser.add_argument(
            '--city',
            type=str,
            default='delhi',
            help='City name for municipal directory'
        )
    
    def handle(self, *args, **options):
        scraper = DirectoryScraper()
        
        source = options['source']
        
        self.stdout.write(f"Starting scrape from {source}...")
        
        if source == 'nic':
            state = options['state']
            officers = scraper.scrape_nic_directory(state)
            self.stdout.write(f"Found {len(officers)} officers from NIC directory")
        
        elif source == 'municipal':
            city = options['city']
            officers = scraper.scrape_municipal_directory(city)
            self.stdout.write(f"Found {len(officers)} officers from municipal directory")
        
        else:
            self.stdout.write(self.style.ERROR(f"Unknown source: {source}"))
            return
        
        # Import officers
        if officers:
            imported = scraper.import_officers(officers)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported {imported} officers")
            )
        else:
            self.stdout.write(self.style.WARNING("No officers found to import"))
