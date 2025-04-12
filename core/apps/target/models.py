# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Core(models.Model):
    seller = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.TextField()
    ean = models.BigIntegerField()
    date_now = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core'


class DularEans(models.Model):
    index = models.BigIntegerField(primary_key=True)
    idproduto = models.BigIntegerField(blank=True, null=True)
    idgradex = models.BigIntegerField(blank=True, null=True)
    idgradey = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    idmarca = models.BigIntegerField(blank=True, null=True)
    iddepartamento = models.BigIntegerField(blank=True, null=True)
    classificacao = models.BigIntegerField(blank=True, null=True)
    idcodigonbm = models.BigIntegerField(blank=True, null=True)
    ean = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dular_eans'


class DularLinks(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    sku = models.FloatField(db_column='SKU', blank=True, null=True)  # Field name made lowercase.
    cód_pai = models.FloatField(db_column='Cód PAI', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descrição = models.TextField(db_column='Descrição', blank=True, null=True)  # Field name made lowercase.
    m_livre = models.TextField(db_column='M_Livre', blank=True, null=True)  # Field name made lowercase.
    magalu = models.TextField(db_column='Magalu', blank=True, null=True)  # Field name made lowercase.
    carrefour = models.TextField(db_column='Carrefour', blank=True, null=True)  # Field name made lowercase.
    madeira = models.TextField(db_column='Madeira', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dular_links'


class Magalu(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.TextField()
    ean = models.BigIntegerField()
    date_now = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magalu'


class Mkt(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    sku = models.FloatField(db_column='SKU', blank=True, null=True)  # Field name made lowercase.
    cód_pai = models.FloatField(db_column='Cód PAI', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descrição = models.TextField(db_column='Descrição', blank=True, null=True)  # Field name made lowercase.
    valor_nf = models.FloatField(db_column='Valor NF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mercado_livre = models.FloatField(db_column='Mercado Livre', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    magalu = models.FloatField(db_column='MAGALU', blank=True, null=True)  # Field name made lowercase.
    via_varejo = models.FloatField(db_column='Via Varejo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    madeira = models.FloatField(db_column='Madeira', blank=True, null=True)  # Field name made lowercase.
    leroy = models.FloatField(db_column='Leroy', blank=True, null=True)  # Field name made lowercase.
    shopee = models.FloatField(db_column='Shopee', blank=True, null=True)  # Field name made lowercase.
    amazon = models.FloatField(db_column='Amazon', blank=True, null=True)  # Field name made lowercase.
    b2w = models.FloatField(db_column='B2W', blank=True, null=True)  # Field name made lowercase.
    colombo = models.FloatField(db_column='Colombo', blank=True, null=True)  # Field name made lowercase.
    carrefour = models.FloatField(db_column='Carrefour', blank=True, null=True)  # Field name made lowercase.
    dular_7_a_12x = models.FloatField(db_column='Dular 7 a 12x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dular_1_a_6x = models.FloatField(db_column='Dular 1 a 6x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dular_1x = models.FloatField(db_column='Dular 1x', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    internet = models.FloatField(db_column='Internet', blank=True, null=True)  # Field name made lowercase.
    search = models.TextField(blank=True, null=True)
    m_livre = models.TextField(db_column='M_Livre', blank=True, null=True)  # Field name made lowercase.
    magalu_0 = models.TextField(db_column='Magalu', blank=True, null=True)  # Field name made lowercase. Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'mkt'


class Search(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    m_livre = models.TextField(db_column='M_Livre', blank=True, null=True)  # Field name made lowercase.
    magalu = models.TextField(db_column='Magalu', blank=True, null=True)  # Field name made lowercase.
    carrefour = models.TextField(db_column='Carrefour', blank=True, null=True)  # Field name made lowercase.
    madeira = models.TextField(db_column='Madeira', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'search'
