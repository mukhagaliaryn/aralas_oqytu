from progress.models import UserSubject

def active_subject_context(request):
    active_subject_id = None

    if request.user.is_authenticated and request.user.user_type == 'student':
        user_subjects = UserSubject.objects.filter(user=request.user)
        for user_subject in user_subjects:
            for chapter in user_subject.subject.chapters.all():
                chapter_url = f"/chapter/{user_subject.id}/{chapter.id}/"
                if request.path == chapter_url:
                    active_subject_id = user_subject.subject.id

    return {
        'active_subject_id': active_subject_id
    }
