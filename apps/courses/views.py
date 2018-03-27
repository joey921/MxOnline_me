# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        #课程搜索
        # search_keywords = request.GET.get('keywords', "")
        # if search_keywords:
        #     all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        #课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses
        })
