from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='currency',
            field=models.CharField(max_length=10, choices=[("USD", "USD"), ("UAH", "UAH")], default="UAH"),
        ),
    ]
