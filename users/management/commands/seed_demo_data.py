import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from projects.models import Project
from users.models import Skill, User


class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей и проекты для TeamFinder.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-file',
            default=Path(__file__).resolve().parent / 'data' / 'demo_data.json',
            help='Путь к JSON-файлу с тестовыми данными.',
        )

    def handle(self, *args, **options):
        data = self.load_data(options['data_file'])
        users = self.create_users(data.get('users', []))
        self.create_projects(data.get('projects', []), users)
        self.stdout.write(
            self.style.SUCCESS('Тестовые данные TeamFinder готовы.'),
        )

    def load_data(self, data_file):
        data_path = Path(data_file)
        if not data_path.exists():
            raise CommandError(f'Файл с данными не найден: {data_path}')

        with data_path.open(encoding='utf-8') as data_stream:
            return json.load(data_stream)

    def create_users(self, users_data):
        created_users = {}
        for item in users_data:
            user, created = User.objects.get_or_create(
                email=item['email'],
                defaults={
                    'name': item['name'],
                    'surname': item['surname'],
                    'about': item['about'],
                    'phone': item['phone'],
                    'github_url': item['github_url'],
                },
            )
            if created:
                user.set_password(item['password'])
                user.save()

            skills = [
                Skill.objects.get_or_create(name=skill_name)[0]
                for skill_name in item.get('skills', [])
            ]
            user.skills.add(*skills)
            created_users[user.email] = user

        return created_users

    def create_projects(self, projects_data, users):
        for item in projects_data:
            owner = users[item['owner']]
            project, _ = Project.objects.get_or_create(
                owner=owner,
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'github_url': item['github_url'],
                    'status': Project.STATUS_OPEN,
                },
            )

            skills = [
                Skill.objects.get_or_create(name=skill_name)[0]
                for skill_name in item.get('skills', [])
            ]
            participants = [
                users[email]
                for email in item.get('participants', [])
            ]
            project.skills.add(*skills)
            project.participants.add(*participants)
