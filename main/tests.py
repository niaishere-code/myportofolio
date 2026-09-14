from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from main.models import Experience, Work


class ExperienceTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen Kalkulus 1",
            description="Membantu mahasiswa memahami dasar dan implementasi matematika",
            category="part-time",
        )
        self.experience_volunteer = Experience.objects.create(
            title="Event Staff Open House Fasilkom UI",
            description="Mengatur keberlangsungan pelaksanaan rangkaian event Open House Fasilkom UI",
            category="volunteer",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model1(self):
        self.assertEqual(str(self.experience), "Asisten Dosen Kalkulus 1")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_model2(self):
        self.assertEqual(str(self.experience_volunteer), "Event Staff Open House Fasilkom UI")
        self.assertEqual(self.experience_volunteer.category, "volunteer")
        self.assertTrue(self.experience_volunteer.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, self.experience_volunteer.title)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Volunteer")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience_volunteer.delete()

        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class WorksPageTest(TestCase):
    def setUp(self):
        self.business_case_works = [
            Work.objects.create(
                category="business_case",
                title="A.C.E. Strategy in Tackling Indonesia's Food Waste from MBG Program",
                year=2026,
                photo_bw="https://lh3.googleusercontent.com/d/1XHcdgrcaWcRAnz682l-4aeNTumaxMhD9",
                photo_color="https://lh3.googleusercontent.com/d/14vy1-Cw1KXEYIRj1TMrtI2gMot1AU4AM",
            ),
            Work.objects.create(
                category="business_case",
                title="Brewtique: Scalable Ecosystem & Uncompromised Premium Identity",
                year=2026,
                photo_bw="https://lh3.googleusercontent.com/d/1gOzy9c5WPLpIjmFJi0ckj6QIipnw9in0",
                photo_color="https://lh3.googleusercontent.com/d/1iMZ-IYn7kv0nsUUSb7xU0ZtevXpOCwgj",
            ),
            Work.objects.create(
                category="business_case",
                title="Arsitektur Pertumbuhan Ritel Lezza",
                year=2026,
                photo_bw="https://lh3.googleusercontent.com/d/19wUgv0GkUbVww3rwBWAHzp2HdA13FZFv",
                photo_color="https://lh3.googleusercontent.com/d/1A210OAXktOJLg01Uzqz-HK8vRr1Fy4eX",
            ),
            Work.objects.create(
                category="business_case",
                title="GreenStep Strategy in Optimizing BRI Green Loan Program",
                year=2026,
                photo_bw="https://lh3.googleusercontent.com/d/17pnJzPOqEzgqbhSiRLVGKEP67Lrl_gl9",
                photo_color="https://lh3.googleusercontent.com/d/1rzHmiFWAGC81yDY0obUEm7IWphI2Ka1O",
            ),
        ]

    def test_works_url_is_accessible(self):
        response = self.client.get(reverse("main:show_works"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "works.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_work_model1(self):
        work = self.business_case_works[0]

        self.assertEqual(str(work), "A.C.E. Strategy in Tackling Indonesia's Food Waste from MBG Program")
        self.assertEqual(work.category, "business_case")
        self.assertEqual(work.year, 2026)

    def test_work_model2(self):
        work = self.business_case_works[1]

        self.assertEqual(str(work), "Brewtique: Scalable Ecosystem & Uncompromised Premium Identity")
        self.assertEqual(work.category, "business_case")
        self.assertEqual(work.year, 2026)

    def test_work_model3(self):
        work = self.business_case_works[2]

        self.assertEqual(str(work), "Arsitektur Pertumbuhan Ritel Lezza")
        self.assertEqual(work.category, "business_case")
        self.assertEqual(work.year, 2026)

    def test_work_model4(self):
        work = self.business_case_works[3]

        self.assertEqual(str(work), "GreenStep Strategy in Optimizing BRI Green Loan Program")
        self.assertEqual(work.category, "business_case")
        self.assertEqual(work.year, 2026)

    def test_business_case_work_page_content(self):
        work = self.business_case_works[0]
        response = self.client.get(reverse("main:show_works"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "works.html")
        self.assertContains(response, escape(work.title))
        self.assertContains(response, work.year)
        self.assertContains(response, work.photo_bw)
        self.assertContains(response, work.photo_color)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_works_page_shows_empty_state_when_no_data(self):
        Work.objects.all().delete()
        response = self.client.get(reverse('main:show_works'))
        self.assertContains(response, 'Belum ada project di kategori ini.')