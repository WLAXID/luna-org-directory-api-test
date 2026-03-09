import random
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Building, Activity, Organization, PhoneNumber

fake = Faker('ru_RU')

# Moscow coordinates range
MOSCOW_LAT_MIN, MOSCOW_LAT_MAX = 55.5, 56.0
MOSCOW_LON_MIN, MOSCOW_LON_MAX = 37.3, 37.8

# Sample activities tree
ACTIVITIES_TREE = {
    "Еда": {
        "Мясная продукция": ["Говядина", "Свинина", "Курица"],
        "Молочная продукция": ["Молоко", "Сыр", "Йогурт"],
        "Хлебобулочные изделия": ["Хлеб", "Булочки", "Пироги"]
    },
    "Автомобили": {
        "Грузовые": ["Фуры", "Пикапы", "Микроавтобусы"],
        "Легковые": ["Седаны", "Хэтчбеки", "Кроссоверы"],
        "Запчасти": ["Двигатели", "Колеса", "Аксессуары"]
    },
    "Электроника": {
        "Компьютеры": ["Ноутбуки", "Десктопы", "Планшеты"],
        "Телефоны": ["Смартфоны", "Проводные", "Радиотелефоны"],
        "Аудио": ["Наушники", "Колонки", "Микрофоны"]
    }
}


def create_buildings(db: Session, count: int = 20):
    """Create sample buildings"""
    buildings = []
    for i in range(count):
        building = Building(
            address=fake.address(),
            latitude=random.uniform(MOSCOW_LAT_MIN, MOSCOW_LAT_MAX),
            longitude=random.uniform(MOSCOW_LON_MIN, MOSCOW_LON_MAX)
        )
        db.add(building)
        buildings.append(building)
    db.commit()
    return buildings


def create_activities(db: Session):
    """Create activities tree"""
    activities = []
    
    def create_activity_tree(tree_dict, parent_id=None, level=1):
        for name, children in tree_dict.items():
            activity = Activity(name=name, parent_id=parent_id, level=level)
            db.add(activity)
            db.flush()
            activities.append(activity)
            
            if isinstance(children, dict):
                create_activity_tree(children, activity.id, level + 1)
            elif isinstance(children, list):
                for child_name in children:
                    child_activity = Activity(name=child_name, parent_id=activity.id, level=level + 1)
                    db.add(child_activity)
                    activities.append(child_activity)
    
    create_activity_tree(ACTIVITIES_TREE)
    db.commit()
    return activities


def create_organizations(db: Session, buildings: list, activities: list, count: int = 100):
    """Create sample organizations"""
    organization_names = [
        "ООО Рога и Копыта", "ИП Иванов", "ЗАО ТехноСервис", "ООО Мясной Двор",
        "ИП Петрова", "ООО Электроника Плюс", "ЗАО АвтоМир", "ИП Сидоров",
        "ООО Хлебный Дом", "ЗАО Компьютерный Мир", "ИП Кузнецов", "ООО Молочные Продукты",
        "ЗАО АвтоЗапчасти", "ИП Смирнова", "ООО Связь Плюс", "ЗАО ГрузТранс",
        "ИП Новиков", "ООО Сырный Дом", "ЗАО Легковые Авто", "ИП Морозова"
    ]
    
    for i in range(count):
        organization = Organization(
            name=random.choice(organization_names),
            building_id=random.choice(buildings).id
        )
        db.add(organization)
        db.flush()
        
        # Add phone numbers
        phone_count = random.randint(1, 3)
        for _ in range(phone_count):
            phone = PhoneNumber(
                number=fake.phone_number(),
                organization_id=organization.id
            )
            db.add(phone)
        
        # Add activities
        activity_count = random.randint(1, 3)
        selected_activities = random.sample(activities, min(activity_count, len(activities)))
        organization.activities.extend(selected_activities)
    
    db.commit()


def seed_database(count: int = 100):
    """Seed the database with sample data"""
    db = SessionLocal()
    try:
        print("Creating buildings...")
        buildings = create_buildings(db, count // 5)
        
        print("Creating activities...")
        activities = create_activities(db)
        
        print("Creating organizations...")
        create_organizations(db, buildings, activities, count)
        
        print(f"Database seeded with {count} organizations!")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    seed_database(count)