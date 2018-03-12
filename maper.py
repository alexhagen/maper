"""Maper - a simple ``Python`` wrapper for ``mapshaper``"""
import os
import subprocess

class maper(object):
    """docstring"""
    def __init__(self):
        """docstring"""
        self.command = 'mapshaper'
        self.arglist = {}

    def add_input(self, filename):
        """docstring"""
        input_kwargs = {'-i': filename, 'combine-files': ''}
        self.arglist.update(input_kwargs)
        return self

    def info(self):
        """docstring"""
        return self

    def simplify(self, perc, method='dp'):
        """docstring"""
        return self

    def export(self):
        """export"""
        return self

    def show(self):
        """docstring"""
        return self
