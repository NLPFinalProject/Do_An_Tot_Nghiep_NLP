

class Migration(migrations.Migration):

    initial = True
    dependencies = [
        migrations.CreateModel(
            name='DataDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataDocumentName', models.CharField(max_length=1000)),
                ('DataDocumentType', models.CharField(max_length=10)),
                ('DataDocumentFile', models.FileField(max_length=1000, upload_to='DocumentFile/')),
                ('DataDocumentAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataDocumentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataDocumentFile', models.FileField(upload_to='DocumentFile/')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
