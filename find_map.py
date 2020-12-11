from diqu_map import *


def find_diqu(diqu):
    for diqu_sum in V5Front_ResGCountry:
        if int(diqu_sum['key']) == int(diqu):
            return diqu_sum['_name']


def find_zt(zt):
    for zhuangtai in V5Front_ResGPSSummary:
        if int(zhuangtai['key']) == int(zt):
            return zhuangtai['_name']

