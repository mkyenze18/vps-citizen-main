# Generated by Django 4.0.3 on 2022-07-01 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vps', '0022_remove_evidenceitemimage_evidence'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='evidence_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='item_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vps.evidenceitemcategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evidence',
            name='location',
            field=models.CharField(default='nairobi', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evidence',
            name='make',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='serial_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evidence',
            name='unit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='evidenceitemcategory',
            name='make',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evidenceitemcategory',
            name='model',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evidenceitemcategory',
            name='unit',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evidenceitemimage',
            name='evidence_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vps.evidence'),
        ),
        migrations.DeleteModel(
            name='EvidenceItem',
        ),
    ]