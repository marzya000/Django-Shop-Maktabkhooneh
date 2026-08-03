# گزارش پیاده‌سازی قابلیت Password Reset

## هدف

در این بخش قابلیت بازیابی رمز عبور (Password Reset) به پروژه اضافه شد تا کاربران بتوانند در صورت فراموش کردن رمز عبور، از طریق ایمیل رمز جدیدی برای حساب خود تنظیم کنند.

---

## مراحل انجام کار

برای پیاده‌سازی این قابلیت از سیستم احراز هویت داخلی Django استفاده شد.

مراحل انجام شده به صورت خلاصه:

1. ایجاد Viewهای مربوط به Password Reset با استفاده از کلاس‌های آماده Django:
   - PasswordResetView
   - PasswordResetDoneView
   - PasswordResetConfirmView
   - PasswordResetCompleteView

2. ایجاد URLهای مربوط به هر مرحله از فرآیند بازیابی رمز عبور.

3. ایجاد Templateهای اختصاصی برای صفحات:
   - password_reset.html
   - password_reset_done.html
   - password_reset_confirm.html
   - password_reset_complete.html

4. سفارشی‌سازی فرم Password Reset با ایجاد کلاس `CustomPasswordResetForm`.

5. ارسال ایمیل توسط Celery به جای ارسال مستقیم در Thread اصلی برنامه.

6. تنظیم محدودیت زمانی اعتبار توکن با استفاده از:

```python
PASSWORD_RESET_TIMEOUT = 60 * 60 * 48
```

که معادل ۴۸ ساعت است.

7. تست کامل فرآیند ارسال ایمیل و تغییر رمز عبور با استفاده از smtp4dev.

---

## دلیل استفاده از Celery

ارسال ایمیل عملیاتی زمان‌بر است و اگر به صورت مستقیم انجام شود، کاربر باید تا پایان ارسال ایمیل منتظر بماند.

به همین دلیل ارسال ایمیل به Workerهای Celery واگذار شد تا پاسخ درخواست سریع‌تر به کاربر نمایش داده شود.

---

## منابع استفاده شده

### مستندات رسمی Django

- https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.views.PasswordResetView

- https://docs.djangoproject.com/en/4.2/topics/email/

### مستندات Celery

- https://docs.celeryq.dev/

---

## استفاده از هوش مصنوعی

در این پروژه برای بررسی بهترین روش‌های پیاده‌سازی و رفع برخی مشکلات از ChatGPT استفاده شد.

نمونه Promptهای استفاده شده:

- How to customize Django PasswordResetView?
- How to send password reset email asynchronously using Celery?
- Best practices for Django Password Reset
- How to customize Django authentication templates
- How to integrate Bootstrap template with Django authentication forms

همچنین برای بررسی ساختار Templateها، نحوه سفارشی‌سازی فرم‌ها و رفع خطاهای احتمالی از راهنمایی ChatGPT استفاده شد.

---

## نتیجه

قابلیت Password Reset با ویژگی‌های زیر پیاده‌سازی شد:

- ارسال ایمیل توسط Celery
- استفاده از Token امن Django
- محدودیت زمانی ۴۸ ساعته برای Token
- قالب‌های اختصاصی برای صفحات Password Reset
- استفاده از Template اختصاصی ایمیل
- امکان تنظیم رمز عبور جدید توسط کاربر



## Best Practices بررسی شده

در پیاده‌سازی این بخش موارد زیر رعایت شد:

- استفاده از Token پیش‌فرض و امن Django
- تعیین زمان انقضای Token (48 ساعت)
- ارسال ایمیل به صورت Asynchronous با Celery
- عدم افشای وجود یا عدم وجود ایمیل ثبت‌شده در سیستم
- استفاده از Viewهای رسمی Django به جای پیاده‌سازی اختصاصی
- استفاده از Templateهای مجزا برای هر مرحله از فرآیند بازیابی رمز عبور