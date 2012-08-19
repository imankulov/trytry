# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table('core_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('command', self.gf('django.db.models.fields.TextField')()),
            ('out', self.gf('django.db.models.fields.TextField')(null=True)),
            ('err', self.gf('django.db.models.fields.TextField')(null=True)),
            ('flow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Flow'])),
        ))
        db.send_create_signal('core', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table('core_log')


    models = {
        'core.flow': {
            'Meta': {'object_name': 'Flow'},
            'current_step': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'flow_module': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '64'})
        },
        'core.log': {
            'Meta': {'object_name': 'Log'},
            'command': ('django.db.models.fields.TextField', [], {}),
            'err': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Flow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'out': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']