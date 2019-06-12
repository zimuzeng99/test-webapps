from unittest import TestCase
from . import models
from . import views

projects = []

class ProjectSearchTestCase(TestCase):
    def setUp(self):
        project = models.Project()
        project.title = "Clean up Hyde Park"
        project.description = "Contribute towards the clean up of the Hyde Park, removing litter."
        project.latitude = 51.507568
        project.longitude = -0.166409
        project.type = "Environment"
        project.duration = 15.0
        projects.append(project)

        project = models.Project()
        project.title = "Rebuild houses destroyed in natural disasters"
        project.description = "Recent earthquakes have destroyed homes."
        project.latitude = 39.849393
        project.longitude = 116.437558
        project.type = "Building"
        project.duration = 50
        projects.append(project)

        project = models.Project()
        project.title = "Help locals in Africa"
        project.description = "Help them improve local infrastructure"
        project.latitude = -3.815922
        project.longitude = 20.380195
        project.type = "Infrastructure"
        project.duration = 45
        projects.append(project)

        project = models.Project()
        project.title = "Teaching a language"
        project.description = "Help young children learn a new foreign language."
        project.latitude = 51.511241
        project.longitude = -0.109625
        project.type = "Education"
        project.duration = 10
        projects.append(project)

    def testLocationFiltering(self):
        output = views.filter_projects(projects, None, None, 1, 51.507568, -0.166409)
        self.assertTrue(projects[0] in output)
        self.assertFalse(projects[1] in output)
        self.assertFalse(projects[2] in output)
        self.assertFalse(projects[3] in output)

        output = views.filter_projects(projects, None, None, 1000000, 40, 0)
        self.assertTrue(projects[0] in output)
        self.assertTrue(projects[1] in output)
        self.assertTrue(projects[2] in output)
        self.assertTrue(projects[3] in output)

    def testDurationFiltering(self):
        output = views.filter_projects(projects, 1, 16, None, None, None)
        self.assertTrue(projects[0] in output)
        self.assertFalse(projects[1] in output)
        self.assertFalse(projects[2] in output)
        self.assertTrue(projects[3] in output)

        output = views.filter_projects(projects, 0, 1, None, None, None)
        self.assertFalse(projects[0] in output)
        self.assertFalse(projects[1] in output)
        self.assertFalse(projects[2] in output)
        self.assertFalse(projects[3] in output)
