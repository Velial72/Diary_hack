from random import choice
from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject)


WORDS_OF_PRAISE = [
    "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!",
    "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!",
    "Очень хороший ответ!"
]

def get_schoolkid_by_name(name):
    try:
        Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик {name} не найден")
        return None
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {name}")
        return None


def create_commendation(child_name, subject_title):
    schoolkid = get_schoolkid_by_name(child_name)
    if schoolkid:
        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject_title
        ).order_by('-date').first()
        compliment = random.choice(WORDS_OF_PRAISE)
        commendation = Commendation.objects.create(
            text=compliment,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher,
        )


def remove_chastisements(child_name):
    schoolkid = get_schoolkid_by_name(child_name)
    if schoolkid:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()


def fix_marks(child_name):
    schoolkid = get_schoolkid_by_name(child_name)
    if schoolkid:
        bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        bad_marks.update(points=5)
