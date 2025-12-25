from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = request.POST.getlist('choice')
    for choice_id in selected_choices:
        submission.choices.add(Choice.objects.get(id=choice_id))

    submission.score = submission.choices.filter(is_correct=True).count()
    submission.save()

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': submission.score
    })


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.filter(enrollment=enrollment).last()

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submission': submission
    })
