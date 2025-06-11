from django.shortcuts import render

def project_overview(request):
    context = {
        'title': "Medicaid Enrollment and Expenditure Forecasting Project",
        'objective': "To forecast annual Medicaid enrollments and expenditures both nationwide and state-specific for the next ten years.",
        'link': "https://emrts.us/2021/07/31/reflections-on-medicaid-enrollment-for-the-next-decade/"
    }
    return render(request, 'forecast/project.html', context)
