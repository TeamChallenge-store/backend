# Generated by Django 4.2.11 on 2024-07-03 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_comments_product_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Коментар', 'verbose_name_plural': 'Коментарі'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(default=1465, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product'),
            preserve_default=False,
        ),
    ]