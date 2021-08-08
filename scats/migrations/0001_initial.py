# Generated by Django 3.2.6 on 2021-08-07 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NB_SCATS_SITE', models.PositiveIntegerField()),
                ('QT_INTERVAL_COUNT', models.DateField()),
                ('NB_DETECTOR', models.PositiveSmallIntegerField()),
                ('V00', models.IntegerField()),
                ('V01', models.IntegerField()),
                ('V02', models.IntegerField()),
                ('V03', models.IntegerField()),
                ('V04', models.IntegerField()),
                ('V05', models.IntegerField()),
                ('V06', models.IntegerField()),
                ('V07', models.IntegerField()),
                ('V08', models.IntegerField()),
                ('V09', models.IntegerField()),
                ('V10', models.IntegerField()),
                ('V11', models.IntegerField()),
                ('V12', models.IntegerField()),
                ('V13', models.IntegerField()),
                ('V14', models.IntegerField()),
                ('V15', models.IntegerField()),
                ('V16', models.IntegerField()),
                ('V17', models.IntegerField()),
                ('V18', models.IntegerField()),
                ('V19', models.IntegerField()),
                ('V20', models.IntegerField()),
                ('V21', models.IntegerField()),
                ('V22', models.IntegerField()),
                ('V23', models.IntegerField()),
                ('V24', models.IntegerField()),
                ('V25', models.IntegerField()),
                ('V26', models.IntegerField()),
                ('V27', models.IntegerField()),
                ('V28', models.IntegerField()),
                ('V29', models.IntegerField()),
                ('V30', models.IntegerField()),
                ('V31', models.IntegerField()),
                ('V32', models.IntegerField()),
                ('V33', models.IntegerField()),
                ('V34', models.IntegerField()),
                ('V35', models.IntegerField()),
                ('V36', models.IntegerField()),
                ('V37', models.IntegerField()),
                ('V38', models.IntegerField()),
                ('V39', models.IntegerField()),
                ('V40', models.IntegerField()),
                ('V41', models.IntegerField()),
                ('V42', models.IntegerField()),
                ('V43', models.IntegerField()),
                ('V44', models.IntegerField()),
                ('V45', models.IntegerField()),
                ('V46', models.IntegerField()),
                ('V47', models.IntegerField()),
                ('V48', models.IntegerField()),
                ('V49', models.IntegerField()),
                ('V50', models.IntegerField()),
                ('V51', models.IntegerField()),
                ('V52', models.IntegerField()),
                ('V53', models.IntegerField()),
                ('V54', models.IntegerField()),
                ('V55', models.IntegerField()),
                ('V56', models.IntegerField()),
                ('V57', models.IntegerField()),
                ('V58', models.IntegerField()),
                ('V59', models.IntegerField()),
                ('V60', models.IntegerField()),
                ('V61', models.IntegerField()),
                ('V62', models.IntegerField()),
                ('V63', models.IntegerField()),
                ('V64', models.IntegerField()),
                ('V65', models.IntegerField()),
                ('V66', models.IntegerField()),
                ('V67', models.IntegerField()),
                ('V68', models.IntegerField()),
                ('V69', models.IntegerField()),
                ('V70', models.IntegerField()),
                ('V71', models.IntegerField()),
                ('V72', models.IntegerField()),
                ('V73', models.IntegerField()),
                ('V74', models.IntegerField()),
                ('V75', models.IntegerField()),
                ('V76', models.IntegerField()),
                ('V77', models.IntegerField()),
                ('V78', models.IntegerField()),
                ('V79', models.IntegerField()),
                ('V80', models.IntegerField()),
                ('V81', models.IntegerField()),
                ('V82', models.IntegerField()),
                ('V83', models.IntegerField()),
                ('V84', models.IntegerField()),
                ('V85', models.IntegerField()),
                ('V86', models.IntegerField()),
                ('V87', models.IntegerField()),
                ('V88', models.IntegerField()),
                ('V89', models.IntegerField()),
                ('V90', models.IntegerField()),
                ('V91', models.IntegerField()),
                ('V92', models.IntegerField()),
                ('V93', models.IntegerField()),
                ('V94', models.IntegerField()),
                ('V95', models.IntegerField()),
                ('NM_REGION', models.CharField(max_length=10)),
                ('CT_RECORDS', models.SmallIntegerField()),
                ('QT_VOLUME_24HOUR', models.IntegerField()),
                ('CT_ALARM_24HOUR', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
