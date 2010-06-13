"""
Yum plugin for Amazon S3 access.

This plugin provides access to a protected Amazon S3 bucket using Amazon's special
REST authentication scheme.
"""

import os
import sys
import urllib

from yum.plugins import TYPE_CORE
from yum.yumRepo import YumRepository

import yum.Errors

from urlgrabber.grabber import URLGrabber
from urlgrabber.grabber import URLGrabError

__revision__ = "1.0.0"

requires_api_version = '2.5'
plugin_type = TYPE_CORE

def config_hook(conduit):
    config.RepoConf.s3_enabled = config.BoolOption(False)

def init_hook(conduit):
    """ 
    Plugin initialization hook. Setup the S3 repositories.
    """
   
    repos = conduit.getRepos()
    for i in repos.repos.keys():
        rs = repos.repos[i]
        if isinstance(repo, YumRepository) and repo.s3_enabled:
            new_repo = AmazonS3Repo(idx)
            new_repo.baseurl = repo.baseurl
            new_repo.mirrorlist = repo.mirrorlist
            new_repo.basecachedir = repo.basecachedir
            new_repo.gpgcheck = repo.gpgcheck
            new_repo.proxy = repo.proxy
            new_repo.enablegroups = repo.enablegroups
                                                                        
            del rs.repos[repo.id]
            rs.add(new_repo)

class AmazonS3Grabber:
    def __init__(self, grabber, awsAccessKey, awsSecretKey, **kwargs):
        print 'init s3'
        self.grabber = grabber
        self.awsAccessKey = awsAccessKey
        self.awsSecretKey = awsSecretKey

    def urlgrab(self, url, filename=None, **kwargs):
        print 'urlgrab s3'
        return self.grabber.urlgrab(url, filename, kwargs)
    
    def urlopen(self, url, **kwargs):
        print 'urlopen s3'
        return self.grabber.urlopen(url, kwargs)

    def urlread(self, url, limit=None, **kwargs):
        print 'urlread s3'
        return self.grabber.urlread(url, limit, kwargs)


class AmazonS3Repo(YumRepository):
    """
    Repository object for Amazon S3.
    """
    
    def __init__(self, repoid):
        YumRepository.__init__(self, repoid)
        self.enable()

    def _setupGrab(self):
        YumRepository.setupGrab(self)
        self.grab = AmazonS3Grabber(self.grab, 'my-access-key', 'my-secret-key')

    setupGrab = _setupGrab
