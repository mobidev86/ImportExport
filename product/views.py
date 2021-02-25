import csv

import xlwt
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from Import_Export.read_google_sheet import handle_url
from product.forms import UploadFileForm
from product.functions import handle_file
from product.models import Product, UploadedFile
from product.tasks import handle_file_task


# Create your views here


def set_scheduling(hour, minute, file_id):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone='Asia/Kolkata'
    )

    # handle_file_task.delay(file_id)

    PeriodicTask.objects.create(
        crontab=schedule,
        name="Import data daily",
        task='product.tasks.handle_file_task',
        args=([file_id, ])
    )


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form:
            if form.is_valid():
                file = form.cleaned_data.get('file')
                url = form.cleaned_data.get('url')
                time = request.POST.get('time')
                if file and time:
                    hour = time.split(':')[0]
                    minute = time.split(':')[1]
                    upload_file = UploadedFile.objects.create(file=file)
                    set_scheduling(hour=hour, minute=minute, file_id=upload_file.id)
                    message = f"Now Data will be imported daily at {hour}:{minute} "
                    return render(request, 'product/success.html', {'message': message})
                elif url and time:
                    pass

                elif file:
                    # creating file object in db
                    upload_file = UploadedFile.objects.create(file=file)

                    # handling file if user uploads the file
                    handle_file(upload_file.id)
                    message = "File successfully Uploaded."
                    return render(request, 'product/success.html', {'message': message})

                elif url:
                    # handling URL if user gives url
                    message = handle_url()
                    if message:
                        return HttpResponse(message)
                    message = "Google sheet Data is successfully imported."
                    return render(request, 'product/success.html', {'message': message})

            else:
                return render(request, 'product/index.html', {'form': form})
    else:
        form = UploadFileForm()
        return render(request, 'product/index.html', {'form': form})


class ProductList(ListView):
    template_name = 'product/success.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset


# this function will export the db data to excel file
def export_data_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    # set file name ..
    response['Content-Disposition'] = 'attachment; filename="new_export_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')  # this will make the sheet named Sheet1

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name', 'Description', 'Category', 'Brand', 'Color', 'Price', 'Size', 'Type', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # getting data from the db
    rows = Product.objects.all().values_list('product_name', 'description', 'category__category',
                                             'brand__brand', 'color__color', 'price', 'size', 'type')

    try:
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    except Exception as e:
        print(e)
    wb.save(response)
    return response


# this function will export the data to the csv file
def export_data_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="new_export_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Description', 'Category', 'Brand', 'Color', 'Price', 'Size', 'Type', ])

    # getting data from the db
    rows = Product.objects.all().values_list('product_name', 'description', 'category__category',
                                             'brand__brand', 'color__color', 'price', 'size', 'type')
    for row in rows:
        writer.writerow(row)

    return response
