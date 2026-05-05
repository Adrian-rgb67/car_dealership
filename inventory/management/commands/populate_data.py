import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Manufacturer, CarModel, Vehicle


class Command(BaseCommand):
    help = 'Populates the database with sample data for the dealership'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@premierauto.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))

        # Create a regular user
        if not User.objects.filter(username='dealer').exists():
            dealer = User.objects.create_user('dealer', 'dealer@premierauto.com', 'dealer123')
            self.stdout.write(self.style.SUCCESS('Created user: dealer / dealer123'))
        else:
            dealer = User.objects.get(username='dealer')

        # Manufacturers data
        manufacturers_data = [
            {'name': 'Toyota', 'country': 'Japan', 'founded_year': 1937, 'description': 'One of the world\'s largest automobile manufacturers, known for reliability and innovation.'},
            {'name': 'BMW', 'country': 'Germany', 'founded_year': 1916, 'description': 'A premier luxury automobile manufacturer combining performance with elegance.'},
            {'name': 'Ford', 'country': 'United States', 'founded_year': 1903, 'description': 'An American automotive pioneer known for innovation and iconic vehicles.'},
            {'name': 'Mercedes-Benz', 'country': 'Germany', 'founded_year': 1926, 'description': 'The epitome of luxury, safety, and cutting-edge automotive technology.'},
            {'name': 'Honda', 'country': 'Japan', 'founded_year': 1948, 'description': 'Japanese manufacturer celebrated for fuel efficiency and reliability.'},
            {'name': 'Tesla', 'country': 'United States', 'founded_year': 2003, 'description': 'Pioneering electric vehicle manufacturer leading the sustainable transport revolution.'},
            {'name': 'Audi', 'country': 'Germany', 'founded_year': 1909, 'description': 'German luxury brand known for progressive design and advanced technology.'},
            {'name': 'Lexus', 'country': 'Japan', 'founded_year': 1989, 'description': 'Toyota\'s luxury division, renowned for exceptional quality and customer service.'},
            {'name': 'Jeep', 'country': 'United States', 'founded_year': 1941, 'description': 'Legendary American brand synonymous with off-road capability and adventure.'},
            {'name': 'Porsche', 'country': 'Germany', 'founded_year': 1931, 'description': 'Iconic sports car manufacturer blending performance with everyday usability.'},
            {'name': 'Volkswagen', 'country': 'Germany', 'founded_year': 1937, 'description': 'The people\'s car brand, offering quality German engineering at accessible prices.'},
            {'name': 'Hyundai', 'country': 'South Korea', 'founded_year': 1967, 'description': 'South Korean automaker offering exceptional value with industry-leading warranties.'},
        ]

        manufacturers = []
        for mdata in manufacturers_data:
            m, created = Manufacturer.objects.get_or_create(
                name=mdata['name'],
                defaults={
                    'country': mdata['country'],
                    'founded_year': mdata['founded_year'],
                    'description': mdata['description'],
                }
            )
            manufacturers.append(m)
            if created:
                self.stdout.write(f'  Created manufacturer: {m.name}')

        # Car Models data
        car_models_data = [
            # Toyota
            ('Toyota', 'Camry', 2024, 'SEDAN', 'GASOLINE', 'AUTOMATIC', '2.5L 4-Cylinder', 203),
            ('Toyota', 'RAV4', 2024, 'SUV', 'HYBRID', 'CVT', '2.5L Hybrid', 219),
            ('Toyota', 'Corolla', 2023, 'SEDAN', 'GASOLINE', 'CVT', '1.8L 4-Cylinder', 139),
            ('Toyota', 'Supra', 2024, 'COUPE', 'GASOLINE', 'AUTOMATIC', '3.0L Inline-6 Turbo', 382),
            # BMW
            ('BMW', '3 Series', 2024, 'SEDAN', 'GASOLINE', 'AUTOMATIC', '2.0L Turbo 4-Cyl', 255),
            ('BMW', 'X5', 2024, 'SUV', 'PLUGIN_HYBRID', 'AUTOMATIC', '3.0L Turbo 6-Cyl Hybrid', 389),
            ('BMW', 'M4', 2024, 'COUPE', 'GASOLINE', 'DUAL_CLUTCH', '3.0L Twin-Turbo 6-Cyl', 503),
            # Ford
            ('Ford', 'Mustang', 2024, 'COUPE', 'GASOLINE', 'MANUAL', '5.0L V8', 480),
            ('Ford', 'F-150', 2024, 'TRUCK', 'GASOLINE', 'AUTOMATIC', '3.5L EcoBoost V6', 400),
            ('Ford', 'Explorer', 2023, 'SUV', 'GASOLINE', 'AUTOMATIC', '2.3L EcoBoost 4-Cyl', 300),
            # Mercedes-Benz
            ('Mercedes-Benz', 'C-Class', 2024, 'SEDAN', 'GASOLINE', 'AUTOMATIC', '2.0L Turbo 4-Cyl', 255),
            ('Mercedes-Benz', 'GLE', 2024, 'SUV', 'DIESEL', 'AUTOMATIC', '3.0L Turbo Diesel 6-Cyl', 362),
            ('Mercedes-Benz', 'AMG GT', 2024, 'COUPE', 'GASOLINE', 'DUAL_CLUTCH', '4.0L V8 Biturbo', 577),
            # Honda
            ('Honda', 'Civic', 2024, 'SEDAN', 'GASOLINE', 'CVT', '1.5L Turbo 4-Cylinder', 180),
            ('Honda', 'CR-V', 2024, 'SUV', 'HYBRID', 'CVT', '2.0L Hybrid', 204),
            ('Honda', 'Accord', 2023, 'SEDAN', 'GASOLINE', 'CVT', '1.5L Turbo 4-Cylinder', 192),
            # Tesla
            ('Tesla', 'Model 3', 2024, 'SEDAN', 'ELECTRIC', 'AUTOMATIC', 'Dual Motor', 341),
            ('Tesla', 'Model Y', 2024, 'SUV', 'ELECTRIC', 'AUTOMATIC', 'Dual Motor AWD', 384),
            ('Tesla', 'Model S', 2024, 'SEDAN', 'ELECTRIC', 'AUTOMATIC', 'Tri Motor AWD', 1020),
            # Audi
            ('Audi', 'A4', 2024, 'SEDAN', 'GASOLINE', 'AUTOMATIC', '2.0L Turbo 4-Cyl', 201),
            ('Audi', 'Q7', 2024, 'SUV', 'GASOLINE', 'AUTOMATIC', '3.0L Turbo V6', 335),
            # Lexus
            ('Lexus', 'RX', 2024, 'SUV', 'HYBRID', 'CVT', '2.5L Hybrid', 246),
            ('Lexus', 'ES', 2023, 'SEDAN', 'GASOLINE', 'AUTOMATIC', '3.5L V6', 302),
            # Jeep
            ('Jeep', 'Wrangler', 2024, 'SUV', 'GASOLINE', 'AUTOMATIC', '3.6L V6', 285),
            ('Jeep', 'Grand Cherokee', 2024, 'SUV', 'GASOLINE', 'AUTOMATIC', '3.6L V6', 293),
            # Porsche
            ('Porsche', '911', 2024, 'COUPE', 'GASOLINE', 'DUAL_CLUTCH', '3.0L Twin-Turbo Flat-6', 443),
            ('Porsche', 'Cayenne', 2024, 'SUV', 'GASOLINE', 'AUTOMATIC', '3.0L Turbo V6', 348),
            # Volkswagen
            ('Volkswagen', 'Golf GTI', 2024, 'HATCHBACK', 'GASOLINE', 'DUAL_CLUTCH', '2.0L Turbo 4-Cyl', 241),
            ('Volkswagen', 'Tiguan', 2023, 'SUV', 'GASOLINE', 'AUTOMATIC', '2.0L Turbo 4-Cyl', 184),
            # Hyundai
            ('Hyundai', 'Tucson', 2024, 'SUV', 'HYBRID', 'AUTOMATIC', '1.6L Turbo Hybrid', 226),
            ('Hyundai', 'Ioniq 5', 2024, 'HATCHBACK', 'ELECTRIC', 'AUTOMATIC', 'Dual Motor AWD', 320),
        ]

        car_models = []
        for mname, model_name, year, body, fuel, trans, engine, hp in car_models_data:
            mfr = Manufacturer.objects.get(name=mname)
            cm, created = CarModel.objects.get_or_create(
                manufacturer=mfr, name=model_name, year=year,
                defaults={
                    'body_type': body,
                    'fuel_type': fuel,
                    'transmission': trans,
                    'engine_size': engine,
                    'horsepower': hp,
                }
            )
            car_models.append(cm)
            if created:
                self.stdout.write(f'  Created car model: {cm}')

        # Vehicle data
        colors = [
            ('Pearl White', '#F5F5F5'),
            ('Midnight Black', '#1A1A2E'),
            ('Racing Red', '#CC0000'),
            ('Ocean Blue', '#0066CC'),
            ('Forest Green', '#228B22'),
            ('Silver Metallic', '#C0C0C0'),
            ('Desert Sand', '#C2B280'),
            ('Graphite Gray', '#4A4A4A'),
            ('Sapphire Blue', '#0F52BA'),
            ('Crimson', '#DC143C'),
            ('Arctic White', '#FAFAFA'),
            ('Jet Black', '#0D0D0D'),
        ]

        conditions = ['NEW', 'LN', 'EX', 'GD']
        features_options = [
            'Sunroof', 'Leather Seats', 'Navigation System', 'Backup Camera', 'Heated Seats',
            'Apple CarPlay', 'Android Auto', 'Blind Spot Monitor', 'Lane Departure Warning',
            'Adaptive Cruise Control', 'Keyless Entry', 'Push Button Start', 'Bluetooth',
            'Wireless Charging', '360 Camera', 'Head-Up Display', 'Panoramic Roof',
            'Ventilated Seats', 'Bose Sound System', 'Ambient Lighting', 'Auto Parking',
        ]

        vins_used = set()
        vehicles_created = 0

        for cm in car_models:
            # Create 1-3 vehicles per model
            num_vehicles = random.randint(1, 3)
            for _ in range(num_vehicles):
                # Generate unique VIN
                while True:
                    vin = ''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ0123456789', k=17))
                    if vin not in vins_used:
                        vins_used.add(vin)
                        break

                color_name, color_hex = random.choice(colors)
                condition = random.choice(conditions)

                # Price varies by make
                base_prices = {
                    'Toyota': (25000, 45000), 'BMW': (40000, 80000), 'Ford': (30000, 70000),
                    'Mercedes-Benz': (45000, 120000), 'Honda': (24000, 40000), 'Tesla': (40000, 100000),
                    'Audi': (38000, 75000), 'Lexus': (42000, 70000), 'Jeep': (35000, 65000),
                    'Porsche': (60000, 180000), 'Volkswagen': (25000, 45000), 'Hyundai': (25000, 50000),
                }
                price_range = base_prices.get(cm.manufacturer.name, (25000, 60000))
                price = round(random.uniform(price_range[0], price_range[1]) / 500) * 500

                # Mileage varies by condition
                mileage_ranges = {'NEW': (0, 50), 'LN': (1000, 15000), 'EX': (15000, 45000), 'GD': (45000, 90000)}
                mileage = random.randint(*mileage_ranges[condition])

                # Random features
                num_features = random.randint(3, 8)
                features = ', '.join(random.sample(features_options, num_features))

                # Description
                descriptions = [
                    f"This stunning {cm.manufacturer.name} {cm.name} is in {dict(Vehicle.Condition.choices)[condition].lower()} condition and ready for its new owner. "
                    f"Featuring a powerful {cm.engine_size} engine delivering {cm.horsepower} HP, this vehicle combines performance with luxury. "
                    f"Don't miss this opportunity to own a meticulously maintained {cm.year} {cm.manufacturer.name} {cm.name}.",
                    f"Experience the perfect blend of style and performance with this {cm.year} {cm.manufacturer.name} {cm.name}. "
                    f"Finished in beautiful {color_name}, this vehicle turns heads wherever it goes. "
                    f"With only {mileage:,} miles, it's practically waiting for new adventures.",
                    f"Looking for a reliable and stylish ride? This {cm.manufacturer.name} {cm.name} checks all the boxes. "
                    f"Well-maintained with regular service history, this vehicle offers exceptional value at its price point. "
                    f"Schedule a test drive today and experience it for yourself.",
                ]

                is_featured = random.random() < 0.2  # 20% chance to be featured

                v, created = Vehicle.objects.get_or_create(
                    vin=vin,
                    defaults={
                        'car_model': cm,
                        'mileage': mileage,
                        'color': color_name,
                        'color_code': color_hex,
                        'price': price,
                        'status': 'AV',
                        'condition': condition,
                        'description': random.choice(descriptions),
                        'features': features,
                        'seller': dealer,
                        'is_featured': is_featured,
                    }
                )
                if created:
                    vehicles_created += 1

        self.stdout.write(self.style.SUCCESS(f'\nCreated {vehicles_created} vehicles'))
        self.stdout.write(self.style.SUCCESS(f'Total vehicles in database: {Vehicle.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total manufacturers: {Manufacturer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total car models: {CarModel.objects.count()}'))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Dealer: dealer / dealer123')
