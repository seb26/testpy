# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import os
import re
import shutil
import wikitools
# import hllib
import hlextract
import wikiUpload
from collections import defaultdict

import wconfig
wconfig = wconfig.config['tfwiki']


def u(s):
    if type(s) is type(u''):
        return s
    if type(s) is type(''):
        try:
            return unicode(s)
        except:
            try:
                return unicode(s.decode('utf8'))
            except:
                try:
                    return unicode(s.decode('windows-1252'))
                except:
                    return unicode(s, errors='ignore')
    try:
        return unicode(s)
    except:
        try:
            return u(str(s))
        except:
            return s


class Re(object):
      def __init__(self):
        self.last_match = None
      def match(self,pattern,text):
        self.last_match = re.match(pattern,text)
        return self.last_match
      def search(self,pattern,text):
        self.last_match = re.search(pattern,text)
        return self.last_match


class tf2extract:

    def __init__(self):
        self.config = {}
        self.config['set'] = True

        # Edit below.
        self.config['package'] = 'team fortress 2 content.gcf'
        self.config['packagedir'] = r'C:\Program Files (x86)\Steam\steamapps\team fortress 2 content.gcf'
        self.config['outdir'] = r'X:\Sebi\Desktop\tf2-extract\tf2'

        self.config['extractlist'] = [
            r'root\tf\resource\closecaption_brazilian.dat',
            r'root\tf\resource\closecaption_brazilian.txt',
            r'root\tf\resource\closecaption_danish.dat',
            r'root\tf\resource\closecaption_danish.txt',
            r'root\tf\resource\closecaption_dutch.dat',
            r'root\tf\resource\closecaption_dutch.txt',
            r'root\tf\resource\closecaption_english.dat',
            r'root\tf\resource\closecaption_english.txt',
            r'root\tf\resource\closecaption_finnish.dat',
            r'root\tf\resource\closecaption_finnish.txt',
            r'root\tf\resource\closecaption_french.dat',
            r'root\tf\resource\closecaption_french.txt',
            r'root\tf\resource\closecaption_german.dat',
            r'root\tf\resource\closecaption_german.txt',
            # r'root\tf\resource\closecaption_hungarian.dat', Doesn't exist? WTB Hungarians.
            r'root\tf\resource\closecaption_hungarian.txt',
            r'root\tf\resource\closecaption_italian.dat',
            r'root\tf\resource\closecaption_italian.txt',
            r'root\tf\resource\closecaption_japanese.dat',
            r'root\tf\resource\closecaption_japanese.txt',
            r'root\tf\resource\closecaption_korean.dat',
            r'root\tf\resource\closecaption_korean.txt',
            r'root\tf\resource\closecaption_koreana.dat',
            r'root\tf\resource\closecaption_koreana.txt',
            r'root\tf\resource\closecaption_norwegian.dat',
            r'root\tf\resource\closecaption_norwegian.txt',
            r'root\tf\resource\closecaption_polish.dat',
            r'root\tf\resource\closecaption_polish.txt',
            r'root\tf\resource\closecaption_portuguese.dat',
            r'root\tf\resource\closecaption_portuguese.txt',
            r'root\tf\resource\closecaption_romanian.dat',
            r'root\tf\resource\closecaption_romanian.txt',
            r'root\tf\resource\closecaption_russian.dat',
            r'root\tf\resource\closecaption_russian.txt',
            r'root\tf\resource\closecaption_schinese.dat',
            r'root\tf\resource\closecaption_schinese.txt',
            r'root\tf\resource\closecaption_spanish.dat',
            r'root\tf\resource\closecaption_spanish.txt',
            r'root\tf\resource\closecaption_swedish.dat',
            r'root\tf\resource\closecaption_swedish.txt',
            r'root\tf\resource\closecaption_tchinese.dat',
            r'root\tf\resource\closecaption_tchinese.txt',
            r'root\tf\resource\closecaption_turkish.dat',
            r'root\tf\resource\closecaption_turkish.txt',

            r'root\tf\resource\tf_brazilian.txt',
            r'root\tf\resource\tf_danish.txt',
            r'root\tf\resource\tf_dutch.txt',
            r'root\tf\resource\tf_english.txt',
            r'root\tf\resource\tf_finnish.txt',
            r'root\tf\resource\tf_french.txt',
            r'root\tf\resource\tf_german.txt',
            r'root\tf\resource\tf_hungarian.txt',
            r'root\tf\resource\tf_italian.txt',
            r'root\tf\resource\tf_japanese.txt',
            r'root\tf\resource\tf_korean.txt',
            r'root\tf\resource\tf_koreana.txt',
            r'root\tf\resource\tf_norwegian.txt',
            r'root\tf\resource\tf_polish.txt',
            r'root\tf\resource\tf_portuguese.txt',
            r'root\tf\resource\tf_romanian.txt',
            r'root\tf\resource\tf_russian.txt',
            r'root\tf\resource\tf_schinese.txt',
            r'root\tf\resource\tf_spanish.txt',
            r'root\tf\resource\tf_swedish.txt',
            r'root\tf\resource\tf_tchinese.txt',
            r'root\tf\resource\tf_turkish.txt',

            r'root\tf\maps\arena_badlands_danish.txt',
            r'root\tf\maps\arena_badlands_dutch.txt',
            r'root\tf\maps\arena_badlands_english.txt',
            r'root\tf\maps\arena_badlands_finnish.txt',
            r'root\tf\maps\arena_badlands_french.txt',
            r'root\tf\maps\arena_badlands_german.txt',
            r'root\tf\maps\arena_badlands_italian.txt',
            r'root\tf\maps\arena_badlands_japanese.txt',
            r'root\tf\maps\arena_badlands_korean.txt',
            r'root\tf\maps\arena_badlands_norwegian.txt',
            r'root\tf\maps\arena_badlands_polish.txt',
            r'root\tf\maps\arena_badlands_portuguese.txt',
            r'root\tf\maps\arena_badlands_russian.txt',
            r'root\tf\maps\arena_badlands_schinese.txt',
            r'root\tf\maps\arena_badlands_spanish.txt',
            r'root\tf\maps\arena_badlands_swedish.txt',
            r'root\tf\maps\arena_badlands_tchinese.txt',
            r'root\tf\maps\arena_granary_danish.txt',
            r'root\tf\maps\arena_granary_dutch.txt',
            r'root\tf\maps\arena_granary_english.txt',
            r'root\tf\maps\arena_granary_finnish.txt',
            r'root\tf\maps\arena_granary_french.txt',
            r'root\tf\maps\arena_granary_german.txt',
            r'root\tf\maps\arena_granary_italian.txt',
            r'root\tf\maps\arena_granary_japanese.txt',
            r'root\tf\maps\arena_granary_korean.txt',
            r'root\tf\maps\arena_granary_norwegian.txt',
            r'root\tf\maps\arena_granary_polish.txt',
            r'root\tf\maps\arena_granary_portuguese.txt',
            r'root\tf\maps\arena_granary_russian.txt',
            r'root\tf\maps\arena_granary_schinese.txt',
            r'root\tf\maps\arena_granary_spanish.txt',
            r'root\tf\maps\arena_granary_swedish.txt',
            r'root\tf\maps\arena_granary_tchinese.txt',
            r'root\tf\maps\arena_lumberyard_danish.txt',
            r'root\tf\maps\arena_lumberyard_dutch.txt',
            r'root\tf\maps\arena_lumberyard_english.txt',
            r'root\tf\maps\arena_lumberyard_finnish.txt',
            r'root\tf\maps\arena_lumberyard_french.txt',
            r'root\tf\maps\arena_lumberyard_german.txt',
            r'root\tf\maps\arena_lumberyard_italian.txt',
            r'root\tf\maps\arena_lumberyard_japanese.txt',
            r'root\tf\maps\arena_lumberyard_korean.txt',
            r'root\tf\maps\arena_lumberyard_norwegian.txt',
            r'root\tf\maps\arena_lumberyard_polish.txt',
            r'root\tf\maps\arena_lumberyard_portuguese.txt',
            r'root\tf\maps\arena_lumberyard_russian.txt',
            r'root\tf\maps\arena_lumberyard_schinese.txt',
            r'root\tf\maps\arena_lumberyard_spanish.txt',
            r'root\tf\maps\arena_lumberyard_swedish.txt',
            r'root\tf\maps\arena_lumberyard_tchinese.txt',
            r'root\tf\maps\arena_nucleus_danish.txt',
            r'root\tf\maps\arena_nucleus_dutch.txt',
            r'root\tf\maps\arena_nucleus_english.txt',
            r'root\tf\maps\arena_nucleus_finnish.txt',
            r'root\tf\maps\arena_nucleus_french.txt',
            r'root\tf\maps\arena_nucleus_german.txt',
            r'root\tf\maps\arena_nucleus_italian.txt',
            r'root\tf\maps\arena_nucleus_japanese.txt',
            r'root\tf\maps\arena_nucleus_korean.txt',
            r'root\tf\maps\arena_nucleus_norwegian.txt',
            r'root\tf\maps\arena_nucleus_polish.txt',
            r'root\tf\maps\arena_nucleus_portuguese.txt',
            r'root\tf\maps\arena_nucleus_russian.txt',
            r'root\tf\maps\arena_nucleus_schinese.txt',
            r'root\tf\maps\arena_nucleus_spanish.txt',
            r'root\tf\maps\arena_nucleus_swedish.txt',
            r'root\tf\maps\arena_nucleus_tchinese.txt',
            r'root\tf\maps\arena_ravine_danish.txt',
            r'root\tf\maps\arena_ravine_dutch.txt',
            r'root\tf\maps\arena_ravine_english.txt',
            r'root\tf\maps\arena_ravine_finnish.txt',
            r'root\tf\maps\arena_ravine_french.txt',
            r'root\tf\maps\arena_ravine_german.txt',
            r'root\tf\maps\arena_ravine_italian.txt',
            r'root\tf\maps\arena_ravine_japanese.txt',
            r'root\tf\maps\arena_ravine_korean.txt',
            r'root\tf\maps\arena_ravine_norwegian.txt',
            r'root\tf\maps\arena_ravine_polish.txt',
            r'root\tf\maps\arena_ravine_portuguese.txt',
            r'root\tf\maps\arena_ravine_russian.txt',
            r'root\tf\maps\arena_ravine_schinese.txt',
            r'root\tf\maps\arena_ravine_spanish.txt',
            r'root\tf\maps\arena_ravine_swedish.txt',
            r'root\tf\maps\arena_ravine_tchinese.txt',
            r'root\tf\maps\arena_sawmill_danish.txt',
            r'root\tf\maps\arena_sawmill_dutch.txt',
            r'root\tf\maps\arena_sawmill_english.txt',
            r'root\tf\maps\arena_sawmill_finnish.txt',
            r'root\tf\maps\arena_sawmill_french.txt',
            r'root\tf\maps\arena_sawmill_german.txt',
            r'root\tf\maps\arena_sawmill_italian.txt',
            r'root\tf\maps\arena_sawmill_japanese.txt',
            r'root\tf\maps\arena_sawmill_korean.txt',
            r'root\tf\maps\arena_sawmill_norwegian.txt',
            r'root\tf\maps\arena_sawmill_polish.txt',
            r'root\tf\maps\arena_sawmill_portuguese.txt',
            r'root\tf\maps\arena_sawmill_russian.txt',
            r'root\tf\maps\arena_sawmill_schinese.txt',
            r'root\tf\maps\arena_sawmill_spanish.txt',
            r'root\tf\maps\arena_sawmill_swedish.txt',
            r'root\tf\maps\arena_sawmill_tchinese.txt',
            r'root\tf\maps\arena_watchtower.txt',
            r'root\tf\maps\arena_well_danish.txt',
            r'root\tf\maps\arena_well_dutch.txt',
            r'root\tf\maps\arena_well_english.txt',
            r'root\tf\maps\arena_well_finnish.txt',
            r'root\tf\maps\arena_well_french.txt',
            r'root\tf\maps\arena_well_german.txt',
            r'root\tf\maps\arena_well_italian.txt',
            r'root\tf\maps\arena_well_japanese.txt',
            r'root\tf\maps\arena_well_korean.txt',
            r'root\tf\maps\arena_well_norwegian.txt',
            r'root\tf\maps\arena_well_polish.txt',
            r'root\tf\maps\arena_well_portuguese.txt',
            r'root\tf\maps\arena_well_russian.txt',
            r'root\tf\maps\arena_well_schinese.txt',
            r'root\tf\maps\arena_well_spanish.txt',
            r'root\tf\maps\arena_well_swedish.txt',
            r'root\tf\maps\arena_well_tchinese.txt',
            r'root\tf\maps\cp_5gorge_danish.txt',
            r'root\tf\maps\cp_5gorge_dutch.txt',
            r'root\tf\maps\cp_5gorge_english.txt',
            r'root\tf\maps\cp_5gorge_finnish.txt',
            r'root\tf\maps\cp_5gorge_french.txt',
            r'root\tf\maps\cp_5gorge_german.txt',
            r'root\tf\maps\cp_5gorge_italian.txt',
            r'root\tf\maps\cp_5gorge_japanese.txt',
            r'root\tf\maps\cp_5gorge_korean.txt',
            r'root\tf\maps\cp_5gorge_norwegian.txt',
            r'root\tf\maps\cp_5gorge_polish.txt',
            r'root\tf\maps\cp_5gorge_portuguese.txt',
            r'root\tf\maps\cp_5gorge_russian.txt',
            r'root\tf\maps\cp_5gorge_schinese.txt',
            r'root\tf\maps\cp_5gorge_spanish.txt',
            r'root\tf\maps\cp_5gorge_swedish.txt',
            r'root\tf\maps\cp_5gorge_tchinese.txt',
            r'root\tf\maps\cp_badlands_danish.txt',
            r'root\tf\maps\cp_badlands_dutch.txt',
            r'root\tf\maps\cp_badlands_english.txt',
            r'root\tf\maps\cp_badlands_finnish.txt',
            r'root\tf\maps\cp_badlands_french.txt',
            r'root\tf\maps\cp_badlands_german.txt',
            r'root\tf\maps\cp_badlands_italian.txt',
            r'root\tf\maps\cp_badlands_japanese.txt',
            r'root\tf\maps\cp_badlands_korean.txt',
            r'root\tf\maps\cp_badlands_norwegian.txt',
            r'root\tf\maps\cp_badlands_polish.txt',
            r'root\tf\maps\cp_badlands_portuguese.txt',
            r'root\tf\maps\cp_badlands_russian.txt',
            r'root\tf\maps\cp_badlands_schinese.txt',
            r'root\tf\maps\cp_badlands_spanish.txt',
            r'root\tf\maps\cp_badlands_swedish.txt',
            r'root\tf\maps\cp_badlands_tchinese.txt',
            r'root\tf\maps\cp_coldfront_danish.txt',
            r'root\tf\maps\cp_coldfront_dutch.txt',
            r'root\tf\maps\cp_coldfront_english.txt',
            r'root\tf\maps\cp_coldfront_finnish.txt',
            r'root\tf\maps\cp_coldfront_french.txt',
            r'root\tf\maps\cp_coldfront_german.txt',
            r'root\tf\maps\cp_coldfront_italian.txt',
            r'root\tf\maps\cp_coldfront_japanese.txt',
            r'root\tf\maps\cp_coldfront_korean.txt',
            r'root\tf\maps\cp_coldfront_norwegian.txt',
            r'root\tf\maps\cp_coldfront_particles.txt',
            r'root\tf\maps\cp_coldfront_polish.txt',
            r'root\tf\maps\cp_coldfront_portuguese.txt',
            r'root\tf\maps\cp_coldfront_russian.txt',
            r'root\tf\maps\cp_coldfront_schinese.txt',
            r'root\tf\maps\cp_coldfront_spanish.txt',
            r'root\tf\maps\cp_coldfront_swedish.txt',
            r'root\tf\maps\cp_coldfront_tchinese.txt',
            r'root\tf\maps\cp_degrootkeep_english.txt',
            r'root\tf\maps\cp_dustbowl_danish.txt',
            r'root\tf\maps\cp_dustbowl_dutch.txt',
            r'root\tf\maps\cp_dustbowl_english.txt',
            r'root\tf\maps\cp_dustbowl_finnish.txt',
            r'root\tf\maps\cp_dustbowl_french.txt',
            r'root\tf\maps\cp_dustbowl_german.txt',
            r'root\tf\maps\cp_dustbowl_italian.txt',
            r'root\tf\maps\cp_dustbowl_japanese.txt',
            r'root\tf\maps\cp_dustbowl_korean.txt',
            r'root\tf\maps\cp_dustbowl_norwegian.txt',
            r'root\tf\maps\cp_dustbowl_polish.txt',
            r'root\tf\maps\cp_dustbowl_portuguese.txt',
            r'root\tf\maps\cp_dustbowl_russian.txt',
            r'root\tf\maps\cp_dustbowl_schinese.txt',
            r'root\tf\maps\cp_dustbowl_spanish.txt',
            r'root\tf\maps\cp_dustbowl_swedish.txt',
            r'root\tf\maps\cp_dustbowl_tchinese.txt',
            r'root\tf\maps\cp_fastlane_english.txt',
            r'root\tf\maps\cp_gorge_danish.txt',
            r'root\tf\maps\cp_gorge_dutch.txt',
            r'root\tf\maps\cp_gorge_english.txt',
            r'root\tf\maps\cp_gorge_finnish.txt',
            r'root\tf\maps\cp_gorge_french.txt',
            r'root\tf\maps\cp_gorge_german.txt',
            r'root\tf\maps\cp_gorge_italian.txt',
            r'root\tf\maps\cp_gorge_japanese.txt',
            r'root\tf\maps\cp_gorge_korean.txt',
            r'root\tf\maps\cp_gorge_norwegian.txt',
            r'root\tf\maps\cp_gorge_polish.txt',
            r'root\tf\maps\cp_gorge_portuguese.txt',
            r'root\tf\maps\cp_gorge_russian.txt',
            r'root\tf\maps\cp_gorge_schinese.txt',
            r'root\tf\maps\cp_gorge_spanish.txt',
            r'root\tf\maps\cp_gorge_swedish.txt',
            r'root\tf\maps\cp_gorge_tchinese.txt',
            r'root\tf\maps\cp_granary_danish.txt',
            r'root\tf\maps\cp_granary_dutch.txt',
            r'root\tf\maps\cp_granary_english.txt',
            r'root\tf\maps\cp_granary_finnish.txt',
            r'root\tf\maps\cp_granary_french.txt',
            r'root\tf\maps\cp_granary_german.txt',
            r'root\tf\maps\cp_granary_italian.txt',
            r'root\tf\maps\cp_granary_japanese.txt',
            r'root\tf\maps\cp_granary_korean.txt',
            r'root\tf\maps\cp_granary_norwegian.txt',
            r'root\tf\maps\cp_granary_polish.txt',
            r'root\tf\maps\cp_granary_portuguese.txt',
            r'root\tf\maps\cp_granary_russian.txt',
            r'root\tf\maps\cp_granary_schinese.txt',
            r'root\tf\maps\cp_granary_spanish.txt',
            r'root\tf\maps\cp_granary_swedish.txt',
            r'root\tf\maps\cp_granary_tchinese.txt',
            r'root\tf\maps\cp_gravelpit_commentary.txt',
            r'root\tf\maps\cp_gravelpit_danish.txt',
            r'root\tf\maps\cp_gravelpit_dutch.txt',
            r'root\tf\maps\cp_gravelpit_english.txt',
            r'root\tf\maps\cp_gravelpit_finnish.txt',
            r'root\tf\maps\cp_gravelpit_french.txt',
            r'root\tf\maps\cp_gravelpit_german.txt',
            r'root\tf\maps\cp_gravelpit_italian.txt',
            r'root\tf\maps\cp_gravelpit_japanese.txt',
            r'root\tf\maps\cp_gravelpit_korean.txt',
            r'root\tf\maps\cp_gravelpit_norwegian.txt',
            r'root\tf\maps\cp_gravelpit_polish.txt',
            r'root\tf\maps\cp_gravelpit_portuguese.txt',
            r'root\tf\maps\cp_gravelpit_russian.txt',
            r'root\tf\maps\cp_gravelpit_schinese.txt',
            r'root\tf\maps\cp_gravelpit_spanish.txt',
            r'root\tf\maps\cp_gravelpit_swedish.txt',
            r'root\tf\maps\cp_gravelpit_tchinese.txt',
            r'root\tf\maps\cp_gullywash_final1_english.txt',
            r'root\tf\maps\cp_manor_event_danish.txt',
            r'root\tf\maps\cp_manor_event_dutch.txt',
            r'root\tf\maps\cp_manor_event_english.txt',
            r'root\tf\maps\cp_manor_event_finnish.txt',
            r'root\tf\maps\cp_manor_event_french.txt',
            r'root\tf\maps\cp_manor_event_german.txt',
            r'root\tf\maps\cp_manor_event_italian.txt',
            r'root\tf\maps\cp_manor_event_japanese.txt',
            r'root\tf\maps\cp_manor_event_korean.txt',
            r'root\tf\maps\cp_manor_event_norwegian.txt',
            r'root\tf\maps\cp_manor_event_polish.txt',
            r'root\tf\maps\cp_manor_event_portuguese.txt',
            r'root\tf\maps\cp_manor_event_russian.txt',
            r'root\tf\maps\cp_manor_event_schinese.txt',
            r'root\tf\maps\cp_manor_event_spanish.txt',
            r'root\tf\maps\cp_manor_event_swedish.txt',
            r'root\tf\maps\cp_manor_event_tchinese.txt',
            r'root\tf\maps\cp_mountainlab_danish.txt',
            r'root\tf\maps\cp_mountainlab_dutch.txt',
            r'root\tf\maps\cp_mountainlab_english.txt',
            r'root\tf\maps\cp_mountainlab_finnish.txt',
            r'root\tf\maps\cp_mountainlab_french.txt',
            r'root\tf\maps\cp_mountainlab_german.txt',
            r'root\tf\maps\cp_mountainlab_italian.txt',
            r'root\tf\maps\cp_mountainlab_japanese.txt',
            r'root\tf\maps\cp_mountainlab_korean.txt',
            r'root\tf\maps\cp_mountainlab_norwegian.txt',
            r'root\tf\maps\cp_mountainlab_polish.txt',
            r'root\tf\maps\cp_mountainlab_portuguese.txt',
            r'root\tf\maps\cp_mountainlab_russian.txt',
            r'root\tf\maps\cp_mountainlab_schinese.txt',
            r'root\tf\maps\cp_mountainlab_spanish.txt',
            r'root\tf\maps\cp_mountainlab_swedish.txt',
            r'root\tf\maps\cp_mountainlab_tchinese.txt',
            r'root\tf\maps\cp_steel.txt',
            r'root\tf\maps\cp_well_commentary.txt',
            r'root\tf\maps\cp_well_danish.txt',
            r'root\tf\maps\cp_well_dutch.txt',
            r'root\tf\maps\cp_well_english.txt',
            r'root\tf\maps\cp_well_finnish.txt',
            r'root\tf\maps\cp_well_french.txt',
            r'root\tf\maps\cp_well_german.txt',
            r'root\tf\maps\cp_well_italian.txt',
            r'root\tf\maps\cp_well_japanese.txt',
            r'root\tf\maps\cp_well_korean.txt',
            r'root\tf\maps\cp_well_norwegian.txt',
            r'root\tf\maps\cp_well_polish.txt',
            r'root\tf\maps\cp_well_portuguese.txt',
            r'root\tf\maps\cp_well_russian.txt',
            r'root\tf\maps\cp_well_schinese.txt',
            r'root\tf\maps\cp_well_spanish.txt',
            r'root\tf\maps\cp_well_swedish.txt',
            r'root\tf\maps\cp_well_tchinese.txt',
            r'root\tf\maps\ctf_2fort_danish.txt',
            r'root\tf\maps\ctf_2fort_dutch.txt',
            r'root\tf\maps\ctf_2fort_english.txt',
            r'root\tf\maps\ctf_2fort_finnish.txt',
            r'root\tf\maps\ctf_2fort_french.txt',
            r'root\tf\maps\ctf_2fort_german.txt',
            r'root\tf\maps\ctf_2fort_italian.txt',
            r'root\tf\maps\ctf_2fort_japanese.txt',
            r'root\tf\maps\ctf_2fort_korean.txt',
            r'root\tf\maps\ctf_2fort_norwegian.txt',
            r'root\tf\maps\ctf_2fort_polish.txt',
            r'root\tf\maps\ctf_2fort_portuguese.txt',
            r'root\tf\maps\ctf_2fort_russian.txt',
            r'root\tf\maps\ctf_2fort_schinese.txt',
            r'root\tf\maps\ctf_2fort_spanish.txt',
            r'root\tf\maps\ctf_2fort_swedish.txt',
            r'root\tf\maps\ctf_2fort_tchinese.txt',
            r'root\tf\maps\ctf_doublecross_danish.txt',
            r'root\tf\maps\ctf_doublecross_dutch.txt',
            r'root\tf\maps\ctf_doublecross_english.txt',
            r'root\tf\maps\ctf_doublecross_finnish.txt',
            r'root\tf\maps\ctf_doublecross_french.txt',
            r'root\tf\maps\ctf_doublecross_german.txt',
            r'root\tf\maps\ctf_doublecross_italian.txt',
            r'root\tf\maps\ctf_doublecross_japanese.txt',
            r'root\tf\maps\ctf_doublecross_korean.txt',
            r'root\tf\maps\ctf_doublecross_norwegian.txt',
            r'root\tf\maps\ctf_doublecross_polish.txt',
            r'root\tf\maps\ctf_doublecross_portuguese.txt',
            r'root\tf\maps\ctf_doublecross_russian.txt',
            r'root\tf\maps\ctf_doublecross_schinese.txt',
            r'root\tf\maps\ctf_doublecross_spanish.txt',
            r'root\tf\maps\ctf_doublecross_swedish.txt',
            r'root\tf\maps\ctf_doublecross_tchinese.txt',
            r'root\tf\maps\ctf_sawmill_danish.txt',
            r'root\tf\maps\ctf_sawmill_dutch.txt',
            r'root\tf\maps\ctf_sawmill_english.txt',
            r'root\tf\maps\ctf_sawmill_finnish.txt',
            r'root\tf\maps\ctf_sawmill_french.txt',
            r'root\tf\maps\ctf_sawmill_german.txt',
            r'root\tf\maps\ctf_sawmill_italian.txt',
            r'root\tf\maps\ctf_sawmill_japanese.txt',
            r'root\tf\maps\ctf_sawmill_korean.txt',
            r'root\tf\maps\ctf_sawmill_norwegian.txt',
            r'root\tf\maps\ctf_sawmill_polish.txt',
            r'root\tf\maps\ctf_sawmill_portuguese.txt',
            r'root\tf\maps\ctf_sawmill_russian.txt',
            r'root\tf\maps\ctf_sawmill_schinese.txt',
            r'root\tf\maps\ctf_sawmill_spanish.txt',
            r'root\tf\maps\ctf_sawmill_swedish.txt',
            r'root\tf\maps\ctf_sawmill_tchinese.txt',
            r'root\tf\maps\ctf_turbine_english.txt',
            r'root\tf\maps\ctf_well_danish.txt',
            r'root\tf\maps\ctf_well_dutch.txt',
            r'root\tf\maps\ctf_well_english.txt',
            r'root\tf\maps\ctf_well_finnish.txt',
            r'root\tf\maps\ctf_well_french.txt',
            r'root\tf\maps\ctf_well_german.txt',
            r'root\tf\maps\ctf_well_italian.txt',
            r'root\tf\maps\ctf_well_japanese.txt',
            r'root\tf\maps\ctf_well_korean.txt',
            r'root\tf\maps\ctf_well_norwegian.txt',
            r'root\tf\maps\ctf_well_polish.txt',
            r'root\tf\maps\ctf_well_portuguese.txt',
            r'root\tf\maps\ctf_well_russian.txt',
            r'root\tf\maps\ctf_well_schinese.txt',
            r'root\tf\maps\ctf_well_spanish.txt',
            r'root\tf\maps\ctf_well_swedish.txt',
            r'root\tf\maps\ctf_well_tchinese.txt',
            r'root\tf\maps\default_arena.txt',
            r'root\tf\maps\default_cp.txt',
            r'root\tf\maps\default_ctf.txt',
            r'root\tf\maps\default_koth.txt',
            r'root\tf\maps\default_payload.txt',
            r'root\tf\maps\default_payload_race.txt',
            r'root\tf\maps\koth_viaduct_english.txt',
            r'root\tf\maps\koth_viaduct_event_english.txt',
            r'root\tf\maps\pl_badwater_danish.txt',
            r'root\tf\maps\pl_badwater_dutch.txt',
            r'root\tf\maps\pl_badwater_english.txt',
            r'root\tf\maps\pl_badwater_finnish.txt',
            r'root\tf\maps\pl_badwater_french.txt',
            r'root\tf\maps\pl_badwater_german.txt',
            r'root\tf\maps\pl_badwater_italian.txt',
            r'root\tf\maps\pl_badwater_japanese.txt',
            r'root\tf\maps\pl_badwater_korean.txt',
            r'root\tf\maps\pl_badwater_norwegian.txt',
            r'root\tf\maps\pl_badwater_polish.txt',
            r'root\tf\maps\pl_badwater_portuguese.txt',
            r'root\tf\maps\pl_badwater_russian.txt',
            r'root\tf\maps\pl_badwater_schinese.txt',
            r'root\tf\maps\pl_badwater_spanish.txt',
            r'root\tf\maps\pl_badwater_swedish.txt',
            r'root\tf\maps\pl_badwater_tchinese.txt',
            r'root\tf\maps\pl_barnblitz_danish.txt',
            r'root\tf\maps\pl_barnblitz_dutch.txt',
            r'root\tf\maps\pl_barnblitz_english.txt',
            r'root\tf\maps\pl_barnblitz_finnish.txt',
            r'root\tf\maps\pl_barnblitz_french.txt',
            r'root\tf\maps\pl_barnblitz_german.txt',
            r'root\tf\maps\pl_barnblitz_italian.txt',
            r'root\tf\maps\pl_barnblitz_japanese.txt',
            r'root\tf\maps\pl_barnblitz_korean.txt',
            r'root\tf\maps\pl_barnblitz_norwegian.txt',
            r'root\tf\maps\pl_barnblitz_polish.txt',
            r'root\tf\maps\pl_barnblitz_portuguese.txt',
            r'root\tf\maps\pl_barnblitz_russian.txt',
            r'root\tf\maps\pl_barnblitz_schinese.txt',
            r'root\tf\maps\pl_barnblitz_spanish.txt',
            r'root\tf\maps\pl_barnblitz_swedish.txt',
            r'root\tf\maps\pl_barnblitz_tchinese.txt',
            r'root\tf\maps\pl_frontier_final_danish.txt',
            r'root\tf\maps\pl_frontier_final_dutch.txt',
            r'root\tf\maps\pl_frontier_final_english.txt',
            r'root\tf\maps\pl_frontier_final_finnish.txt',
            r'root\tf\maps\pl_frontier_final_french.txt',
            r'root\tf\maps\pl_frontier_final_german.txt',
            r'root\tf\maps\pl_frontier_final_italian.txt',
            r'root\tf\maps\pl_frontier_final_japanese.txt',
            r'root\tf\maps\pl_frontier_final_korean.txt',
            r'root\tf\maps\pl_frontier_final_norwegian.txt',
            r'root\tf\maps\pl_frontier_final_polish.txt',
            r'root\tf\maps\pl_frontier_final_portuguese.txt',
            r'root\tf\maps\pl_frontier_final_russian.txt',
            r'root\tf\maps\pl_frontier_final_schinese.txt',
            r'root\tf\maps\pl_frontier_final_spanish.txt',
            r'root\tf\maps\pl_frontier_final_swedish.txt',
            r'root\tf\maps\pl_frontier_final_tchinese.txt',
            r'root\tf\maps\pl_goldrush_danish.txt',
            r'root\tf\maps\pl_goldrush_dutch.txt',
            r'root\tf\maps\pl_goldrush_english.txt',
            r'root\tf\maps\pl_goldrush_finnish.txt',
            r'root\tf\maps\pl_goldrush_french.txt',
            r'root\tf\maps\pl_goldrush_german.txt',
            r'root\tf\maps\pl_goldrush_italian.txt',
            r'root\tf\maps\pl_goldrush_japanese.txt',
            r'root\tf\maps\pl_goldrush_korean.txt',
            r'root\tf\maps\pl_goldrush_norwegian.txt',
            r'root\tf\maps\pl_goldrush_polish.txt',
            r'root\tf\maps\pl_goldrush_portuguese.txt',
            r'root\tf\maps\pl_goldrush_russian.txt',
            r'root\tf\maps\pl_goldrush_schinese.txt',
            r'root\tf\maps\pl_goldrush_spanish.txt',
            r'root\tf\maps\pl_goldrush_swedish.txt',
            r'root\tf\maps\pl_goldrush_tchinese.txt',
            r'root\tf\maps\pl_hoodoo_final.txt',
            r'root\tf\maps\pl_thundermountain_danish.txt',
            r'root\tf\maps\pl_thundermountain_dutch.txt',
            r'root\tf\maps\pl_thundermountain_english.txt',
            r'root\tf\maps\pl_thundermountain_finnish.txt',
            r'root\tf\maps\pl_thundermountain_french.txt',
            r'root\tf\maps\pl_thundermountain_german.txt',
            r'root\tf\maps\pl_thundermountain_italian.txt',
            r'root\tf\maps\pl_thundermountain_japanese.txt',
            r'root\tf\maps\pl_thundermountain_korean.txt',
            r'root\tf\maps\pl_thundermountain_norwegian.txt',
            r'root\tf\maps\pl_thundermountain_polish.txt',
            r'root\tf\maps\pl_thundermountain_portuguese.txt',
            r'root\tf\maps\pl_thundermountain_russian.txt',
            r'root\tf\maps\pl_thundermountain_schinese.txt',
            r'root\tf\maps\pl_thundermountain_spanish.txt',
            r'root\tf\maps\pl_thundermountain_swedish.txt',
            r'root\tf\maps\pl_thundermountain_tchinese.txt',
            r'root\tf\maps\pl_upward_danish.txt',
            r'root\tf\maps\pl_upward_dutch.txt',
            r'root\tf\maps\pl_upward_english.txt',
            r'root\tf\maps\pl_upward_finnish.txt',
            r'root\tf\maps\pl_upward_french.txt',
            r'root\tf\maps\pl_upward_german.txt',
            r'root\tf\maps\pl_upward_italian.txt',
            r'root\tf\maps\pl_upward_japanese.txt',
            r'root\tf\maps\pl_upward_korean.txt',
            r'root\tf\maps\pl_upward_norwegian.txt',
            r'root\tf\maps\pl_upward_polish.txt',
            r'root\tf\maps\pl_upward_portuguese.txt',
            r'root\tf\maps\pl_upward_russian.txt',
            r'root\tf\maps\pl_upward_schinese.txt',
            r'root\tf\maps\pl_upward_spanish.txt',
            r'root\tf\maps\pl_upward_swedish.txt',
            r'root\tf\maps\pl_upward_tchinese.txt',
            r'root\tf\maps\plr_hightower_danish.txt',
            r'root\tf\maps\plr_hightower_dutch.txt',
            r'root\tf\maps\plr_hightower_english.txt',
            r'root\tf\maps\plr_hightower_finnish.txt',
            r'root\tf\maps\plr_hightower_french.txt',
            r'root\tf\maps\plr_hightower_german.txt',
            r'root\tf\maps\plr_hightower_italian.txt',
            r'root\tf\maps\plr_hightower_japanese.txt',
            r'root\tf\maps\plr_hightower_korean.txt',
            r'root\tf\maps\plr_hightower_norwegian.txt',
            r'root\tf\maps\plr_hightower_polish.txt',
            r'root\tf\maps\plr_hightower_portuguese.txt',
            r'root\tf\maps\plr_hightower_russian.txt',
            r'root\tf\maps\plr_hightower_schinese.txt',
            r'root\tf\maps\plr_hightower_spanish.txt',
            r'root\tf\maps\plr_hightower_swedish.txt',
            r'root\tf\maps\plr_hightower_tchinese.txt',
            r'root\tf\maps\plr_nightfall_final_danish.txt',
            r'root\tf\maps\plr_nightfall_final_dutch.txt',
            r'root\tf\maps\plr_nightfall_final_english.txt',
            r'root\tf\maps\plr_nightfall_final_finnish.txt',
            r'root\tf\maps\plr_nightfall_final_french.txt',
            r'root\tf\maps\plr_nightfall_final_german.txt',
            r'root\tf\maps\plr_nightfall_final_italian.txt',
            r'root\tf\maps\plr_nightfall_final_japanese.txt',
            r'root\tf\maps\plr_nightfall_final_korean.txt',
            r'root\tf\maps\plr_nightfall_final_norwegian.txt',
            r'root\tf\maps\plr_nightfall_final_polish.txt',
            r'root\tf\maps\plr_nightfall_final_portuguese.txt',
            r'root\tf\maps\plr_nightfall_final_russian.txt',
            r'root\tf\maps\plr_nightfall_final_schinese.txt',
            r'root\tf\maps\plr_nightfall_final_spanish.txt',
            r'root\tf\maps\plr_nightfall_final_swedish.txt',
            r'root\tf\maps\plr_nightfall_final_tchinese.txt',
            r'root\tf\maps\plr_pipeline_danish.txt',
            r'root\tf\maps\plr_pipeline_dutch.txt',
            r'root\tf\maps\plr_pipeline_english.txt',
            r'root\tf\maps\plr_pipeline_finnish.txt',
            r'root\tf\maps\plr_pipeline_french.txt',
            r'root\tf\maps\plr_pipeline_german.txt',
            r'root\tf\maps\plr_pipeline_italian.txt',
            r'root\tf\maps\plr_pipeline_japanese.txt',
            r'root\tf\maps\plr_pipeline_korean.txt',
            r'root\tf\maps\plr_pipeline_norwegian.txt',
            r'root\tf\maps\plr_pipeline_polish.txt',
            r'root\tf\maps\plr_pipeline_portuguese.txt',
            r'root\tf\maps\plr_pipeline_russian.txt',
            r'root\tf\maps\plr_pipeline_schinese.txt',
            r'root\tf\maps\plr_pipeline_spanish.txt',
            r'root\tf\maps\plr_pipeline_swedish.txt',
            r'root\tf\maps\plr_pipeline_tchinese.txt',
            r'root\tf\maps\tc_hydro_commentary.txt',
            r'root\tf\maps\tc_hydro_danish.txt',
            r'root\tf\maps\tc_hydro_dutch.txt',
            r'root\tf\maps\tc_hydro_english.txt',
            r'root\tf\maps\tc_hydro_finnish.txt',
            r'root\tf\maps\tc_hydro_french.txt',
            r'root\tf\maps\tc_hydro_german.txt',
            r'root\tf\maps\tc_hydro_italian.txt',
            r'root\tf\maps\tc_hydro_japanese.txt',
            r'root\tf\maps\tc_hydro_korean.txt',
            r'root\tf\maps\tc_hydro_norwegian.txt',
            r'root\tf\maps\tc_hydro_polish.txt',
            r'root\tf\maps\tc_hydro_portuguese.txt',
            r'root\tf\maps\tc_hydro_russian.txt',
            r'root\tf\maps\tc_hydro_schinese.txt',
            r'root\tf\maps\tc_hydro_spanish.txt',
            r'root\tf\maps\tc_hydro_swedish.txt',
            r'root\tf\maps\tc_hydro_tchinese.txt',

            r'root\tf\steam.inf'
            ]

        self.config['recodelist'] = [
            r'root\tf\maps',
            r'root\tf\resource'
        ]

        self.config['uploadlist'] = [
            'tf_brazilian.txt',
            'tf_danish.txt',
            'tf_dutch.txt',
            'tf_english.txt',
            'tf_finnish.txt',
            'tf_french.txt',
            'tf_german.txt',
            'tf_hungarian.txt',
            'tf_italian.txt',
            'tf_japanese.txt',
            'tf_korean.txt',
            'tf_norwegian.txt',
            'tf_polish.txt',
            'tf_portuguese.txt',
            'tf_romanian.txt',
            'tf_russian.txt',
            'tf_schinese.txt',
            'tf_spanish.txt',
            'tf_swedish.txt',
            'tf_tchinese.txt',
            'tf_turkish.txt'
            ]
        self.config['uploadpath'] = r'X:\Sebi\Desktop\tf2-extract\tf2\team fortress 2 content.gcf\root\tf\resource\UTF-8'

        self.config['difflist'] = self.config['uploadlist']
        self.config['diffile'] = r'X:\Sebi\Desktop\testpy\tf2-extract\raw.diff'
        # self.config['patch'] =

        self.template = ur"""<!-- This page is updated by a bot. Changes made to it will likely be lost the next time it edits. -->
== Recent changes ==
{{tf diff|p=%s}}
== File info ==
'''Note''': this encoding of this file has been changed from UCS-2 Little Endian (UTF-16) to UTF-8 (without BOM) to reduce filesize. The content of the file still matches the original version from {{code|root\tf\resource}}.
== Licensing ==
{{Externally linked}}
{{ExtractTF2}}
[[Category:Text files]]"""


    def extract(self):
        HL = hlextract.HLExtract(volatile=True)
        print 'Extracting...'
        HL.extract(self.config['packagedir'], self.config['outdir'], self.config['extractlist'], multidir=True)


    def recode(self):
        """Duplicates files, and recode them to utf-8."""
        for group in self.config['recodelist']:
            txt = []
            fdir = os.path.join(self.config['outdir'], self.config['package'], group)
            for line in os.listdir(fdir):
                if re.search(r'\.txt', line):
                    txt.append(line)
            for f in txt:
                utf = os.path.join(fdir, 'UTF-8')
                if not os.path.exists(utf):
                    os.mkdir(utf)
                src = os.path.join(fdir, f)
                dst = os.path.join(fdir, 'UTF-8', f)
                if os.path.isfile(dst):
                    os.remove(dst)
                shutil.copy2(src, dst)
                print f, 'Reading...'
                try:
                    utf_f = open(dst, 'rb').read(-1).decode('utf16').encode('utf8')
                    print f, 'Writing...'
                    utf_fn = open(dst, 'wb').write(utf_f)
                except UnicodeDecodeError:
                    print 'UnicodeDecodeError', f, 'failed. Skipped.'
                    continue


    def __upload__(self, f, name, summary):
        uploader = wikiUpload.wikiUploader(wconfig['usr'], wconfig['pwd'], wconfig['url'])
        try:
            print 'upload():', f, 'uploading to', name, '...'
            uploader.upload(f, name, summary, overwrite=True, reupload=True)
            print 'Attempted upload of %s | %s\n' % (f, name)
        except:
            print 'upload():', f, 'to', name, 'failed.'
            print 'error:upload() %s | %s\n' % (f, name)


    def upload(self):
        # f.upload(self.config['uploadlist'], self.config['uploadpath'], 'Updated patch for [[%s]]' % self.config['patch'])
        for f in self.config['uploadlist']:
            filepath = os.path.join(self.config['uploadpath'], f)
            print filepath, 'to:', f.capitalize(), 'summ:', 'HI!'
            self.__upload__(filepath, f.capitalize(), '[[%s]] (UTF-8)' % self.config['patch'])
            print 'Uploaded:', filepath


    def format(self):
        gre = Re()
        r_add = re.compile(r'^\+[^\+](.+)', re.MULTILINE)
        r_rem = re.compile(r'^\-[^\-](.+)', re.MULTILINE)
        r_head = re.compile(r'^@@(.+)', re.MULTILINE)
        r_con = re.compile(r'^\s[^\}](.+)', re.MULTILINE)
        r_diff = re.compile(r'^diff --git (a\/.*)\s(b\/.*)', re.MULTILINE)

        f = open(self.config['diffile'], 'r')
        output = []
        print 'Parsing %s and formatting...' % self.config['diffile']
        for line in f.readlines():
            if gre.match(r_add, line):
                output.append(u'{{tf diff|+|2=%s}}' % u(gre.match(r_add, line).groups(0)[0]))
            elif gre.match(r_rem, line):
                output.append(u'{{tf diff|-|2=%s}}' % u(gre.match(r_rem, line).groups(0)[0]))
            elif gre.match(r_head, line):
                output.append(u'{{tf diff|@|2=%s}}' % u(gre.match(r_head, line).groups(0)[0]))
            elif gre.match(r_con, line):
                output.append(u'{{tf diff|c|2=%s}}' % u(gre.match(r_con, line).groups(0)[0]))
            elif gre.match(r_diff, line):
                p = gre.match(r_diff, line).groups(1)[0]
                output.append('#' + os.path.split(p)[-1])
            elif line.startswith('index'):
                pass
            elif line.startswith('+++') or line.startswith('---'):
                pass
            elif line.startswith(' }'):
                pass
            elif line.startswith('Binary files'):
                pass
            else:
                output.append(line)

        self.formatted = [ x.strip() for x in output if x ] # Blank line and whitespace stripping.
        print 'Done.'


    def edit(self):
        print 'Logging in.'
        wiki = wikitools.Wiki(wconfig['url-api'])
        wiki.login(wconfig['usr'], wconfig['pwd'])
        print 'Logged in.'
        print 'Beginning edit iterator. Today I\'ll be editing:', self.config['difflist']
        for f in self.config['difflist']:
            text = self.template % (self.config['patch'])
            print f, '> editing...'
            page = wikitools.Page(wiki, 'File:' + f.capitalize())
            page.edit(text, summary='Updated diff for [[%s]].' % self.config['patch'], bot=1, skipmd5=True)
            print f, '> done.'


    def run(self, patch, extract=False, upload=False, diffs=False):
        self.config['patch'] = patch
        if extract is True:
            self.extract()
            self.recode()
        if upload is True:
            self.upload()
        if diffs is True:
            self.edit()
        if extract is False and upload is False and diffs is False:
            # Oh god ^
            print 'I do nothing?'
            return self.config

    def run2(self):
        HL = hlextract.HLExtract(volatile=True)
        print 'Extracting...'
        HL.extract(self.config['packagedir'], self.config['outdir'], self.config['extractlist'], multidir=True)


tf = tf2extract()
tf.run('December 2, 2011 Patch', extract=True, upload=False, diffs=False)