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
        self.styledicts = {}
        self.names = []
        # check if .maper exists
        maper_metadata_path = osp.join(osp.expanduser('~'), '.maper')
        if not osp.exists(maper_metadata_path):
            os.mkdir(maper_metadata_path)

    def i(self, filename, name=None, proj=True, simplify=False, xl=False,
          filter=None):
        """docstring."""
        if name is None:
            name = osp.splitext(filename)[0].split('/')[-1]
        if proj:
            if not osp.isfile(osp.splitext(filename)[0] + '_temp.shp'):
                if xl:
                    cmd = 'mapshaper-xl'
                else:
                    cmd = self.command
                cmd += ' -i {0}'.format(filename)
                if filter is not None:
                    cmd += ' -filter \'%s\'' % filter
                cmd += ' -proj wgs84 -drop target=* fields=*'
                if simplify:
                    cmd += ' -simplify dp stats resolution=720x680'
                cmd += ' -o {0}_temp.shp'.format(osp.splitext(filename)[0])
                print cmd
                self.cmd(cmd)
            self.inputs['-i'].append(osp.splitext(filename)[0] + '_temp.shp')
        else:
            self.inputs['-i'].append(osp.splitext(filename)[0] + '.shp' + suffix)
        self.names.extend([name])

        return self

    def convert_and_clip(self, filename):
        """docstring."""
        pass

    def info(self):
        """docstring."""
        return self

    def style(self, name=None, **kwargs):
        if name is None:
            self.styledict = kwargs
        else:
            self.styledicts[name] = kwargs
        return self

    def simplify(self, perc, method='dp'):
        """docstring."""
        self.arglist.update({'-simplify': 'dp stats resolution=720x680'})
        return self

    def clip(self):
        cmd = self.command
        cmd += ' -rectangle name=box bbox=-127,43,-115,51'
        cmd += ' -proj +proj=merc +lat_ts=46.289428 +lon_0=-119.291794'
        cmd += ' -o box_temp.shp'
        print cmd
        self.cmd(cmd)

    def export(self):
        """export."""
        output = {'-o': 'target=* format=svg width=720 {0}.svg'.format(self.filename)}
        arg = self.command
        for key, val in self.inputs.items():
            arg += ' {0} combine-files'.format(key)
            for item in val:
                arg += ' {1}'.format(key, item)
        arg += ' -rename-layers {0}'.format(self.names[0])
        for name in self.names[1:]:
            arg += ',{0}'.format(name)
        arg += ' -proj +proj=merc +lat_ts=46.289428 +lon_0=-119.291794'
        arg += ' -clip box_temp.shp'

        #arg += ' -o target=* %s.topojson' % self.filename
        #print arg
        #self.cmd(arg)
        #arg = self.command + ' -i %s.topojson' % self.filename
        try:
            arg += ' -svg-style'
            for key, val in self.styledict.items():
                arg += ' {0}={1}'.format(key, val)
        except AttributeError:
            pass
        #arg += ' -drop target=* fields=*'
        for name, _dict in self.styledicts.items():
            arg += ' -svg-style target=%s' % name
            for key, val in _dict.items():
                arg += ' {0}={1}'.format(key, val)
        #arg += ' -merge-layers'
        for key, val in self.arglist.items():
            arg += ' {0} {1}'.format(key, val)
        for key, val in output.items():
            arg += ' {0} {1}'.format(key, val)
        print arg
        self.cmd(arg)
        #arg = 'mapshaper output.topojson -info'
        #print arg
        #self.cmd(arg)
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
