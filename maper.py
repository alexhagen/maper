"""Maper - a simple ``Python`` wrapper for ``mapshaper``."""
import os.path as osp
import subprocess
import shutil
import os
from pyg import twod as pyg
from collections import defaultdict

class maper(object):
    """docstring"""

    def __init__(self, filename='out'):
        """docstring."""
        self.filename = filename
        self.command = 'mapshaper'
        self.arglist = defaultdict()
        self.inputs = defaultdict()
        self.inputs['-i'] = []
        # check if .maper exists
        maper_metadata_path = osp.join(osp.expanduser('~'), '.maper')
        if not osp.exists(maper_metadata_path):
            os.mkdir(maper_metadata_path)

    def i(self, filename, name=None, proj=False):
        """docstring."""

        if proj:
            cmd = self.command
            cmd += ' -i {0}'.format(filename)
            cmd += ' -proj wgs84'
            cmd += ' -o {0}_temp.shp'.format(osp.splitext(filename)[0])
            print cmd
            self.cmd(cmd)
            self.inputs['-i'].append(osp.splitext(filename)[0] + '_temp.shp')
        else:
            self.inputs['-i'].append(osp.splitext(filename)[0] + '.shp')
        return self

    def convert_and_clip(self, filename):
        """docstring."""
        pass

    def info(self):
        """docstring."""
        return self

    def style(self, **kwargs):
        self.styledict = kwargs
        return self

    def simplify(self, perc, method='dp'):
        """docstring."""
        self.arglist.update({'-simplify': 'dp stats resolution=720x680'})
        return self

    def clip(self):
        cmd = self.command
        cmd += ' -rectangle name=box bbox=-130,35,-110,55'
        cmd += ' -proj +proj=merc +lat_ts=46.289428 +lon_0=-119.291794'
        cmd += ' -o box_temp.shp'
        print cmd
        self.cmd(cmd)

    def export(self):
        """export."""
        output = {'-o': 'format=svg width=720 {0}.svg'.format(self.filename)}
        arg = self.command
        for key, val in self.inputs.items():
            arg += ' {0} combine-files'.format(key)
            for item in val:
                arg += ' {1}'.format(key, item)
        arg += ' -svg-style'
        for key, val in self.styledict.items():
            arg += ' {0}={1}'.format(key, val)
        arg += ' -proj +proj=merc +lat_ts=46.289428 +lon_0=-119.291794'
        arg += ' -clip box_temp.shp'
        for key, val in self.arglist.items():
            arg += ' {0} {1}'.format(key, val)
        for key, val in output.items():
            arg += ' {0} {1}'.format(key, val)
        print arg
        self.cmd(arg)
        return self

    def show(self):
        """docstring."""
        pyg.svg_show('{0}.svg'.format(self.filename), caption='map', label='', width='4')
        return self

    @staticmethod
    def cmd(command, blocking=True, **kwargs):
        _cmd = "{command}".format(command=command)
        p = subprocess.Popen([_cmd], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True,
                             env=dict(PATH='${PATH}:/usr/local/bin'))
        if blocking:
            (out, err) = p.communicate()
            if len(err) > 0:
                print err
            return out
