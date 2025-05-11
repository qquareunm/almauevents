import json

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Event, Registration, EventType, MainImage, SubCategory
from .forms import RegistrationForm
import openpyxl
from openpyxl.styles import Font
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import markdown


def index(request):
    event_type_id = request.GET.get('event_type', None)
    subcategory_id = request.GET.get('subcategory', None)

    events = Event.objects.all().order_by("date")
    main_image = MainImage.objects.first()
    event_types = EventType.objects.all()

    if event_type_id:
        events = events.filter(event_type_id=event_type_id)

    if subcategory_id:
        events = events.filter(subcategory_id=subcategory_id)

    # Получаем подкатегории для "Развлекательных мероприятий"
    entertainment_event_type = EventType.objects.filter(name="Развлекательные мероприятия").first()
    subcategories = SubCategory.objects.filter(event_type=entertainment_event_type) if entertainment_event_type else []

    return render(request, "index.html", {
        "events": events,
        "event_types": event_types,
        "selected_event_type": event_type_id,
        "subcategories": subcategories,  # Передаем подкатегории всегда
        "selected_subcategory": subcategory_id,
        'main_image': main_image,
    })



def calendar_page(request):
    """ Страница с календарем событий """
    events = Event.objects.all().values("id", "title", "date", "event_type__color")
    return render(request, "calendar.html", {"events": list(events)})

def calendar_view(request):
    """ Страница календаря с событиями """
    events = Event.objects.all().values("id", "title", "date", "event_type__color")
    events_list = []
    for event in events:
        events_list.append({
            "id": event["id"],
            "title": event["title"],
            "start": str(event["date"]),  # Преобразуем дату в строку
            "color": event["event_type__color"] if event["event_type__color"] else "#007bff"
        })

    events_json = json.dumps(events_list)

    return render(request, "calendar.html", {"events_json": events_json})


def event_detail(request, event_id):
    """ Детальная страница мероприятия """
    event = get_object_or_404(Event, id=event_id)

    # Обрабатываем Markdown для описания события
    event.description = markdown.markdown(event.description)

    error_message = None  # Создаем переменную для ошибки, которая будет отображаться в модальном окне

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Проверка на наличие уже существующей регистрации
            existing_registration = Registration.objects.filter(event=event, email=email).first()
            if existing_registration:
                error_message = "Вы уже зарегистрированы на это событие с этим email."
            else:
                # Если регистрации нет, сохраняем новую
                registration = form.save(commit=False)
                registration.event = event
                registration.save()

                # Отправка email пользователю
                try:
                    send_mail(
                        subject=f'Регистрация на {event.title}',
                        message=(
                            f'Здравствуйте, {registration.first_name}!\n\n'
                            f'Вы успешно зарегистрированы на мероприятие: {event.title}.\n'
                            f'📅 Дата: {event.date}\n'
                            f'🕒 Время: {event.start_time} - {event.end_time}\n'
                            f'📍 Место: {event.location}\n\n'
                            f'Спасибо за регистрацию!'
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[registration.email],
                        fail_silently=False,
                    )
                    print(f"✅ Email отправлен на {registration.email}")
                except Exception as e:
                    print(f"❌ Ошибка email: {str(e)}")

                return redirect("success")

        else:
            # Если форма невалидна
            error_message = "Ошибка при регистрации. Пожалуйста, проверьте данные и попробуйте снова."

    else:
        form = RegistrationForm()

    return render(request, "event_detail.html", {
        "event": event,
        "form": form,
        "error_message": error_message,  # Передаем ошибку в шаблон
    })




def success(request):
    """ Страница успешной регистрации """
    return render(request, "success.html")

@staff_member_required
def admin_settings(request):
    """Страница настроек для администратора"""
    if not request.user.is_staff:
        return redirect('index')  # Перенаправляем, если пользователь не админ

    return render(request, 'admin_settings.html')

@staff_member_required
def export_registrations_to_excel(request):
    """Экспорт данных о регистрациях в Excel с красивым оформлением"""
    registrations = Registration.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Регистрации"

    # Заголовки столбцов
    headers = ["Имя", "Фамилия", "Email", "Телефон", "Событие", "Дата регистрации"]

    header_font = Font(bold=True)  # Делаем заголовки жирными

    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font

    # Данные
    for row_num, reg in enumerate(registrations, start=2):
        sheet.cell(row=row_num, column=1, value=reg.first_name)
        sheet.cell(row=row_num, column=2, value=reg.last_name)
        sheet.cell(row=row_num, column=3, value=reg.email)
        sheet.cell(row=row_num, column=4, value=reg.phone_number)
        sheet.cell(row=row_num, column=5, value=reg.event.title)

        # красивое форматирование даты и времени
        created_at_display = reg.created_at.strftime("%d-%m-%Y %H:%M") if reg.created_at else "Не указано"
        sheet.cell(row=row_num, column=6, value=created_at_display)

    # Автоматическая ширина столбцов
    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Создание HTTP-ответа
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=registrations.xlsx"
    workbook.save(response)

    return response