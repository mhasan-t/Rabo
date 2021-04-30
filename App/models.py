from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'category'


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    send_at = models.DateTimeField(blank=True, null=True)
    msg_text = models.TextField(blank=True, null=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    sent_by = models.ForeignKey(
        'User', on_delete=models.SET_NULL, db_column='sent_by', null=True)

    class Meta:
        managed = False
        db_table = 'message'


class Notice(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=11, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'notice'


class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    sent_to = models.ForeignKey(
        'User', on_delete=models.CASCADE, db_column='sent_to')
    sent_by = models.ForeignKey(
        'User', on_delete=models.SET_NULL, db_column='sent_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification'


class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=11, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    urgency = models.CharField(max_length=11, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dependent_on = models.ForeignKey(
        'self', on_delete=models.CASCADE, db_column='dependent_on')
    managed_by = models.ForeignKey(
        'User', on_delete=models.SET_NULL, db_column='managed_by')

    class Meta:
        managed = False
        db_table = 'task'


class WorksOn(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'works_on'
        unique_together = (('project', 'user'),)
