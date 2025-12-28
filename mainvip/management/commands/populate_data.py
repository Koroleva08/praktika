from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import random
from mainvip.models import Organization, VIPClient, Interaction, User, Role


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write("Начало заполнения базы данных...\n")
        
        # Создаем роли
        roles = self.create_roles()
        self.stdout.write("")
        
        # Создаем организации
        organizations = self.create_organizations()
        self.stdout.write("")
        
        # Создаем пользователей
        user2 = self.create_users(roles)
        all_users = list(User.objects.filter(is_active=True))
        self.stdout.write("")
        
        # Создаем VIP-клиентов
        clients = self.create_vip_clients(organizations)
        self.stdout.write("")
        
        # Создаем взаимодействия
        self.create_interactions(clients, all_users)
        self.stdout.write("")
        
        self.stdout.write(self.style.SUCCESS("\n✓ Заполнение базы данных завершено!"))
        self.stdout.write(f"\nСоздано:")
        self.stdout.write(f"  - Организаций: {len(organizations)}")
        self.stdout.write(f"  - VIP-клиентов: {len(clients)}")
        self.stdout.write(f"  - Пользователей: {len(all_users)}")
        self.stdout.write(f"\nДля входа используйте:")
        self.stdout.write(f"  Логин: test_user2")
        self.stdout.write(f"  Пароль: test_user2")

    def create_roles(self):
        """Создание ролей"""
        roles_data = [
            {'role_name': 'Администратор', 'permissions': 'Полный доступ к системе'},
            {'role_name': 'Менеджер по работе с клиентами', 'permissions': 'Управление VIP-клиентами и взаимодействиями'},
            {'role_name': 'Аналитик', 'permissions': 'Просмотр данных и формирование отчетов'},
        ]
        
        roles = []
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                role_name=role_data['role_name'],
                defaults=role_data
            )
            roles.append(role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Роль: {role.role_name}"))
        
        return roles

    def create_organizations(self):
        """Создание организаций"""
        organizations = [
            {
                'name': 'ООО "Технологические Решения"',
                'type': 'Партнерская организация',
                'address': 'г. Москва, ул. Ленина, д. 10',
                'website': 'https://tech-solutions.ru'
            },
            {
                'name': 'АНО "Научно-Исследовательский Центр"',
                'type': 'Научная организация',
                'address': 'г. Санкт-Петербург, пр. Невский, д. 25',
                'website': 'https://research-center.org'
            },
            {
                'name': 'ГБУ "Инновационный Парк"',
                'type': 'Государственная организация',
                'address': 'г. Казань, ул. Баумана, д. 58',
                'website': 'https://innopark.gov.ru'
            },
            {
                'name': 'ООО "Цифровые Технологии"',
                'type': 'IT-компания',
                'address': 'г. Новосибирск, ул. Красный проспект, д. 15',
                'website': 'https://digital-tech.com'
            },
            {
                'name': 'ФГБОУ ВО "Университет Инноваций"',
                'type': 'Образовательная организация',
                'address': 'г. Екатеринбург, ул. Мира, д. 19',
                'website': 'https://university-innov.ru'
            },
            {
                'name': 'ООО "Бизнес Консалтинг Групп"',
                'type': 'Консалтинговая компания',
                'address': 'г. Москва, ул. Тверская, д. 7',
                'website': 'https://bcg-consulting.ru'
            },
        ]
        
        created_orgs = []
        for org_data in organizations:
            org, created = Organization.objects.get_or_create(
                name=org_data['name'],
                defaults=org_data
            )
            created_orgs.append(org)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Организация: {org.name}"))
        
        return created_orgs

    def create_users(self, roles):
        """Создание пользователей"""
        user2, created = User.objects.get_or_create(
            username='test_user2',
            defaults={
                'email': 'test_user2@example.com',
                'full_name': 'Иванов Иван Иванович',
                'password': make_password('test_user2'),
                'is_staff': True,
                'is_active': True,
                'role': roles[1] if len(roles) > 1 else None,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Пользователь: {user2.username} ({user2.full_name})"))
        
        return user2

    def create_vip_clients(self, organizations):
        """Создание VIP-клиентов"""
        vip_clients_data = [
            {
                'full_name': 'Петров Петр Петрович',
                'position': 'Генеральный директор',
                'phone': '+7 (495) 123-45-67',
                'email': 'petrov@tech-solutions.ru',
                'organization': organizations[0] if organizations else None,
                'status': 'active',
                'notes': 'Ключевой партнер по совместным проектам в области IT-разработки. Руководитель стратегических инициатив.'
            },
            {
                'full_name': 'Сидорова Анна Владимировна',
                'position': 'Руководитель научных проектов',
                'phone': '+7 (812) 234-56-78',
                'email': 'sidorova@research-center.org',
                'organization': organizations[1] if len(organizations) > 1 else None,
                'status': 'active',
                'notes': 'Ответственное лицо за координацию научно-исследовательских проектов. Эксперт в области инновационных технологий.'
            },
            {
                'full_name': 'Козлов Дмитрий Сергеевич',
                'position': 'Директор инновационного парка',
                'phone': '+7 (843) 345-67-89',
                'email': 'kozlov@innopark.gov.ru',
                'organization': organizations[2] if len(organizations) > 2 else None,
                'status': 'active',
                'notes': 'Руководитель государственного инновационного парка. Координатор совместных программ развития.'
            },
            {
                'full_name': 'Морозова Елена Александровна',
                'position': 'Технический директор',
                'phone': '+7 (383) 456-78-90',
                'email': 'morozova@digital-tech.com',
                'organization': organizations[3] if len(organizations) > 3 else None,
                'status': 'active',
                'notes': 'Руководитель технических проектов. Партнер по разработке программного обеспечения.'
            },
            {
                'full_name': 'Волков Сергей Николаевич',
                'position': 'Проректор по научной работе',
                'phone': '+7 (343) 567-89-01',
                'email': 'volkov@university-innov.ru',
                'organization': organizations[4] if len(organizations) > 4 else None,
                'status': 'active',
                'notes': 'Руководитель совместных образовательных и научных программ. Координатор академических проектов.'
            },
            {
                'full_name': 'Новикова Мария Игоревна',
                'position': 'Руководитель отдела партнерств',
                'phone': '+7 (495) 678-90-12',
                'email': 'novikova@bcg-consulting.ru',
                'organization': organizations[5] if len(organizations) > 5 else None,
                'status': 'active',
                'notes': 'Ответственное лицо за развитие партнерских отношений. Эксперт по стратегическому планированию.'
            },
            {
                'full_name': 'Лебедев Алексей Викторович',
                'position': 'Заместитель генерального директора',
                'phone': '+7 (495) 789-01-23',
                'email': 'lebedev@tech-solutions.ru',
                'organization': organizations[0] if organizations else None,
                'status': 'active',
                'notes': 'Куратор совместных проектов. Ответственное лицо за координацию взаимодействия.'
            },
            {
                'full_name': 'Соколова Ольга Дмитриевна',
                'position': 'Начальник отдела инноваций',
                'phone': '+7 (812) 890-12-34',
                'email': 'sokolova@research-center.org',
                'organization': organizations[1] if len(organizations) > 1 else None,
                'status': 'potential',
                'notes': 'Потенциальный партнер по инновационным проектам. Эксперт в области исследований и разработок.'
            },
            {
                'full_name': 'Федоров Игорь Борисович',
                'position': 'Руководитель проектного офиса',
                'phone': '+7 (843) 901-23-45',
                'email': 'fedorov@innopark.gov.ru',
                'organization': organizations[2] if len(organizations) > 2 else None,
                'status': 'active',
                'notes': 'Координатор проектных инициатив. Ответственное лицо за реализацию совместных программ.'
            },
            {
                'full_name': 'Орлова Татьяна Сергеевна',
                'position': 'Директор по развитию',
                'phone': '+7 (383) 012-34-56',
                'email': 'orlova@digital-tech.com',
                'organization': organizations[3] if len(organizations) > 3 else None,
                'status': 'active',
                'notes': 'Руководитель стратегических направлений развития. Партнер по долгосрочным проектам.'
            },
            {
                'full_name': 'Григорьев Владимир Петрович',
                'position': 'Декан факультета информационных технологий',
                'phone': '+7 (343) 123-45-67',
                'email': 'grigoriev@university-innov.ru',
                'organization': organizations[4] if len(organizations) > 4 else None,
                'status': 'active',
                'notes': 'Руководитель образовательных программ. Координатор академического сотрудничества.'
            },
        ]
        
        created_clients = []
        for client_data in vip_clients_data:
            client, created = VIPClient.objects.get_or_create(
                email=client_data['email'],
                defaults=client_data
            )
            created_clients.append(client)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ VIP-клиент: {client.full_name} ({client.position})"))
        
        return created_clients

    def create_interactions(self, clients, users):
        """Создание взаимодействий"""
        interaction_types = ['meeting', 'email', 'call', 'project', 'agreement', 'other']
        channels = ['phone', 'email', 'in_person', 'online', 'other']
        
        descriptions = [
            'Обсуждение перспектив сотрудничества и совместных проектов',
            'Согласование условий партнерского соглашения',
            'Презентация новых технологических решений',
            'Координация работы по совместному проекту',
            'Обсуждение результатов проведенных исследований',
            'Планирование дальнейших шагов взаимодействия',
            'Согласование технических требований к проекту',
            'Обсуждение вопросов финансирования и ресурсов',
            'Презентация результатов работы',
            'Координация встречи с ключевыми участниками проекта',
        ]
        
        results = [
            'Достигнута договоренность о дальнейшем сотрудничестве',
            'Согласованы основные параметры проекта',
            'Определены сроки реализации инициативы',
            'Подготовлен план совместных действий',
            'Получено одобрение на продолжение работы',
            'Согласованы детали технического задания',
            'Определены приоритетные направления',
            'Достигнуто взаимопонимание по ключевым вопросам',
            'Подготовлены материалы для следующего этапа',
            'Согласована стратегия развития партнерства',
        ]
        
        # Создаем несколько взаимодействий для разных клиентов
        for i, client in enumerate(clients[:8]):  # Для первых 8 клиентов
            num_interactions = random.randint(2, 5)
            for j in range(num_interactions):
                interaction_date = date.today() - timedelta(days=random.randint(1, 90))
                interaction_type = random.choice(interaction_types)
                channel = random.choice(channels) if interaction_type in ['meeting', 'call'] else None
                
                Interaction.objects.create(
                    vip_client=client,
                    user=random.choice(users) if users else None,
                    date=interaction_date,
                    type=interaction_type,
                    channel=channel,
                    description=random.choice(descriptions),
                    result=random.choice(results),
                )
        
        self.stdout.write(self.style.SUCCESS(f"✓ Создано взаимодействий для VIP-клиентов"))


