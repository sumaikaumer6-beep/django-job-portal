from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Company, Applicant, UserProfile
from .forms import JobForm
# Create your views here.
def job_list_view(request):
    jobs = Job.objects.all().order_by('-posted_on')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Applicant.objects.filter(job=job,student=request.user.userprofile).exists()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if has_applied:
            messages.error(request, 'You are already applied')
        else:
            messages.error(request, 'please upload resume')
        return redirect('job_detail', pk=pk)
    context = {'job': job, 'has_applied': has_applied}
    return render(request, 'jobs/job_detail.html', context)
@login_required
def job_create_view(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile.is_employer:
            messages.error(request, 'Only employer can post jobs')
            return redirect('job_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'First make profile')
        return redirect('job_list')
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'First make company profile')
        return redirect('job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, 'Job posted successfully')
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})