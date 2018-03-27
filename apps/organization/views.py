# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CityDict, CourseOrg, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course


class OrgView(View):
    def get(self,request):
        all_city = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        #统计排名，点击量从高到低
        hot_orgs = all_orgs.order_by('-click_nums')

        #取出指定城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #筛选机构类别
        ct = request.GET.get('ct', '')
        if ct:
            all_orgs = all_orgs.filter(category=ct)

        #统计筛选出的机构数量
        org_nums = all_orgs.count()

        #根据学习人数据排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')


        # 统计筛选出的机构数量
        org_nums = all_orgs.count()
        #分页代码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_city': all_city,
            'all_orgs': orgs,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': ct,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })

class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)   #使用ModelForm可以直接生成一个model对象，对象有save方法可以直接保存数据到数据库
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')



class OrgHomeView(View):
    def get(self,request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_tearchs': all_teachers ,
            'course_org': course_org,
            'current_page':current_page,
        })


class OrgCourseView(View):
    def get(self,request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html',{
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgDescView(View):
    def get(self,request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    def get(self,request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',{
            'all_teachers': all_teachers,
            'current_page': current_page,
            'course_org': course_org,
        })


class AddFavView(View):
    """
    用户收藏，取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')