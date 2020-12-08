# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Areas(models.Model):
    idarea = models.AutoField(primary_key=True)
    nameareaen = models.CharField(max_length=155)
    nameareaes = models.CharField(max_length=155)

    class Meta:
        managed = False
        db_table = 'areas'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Competences(models.Model):
    idcompetence = models.AutoField(primary_key=True)
    fkarea = models.ForeignKey(Areas, models.DO_NOTHING, db_column='fkarea')
    codecompetence = models.CharField(max_length=5)
    namecompetenceen = models.CharField(max_length=155)
    namecompetencees = models.CharField(max_length=155)
    descriptioncompetenceen = models.CharField(max_length=350)
    descriptioncompetencees = models.CharField(max_length=350)

    class Meta:
        managed = False
        db_table = 'competences'


class Competenciasusuario(models.Model):
    idregistrocompusuario = models.AutoField(primary_key=True)
    fkcompetence = models.ForeignKey(Competences, models.DO_NOTHING, db_column='fkcompetence')
    fkuser = models.ForeignKey(User, models.DO_NOTHING, db_column='fkuser')
    tiene = models.BooleanField(blank=True, null=True)
    recomendacion = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competenciasusuario'
        unique_together = (('fkcompetence', 'fkuser'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Examples(models.Model):
    idexample = models.AutoField(primary_key=True)
    fklevel = models.ForeignKey('Proficiencylevels', models.DO_NOTHING, db_column='fklevel')
    fkcompetence = models.ForeignKey(Competences, models.DO_NOTHING, db_column='fkcompetence')
    titlescenarioen = models.CharField(max_length=155)
    titlescenarioes = models.CharField(max_length=155)
    objectivescenarioen = models.CharField(max_length=155)
    objectivescenarioes = models.CharField(max_length=155)
    descriptionexampleen = models.CharField(max_length=780)
    descriptionexamplees = models.CharField(max_length=780)

    class Meta:
        managed = False
        db_table = 'examples'


class Groups(models.Model):
    idgroup = models.AutoField(primary_key=True)
    namegroupen = models.CharField(max_length=50)
    namegroupes = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'groups'


class Linecompetences(models.Model):
    idline = models.AutoField(primary_key=True)
    fkcompetence = models.ForeignKey(Competences, models.DO_NOTHING, db_column='fkcompetence')
    fklevel = models.ForeignKey('Proficiencylevels', models.DO_NOTHING, db_column='fklevel')
    verben = models.CharField(max_length=100)
    verbes = models.CharField(max_length=100)
    keywordsen = models.CharField(max_length=100)
    keywordses = models.CharField(max_length=100)
    linecompetenceen = models.CharField(max_length=350)
    linecompetencees = models.CharField(max_length=350)

    class Meta:
        managed = False
        db_table = 'linecompetences'


class Proficiencylevels(models.Model):
    idlevel = models.AutoField(primary_key=True)
    fkgroup = models.ForeignKey(Groups, models.DO_NOTHING, db_column='fkgroup')
    namelevelen = models.CharField(max_length=50)
    nameleveles = models.CharField(max_length=50)
    descriptionlevelen = models.CharField(max_length=155)
    descriptionleveles = models.CharField(max_length=155)

    class Meta:
        managed = False
        db_table = 'proficiencylevels'
