# Generated by Django 4.2.11 on 2024-06-26 19:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('quantity_in_stock', models.IntegerField()),
                ('rate', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('subtitle', models.CharField(max_length=255)),
                ('subscription', models.CharField(max_length=255)),
                ('features', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.color')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.subcategory')),
            ],
        ),
    ]
