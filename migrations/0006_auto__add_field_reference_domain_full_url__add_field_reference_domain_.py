# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Reference_Domain.full_url'
        db.add_column(u'django_reference_data_reference_domain', 'full_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.protocol'
        db.add_column(u'django_reference_data_reference_domain', 'protocol',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.is_url_ok'
        db.add_column(u'django_reference_data_reference_domain', 'is_url_ok',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Reference_Domain.redirect_status'
        db.add_column(u'django_reference_data_reference_domain', 'redirect_status',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.redirect_full_url'
        db.add_column(u'django_reference_data_reference_domain', 'redirect_full_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.redirect_protocol'
        db.add_column(u'django_reference_data_reference_domain', 'redirect_protocol',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.redirect_domain_name'
        db.add_column(u'django_reference_data_reference_domain', 'redirect_domain_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.redirect_domain_path'
        db.add_column(u'django_reference_data_reference_domain', 'redirect_domain_path',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference_Domain.parent'
        db.add_column(u'django_reference_data_reference_domain', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_reference_data.Reference_Domain'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Reference_Domain.full_url'
        db.delete_column(u'django_reference_data_reference_domain', 'full_url')

        # Deleting field 'Reference_Domain.protocol'
        db.delete_column(u'django_reference_data_reference_domain', 'protocol')

        # Deleting field 'Reference_Domain.is_url_ok'
        db.delete_column(u'django_reference_data_reference_domain', 'is_url_ok')

        # Deleting field 'Reference_Domain.redirect_status'
        db.delete_column(u'django_reference_data_reference_domain', 'redirect_status')

        # Deleting field 'Reference_Domain.redirect_full_url'
        db.delete_column(u'django_reference_data_reference_domain', 'redirect_full_url')

        # Deleting field 'Reference_Domain.redirect_protocol'
        db.delete_column(u'django_reference_data_reference_domain', 'redirect_protocol')

        # Deleting field 'Reference_Domain.redirect_domain_name'
        db.delete_column(u'django_reference_data_reference_domain', 'redirect_domain_name')

        # Deleting field 'Reference_Domain.redirect_domain_path'
        db.delete_column(u'django_reference_data_reference_domain', 'redirect_domain_path')

        # Deleting field 'Reference_Domain.parent'
        db.delete_column(u'django_reference_data_reference_domain', 'parent_id')


    models = {
        u'django_reference_data.postal_code': {
            'Meta': {'object_name': 'Postal_Code'},
            'admin_code1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'admin_code2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'admin_code3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'admin_name1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'admin_name2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'admin_name3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'lat_long_accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_reference_data.reference_domain': {
            'Meta': {'object_name': 'Reference_Domain'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'domain_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'domain_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_multimedia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_news': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_url_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_reference_data.Reference_Domain']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'redirect_domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirect_domain_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirect_full_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirect_protocol': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'redirect_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_reference_data']