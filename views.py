from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_ids = request.POST.getlist('choice')
    for choice_id in selected_ids:
        submission.choices.add(Choice.objects.get(id=choice_id))

    submission.save()

    # ✅ MUST redirect to show_exam_result
    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course.id,))
    )


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.filter(enrollment=enrollment).last()

    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    possible_score = 0

    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score,
    }

    return render(request, 'onlinecourse/exam_result.html', context)
