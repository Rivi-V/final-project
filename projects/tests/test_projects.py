from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project
from users.models import User

PROJECTS_PER_PAGE = 12


class ProjectCoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            email='owner@example.com',
            password='password',
            name='Owner',
            surname='User',
        )
        cls.member = User.objects.create_user(
            email='member@example.com',
            password='password',
            name='Member',
            surname='User',
        )
        cls.owner_client = Client()
        cls.owner_client.force_login(cls.owner)
        cls.member_client = Client()
        cls.member_client.force_login(cls.member)

    def test_project_create_adds_owner_to_participants(self):
        response = self.owner_client.post(
            reverse('projects:create-slash'),
            {
                'name': 'New Project',
                'description': 'Description',
                'github_url': 'https://github.com/example/new-project',
                'status': Project.STATUS_OPEN,
            },
        )
        project = Project.objects.get(name='New Project')
        self.assertRedirects(
            response,
            reverse('projects:detail-no-slash', args=(project.id,)),
        )
        self.assertEqual(project.owner, self.owner)
        self.assertTrue(project.participants.filter(pk=self.owner.pk).exists())

    def test_favorites_participation_and_pagination(self):
        project = Project.objects.create(name='Pet', description='Desc', owner=self.owner)
        project.participants.add(self.owner)

        favorite_response = self.member_client.post(
            reverse('projects:toggle-favorite', args=(project.id,)),
        )
        self.assertTrue(favorite_response.json()['favorited'])

        participate_response = self.member_client.post(
            reverse('projects:toggle-participate', args=(project.id,)),
        )
        self.assertTrue(participate_response.json()['participant'])

        favorites_page = self.member_client.get(reverse('projects:favorites'))
        self.assertContains(favorites_page, 'Pet')

        participants_page = self.member_client.get(
            f"{reverse('users:list')}?filter=owners-of-favorite-projects"
        )
        participants = list(participants_page.context['participants'])
        self.assertEqual(participants, [self.owner])

        for idx in range(PROJECTS_PER_PAGE + 1):
            Project.objects.create(name=f'Project {idx}', owner=self.owner)
        response = self.client.get(reverse('projects:list-slash'))
        self.assertEqual(response.context['projects'].paginator.num_pages, 2)

    def test_complete_project(self):
        project = Project.objects.create(name='Closable', owner=self.owner)

        response = self.owner_client.post(
            reverse('projects:complete', args=(project.id,)),
        )
        updated_project = Project.objects.get(pk=project.pk)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(updated_project.status, Project.STATUS_CLOSED)
