#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrosbag as prb  

with prb.bagplayer("/home/hugo/catkin_ws/src/pkg_log/bag/2017-03-02-09-57-07.bag") as ex:
	ex.play()
