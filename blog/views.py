from django.shortcuts import render, redirect, get_object_or_404
from .models import Builder, SubAssembly, BuildRecord
from django.db.models import Max, Sum, Min
from collections import defaultdict
from .forms import BuildRecordForm
import math


def leaderboard(request):
    subassemblies = list(SubAssembly.objects.all())
    total_subs = len(subassemblies)
    longest_times = {}

    # Pre-calculate the longest time for each subassembly
    for sub in subassemblies:
        max_time = BuildRecord.objects.filter(subassembly=sub).aggregate(Max('time_minutes'))['time_minutes__max']
        longest_times[sub.id] = max_time if max_time else 0

    leaderboard_data = []

    # Calculate total time per builder
    for builder in Builder.objects.all():
        builder_records = BuildRecord.objects.filter(builder=builder)
        sub_times = defaultdict(float)
        completed_sub_ids = set()

        for record in builder_records:
            sub_times[record.subassembly.id] += record.time_minutes
            completed_sub_ids.add(record.subassembly.id)

        total_time = sum(sub_times.values())
        is_incomplete = len(completed_sub_ids) < total_subs

        # If builder missed a subassembly, add double the longest time
        if is_incomplete:
            missing_subs = set(sub.id for sub in subassemblies) - completed_sub_ids
            penalty_time = sum(longest_times[sub_id] * 2 for sub_id in missing_subs)
            total_time += penalty_time

        leaderboard_data.append({
            'builder': builder,  # Pass the full object!
            'builder_display_name': builder.name + ('*' if is_incomplete else ''),
            'total_time': round(total_time, 2),
        })

    # Sort by total_time ascending
    leaderboard_data.sort(key=lambda x: x['total_time'])

    return render(request, 'blog/leaderboard.html', {'leaderboard': leaderboard_data})


SHARED_PASSWORD = "helenisn'treal"

SIGN_OFF_PASSWORDS = {
    "spedersen": "Steven",
    "gdoney": "Gavin",
    "dhughes": "Darius",
}


def submit_build_time(request):
    error_message = None
    if request.method == 'POST':
        form = BuildRecordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.pop('password')
            if password not in SIGN_OFF_PASSWORDS:
                error_message = "Incorrect password."
                # Clear password field on error
                form.data = form.data.copy()
                form.data['password'] = ''
            else:
                signed_off_by = SIGN_OFF_PASSWORDS[password]

                builder = form.cleaned_data['builder']
                subassembly = form.cleaned_data['subassembly']
                time_minutes = form.cleaned_data['time_minutes']
                build_date = form.cleaned_data['build_date']

                record, created = BuildRecord.objects.get_or_create(
                    builder=builder,
                    subassembly=subassembly,
                    defaults={
                        'time_minutes': time_minutes,
                        'build_date': build_date,
                        'signed_off_by': signed_off_by
                    }
                )
                if not created and time_minutes < record.time_minutes:
                    record.time_minutes = time_minutes
                    record.build_date = build_date
                    record.signed_off_by = signed_off_by
                    record.save()

                return redirect('leaderboard')

    else:
        form = BuildRecordForm()

    return render(request, 'blog/submit_build_time.html', {'form': form, 'error_message': error_message})



def builder_stats(request, builder_id):
    builder = Builder.objects.get(id=builder_id)
    subassemblies = SubAssembly.objects.all()
    records = []

    for sub in subassemblies:
        rec = BuildRecord.objects.filter(builder=builder, subassembly=sub).first()
        best_time = BuildRecord.objects.filter(subassembly=sub).order_by('time_minutes').first()

        if rec:
            time_behind = (rec.time_minutes - best_time.time_minutes) if best_time else None
            has_time_behind = True if time_behind is not None else False
            is_record_holder = (rec.time_minutes == best_time.time_minutes) if best_time else False
        else:
            time_behind = None
            has_time_behind = False
            is_record_holder = False

        records.append({
            'subassembly': sub.name,
            'builder_time': rec.time_minutes if rec else None,
            'build_date': rec.build_date if rec else None,
            'time_behind': time_behind,
            'has_time_behind': has_time_behind,
            'is_record_holder': is_record_holder,
            'signed_off_by': rec.signed_off_by if rec else None  # <-- Added
        })

    return render(request, 'blog/builder_stats.html', {'builder': builder, 'records': records})





# def builder_stats(request, builder_id):
#     builder = get_object_or_404(Builder, id=builder_id)
#     builder_records = BuildRecord.objects.filter(builder=builder).select_related('subassembly')
#
#     # Build record info with time behind best time
#     record_data = []
#     for record in builder_records:
#         best_time = BuildRecord.objects.filter(subassembly=record.subassembly).aggregate(Min('time_minutes'))['time_minutes__min']
#         time_behind = record.time_minutes - best_time if best_time is not None else 0
#         record_data.append({
#             'subassembly': record.subassembly.name,
#             'builder_time': record.time_minutes,
#             'build_date': record.build_date,
#             'time_behind': round(time_behind, 2) if time_behind > 0 else 0,
#         })
#
#     return render(request, 'blog/builder_stats.html', {
#         'builder': builder,
#         'records': record_data,
#     })




def subassembly_records(request):
    subassemblies = SubAssembly.objects.all()
    records = []

    for sub in subassemblies:
        best_record = BuildRecord.objects.filter(subassembly=sub).order_by('time_minutes', 'build_date').first()
        if best_record:
            records.append({
                'subassembly': sub.name,
                'builder': best_record.builder.name,
                'time': round(best_record.time_minutes, 2),
                'date': best_record.build_date,
            })
        else:
            records.append({
                'subassembly': sub.name,
                'builder': '—',
                'time': '—',
                'date': '—',
            })

    return render(request, 'blog/subassembly_records.html', {
        'records': records
    })
