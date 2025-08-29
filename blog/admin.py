from django.contrib import admin
from .models import Builder, SubAssembly, BuildRecord


# create builders
@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# create sub assemblies
@admin.register(SubAssembly)
class SubAssemblyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# create build record pulling from builder and subassembly
@admin.register(BuildRecord)
class BuildRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'builder', 'subassembly', 'time_minutes', 'build_date')
    list_filter = ('build_date', 'builder', 'subassembly')
    search_fields = ('builder__name', 'subassembly__name')
    ordering = ('time_minutes',)
