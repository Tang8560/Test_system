# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : TE_result.py
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

from pubsub import pub

class TE_result(object):
    def __init__(self,thread_event):
        pub.sendMessage("get_result")