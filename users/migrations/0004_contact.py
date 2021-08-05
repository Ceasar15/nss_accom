
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_nrh'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=190)),
                ('email', models.EmailField(max_length=190)),
                ('message', models.TextField()),
            ],
        ),
    ]


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_nrh'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=190)),
                ('email', models.EmailField(max_length=190)),
                ('message', models.TextField()),
            ],
        ),
    ]
<<<<<<< HEAD
>>>>>>> a5b01b2234453fd82e8165fe8a19cabbcc08cc9b
||||||| merged common ancestors
>>>>>>>>> Temporary merge branch 2
=======
>>>>>>> 9d410d34102b3c7620ba72b1991282c00f6d0e57
>>>>>>> 84f9f4ee7075db41e1d1bf66559cb3db6e9c758b
