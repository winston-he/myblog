from django.contrib import admin
from django.utils import timezone

from .models import Post, Comment, ViolationReport


# 博客审核
def approve_post(modeladmin, request, queryset):
    queryset.update(status=2)
    queryset.update_time = timezone.now()

approve_post.short_description = 'Approve selected blog(s)'

# 评论审核
def approve_comment(modeladmin, request, queryset):
    queryset.update(status=2)

# 举报审核
def approve_violation_report(modeladmin, request, queryset):
    for record in queryset:
        # 这是一篇博客
        if record.related_object_type == 0:
            Post.objects.filter(pk=record.related_object).update(status=3)
        # 这是一篇评论
        else:
            Comment.objects.filter(pk=record.related_object).delete()
    queryset.update(status=1, handled_by=request.user)

approve_comment.short_description = 'Approve selected comment(s)'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_time', 'status')
    list_filter = ('published_time', 'status')
    search_fields = ('title', )
    list_per_page = 5
    change_list_template = 'admin/blog_change_list.html'
    change_form_template = 'admin/blog_change_form.html'

    readonly_fields = ['create_time', 'update_time', 'published_time']

    actions = [approve_post, ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'create_time', 'post')
    list_filter = ('create_time', )
    search_fields = ('post', )

    actions = [approve_comment, ]

class ViolationReportAdmin(admin.ModelAdmin):
    readonly_fields = ['comment', 'related_object_type', 'related_object',  'violation_type', 'create_time', 'update_time', 'post_by', 'handled_by', 'status', ]
    list_filter = ('status', 'violation_type', 'related_object_type')
    change_form_template = "admin/violation_report_change_form.html"
    actions = [approve_violation_report, ]


    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        return super().render_change_form(request, context)



admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ViolationReport, ViolationReportAdmin)
