from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project
from team_finder.constants import PROJECTS_PER_PAGE
from users.models import User


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

    def test_toggle_favorite_adds_project_to_favorites(self):
        project = Project.objects.create(
            name='Pet',
            description='Desc',
            owner=self.owner,
        )

        response = self.member_client.post(
            reverse('projects:toggle-favorite', args=(project.id,)),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json()['favorited'])
        self.assertTrue(project.interested_users.filter(pk=self.member.pk).exists())

    def test_toggle_participate_adds_user_to_participants(self):
        project = Project.objects.create(
            name='Pet',
            description='Desc',
            owner=self.owner,
        )

        response = self.member_client.post(
            reverse('projects:toggle-participate', args=(project.id,)),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json()['participant'])
        self.assertTrue(project.participants.filter(pk=self.member.pk).exists())

    def test_favorites_page_displays_favorited_project(self):
        project = Project.objects.create(
            name='Pet',
            description='Desc',
            owner=self.owner,
        )
        project.interested_users.add(self.member)

        response = self.member_client.get(reverse('projects:favorites'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Pet')

    def test_users_filter_shows_owners_of_favorite_projects(self):
        project = Project.objects.create(
            name='Pet',
            description='Desc',
            owner=self.owner,
        )
        project.interested_users.add(self.member)

        response = self.member_client.get(
            f"{reverse('users:list')}?filter=owners-of-favorite-projects"
        )

        participants = list(response.context['participants'])
        self.assertEqual(participants, [self.owner])

    def test_project_list_pagination(self):
        for idx in range(PROJECTS_PER_PAGE + 1):
            Project.objects.create(
                name=f'Project {idx}',
                description='Desc',
                owner=self.owner,
            )

        response = self.client.get(reverse('projects:list-slash'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['projects'].paginator.num_pages, 2)

    def test_complete_project(self):
        project = Project.objects.create(
            name='Closable',
            description='Desc',
            owner=self.owner,
        )

        response = self.owner_client.post(
            reverse('projects:complete', args=(project.id,)),
        )
        updated_project = Project.objects.get(pk=project.pk)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(updated_project.status, Project.STATUS_CLOSED)
