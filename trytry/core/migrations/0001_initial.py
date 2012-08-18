# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Flow'
        db.create_table('core_flow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flow_module', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('current_step', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('state', self.gf('django.db.models.fields.CharField')(default='active', max_length=64)),
        ))
        db.send_create_signal('core', ['Flow'])


    def backwards(self, orm):
        # Deleting model 'Flow'
        db.delete_table('core_flow')


    models = {
        'core.flow': {
            'Meta': {'object_name': 'Flow'},
            'current_step': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'flow_module': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '64'})
        }
    }

    complete_apps = ['core']