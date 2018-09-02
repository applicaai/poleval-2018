#!/usr/bin/env python

"""
Separate models are being trained per (almost) non-overlaping entity groups,
that is groups guaranteeing it is at least highly unlikely entities within
will collide. Whenever possible, groups consisted of neighboring entities
in order to exploit the potential of linear CRF chain.
"""

GROUPS = (['persName'],
          ['time', 'date', 'placeName_settlement'],
          ['orgName'],
          ['geogName', 'placeName'],
          ['placeName_bloc', 'placeName_region', 'placeName_country', 'placeName_district'],
          ['persName_addName', 'persName_forename', 'persName_surname'])
