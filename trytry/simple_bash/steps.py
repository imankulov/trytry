# -*- coding: utf-8 -*-
from trytry.core.steps import GenericStep



class GenericBashStep(GenericStep):

    def get_command(self, user_input):
        return (['bash', ], user_input)
