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
        db_table = 'areas'

    def __unicode__(self):
        return "%s - %s" % (self.idarea, self.nameareaes)
    
    def __str__(self):
        return "%s - %s" % (self.idarea, self.nameareaes)


class Competences(models.Model):
    idcompetence = models.AutoField(primary_key=True)
    fkarea = models.ForeignKey(Areas, models.DO_NOTHING, db_column='fkarea')
    codecompetence = models.CharField(max_length=5)
    namecompetenceen = models.CharField(max_length=155)
    namecompetencees = models.CharField(max_length=155)
    descriptioncompetenceen = models.CharField(max_length=350)
    descriptioncompetencees = models.CharField(max_length=350)

    class Meta:
        db_table = 'competences'

    def __unicode__(self):
        return "%s - %s - %s" % (self.idcompetence, self.fkarea, self.namecompetencees)
    
    def __str__(self):
        return "%s" % (self.namecompetencees)
        # return "%s - %s" % (self.namecompetencees, self.descriptioncompetencees)

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
        db_table = 'examples'

    def __unicode__(self):
        return "%d - %d - %d - %s" % (self.idexample, self.fklevel, self.fkcompetence, self.titlescenarioes)


class Groups(models.Model):
    idgroup = models.AutoField(primary_key=True)
    namegroupen = models.CharField(max_length=50)
    namegroupes = models.CharField(max_length=50)

    class Meta:
        db_table = 'groups'

    def __unicode__(self):
        return "%d - %s" % (self.idgroup, self.namegroupes)


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
        db_table = 'linecompetences'

    def __unicode__(self):
        return "%d - %d - %d" % (self.idline, self.fkcompetence, self.fklevel)


class Proficiencylevels(models.Model):
    idlevel = models.AutoField(primary_key=True)
    fkgroup = models.ForeignKey(Groups, models.DO_NOTHING, db_column='fkgroup')
    namelevelen = models.CharField(max_length=50)
    nameleveles = models.CharField(max_length=50)
    descriptionlevelen = models.CharField(max_length=155)
    descriptionleveles = models.CharField(max_length=155)

    class Meta:
        db_table = 'proficiencylevels'

    def __unicode__(self):
        return "%d - %d - %s" % (self.idlevel, self.fkgroup, self.nameleveles)


class Competenciasusuario(models.Model):
    idregistrocompusuario = models.AutoField(primary_key=True)
    fkcompetence = models.ForeignKey(Competences, models.DO_NOTHING, db_column='fkcompetence')
    fkuser = models.ForeignKey(User, models.DO_NOTHING, db_column='fkuser')
    tiene = models.BooleanField(blank=True, null=True)
    recomendacion = models.CharField(max_length=300, blank=True, null=True)
    
    class Meta:
        db_table = 'competenciasusuario'
        unique_together = (('fkcompetence', 'fkuser'),)
    
    def __str__(self):
        return "%s - %s - %s - %s - %s" % (self.idregistrocompusuario, self.fkcompetence, self.fkuser, self.tiene, self.recomendacion)
    