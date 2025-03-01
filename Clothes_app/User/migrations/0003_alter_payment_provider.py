# Generated by Django 5.1.4 on 2025-03-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='provider',
            field=models.CharField(choices=[('stripe', 'Stripe'), ('paypal', 'Paypal'), ('google_pay', 'Google Pay'), ('apple_pay', 'Apple Pay')], max_length=50),
        ),
    ]
