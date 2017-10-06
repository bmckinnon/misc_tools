#!/usr/bin/env python3
#
# Author: Bill McKinnon
# Date:   2017-10-05
#
# Script to take two directories, a src one and a dst one, and to clone timestamps 
# (atime, mtime) from files in the src dir to the dst dir, ignoring file extensions. 
#

import sys
import os
import glob
import time

def get_times(file):
    """
    Return a tuple of (atime, mtime) for the given file.
    """
    stat_info = os.stat(file)
    return (stat_info[7], stat_info[8])

args = sys.argv[1:]

if len(args) != 2:
    sys.exit("Usage: %s <src dir> <dst dir>" % sys.argv[0])

src_dir = args[0]
dst_dir = args[1]

times = {}

# Get src_dir times, based on just basename. If there are multiple files w/the same first portion of the filename,
# the last one wins.
for path in glob.glob("%s/*" % (src_dir,)):
    if not os.path.isfile(path):
        continue
    #basename = os.path.basename(path).split('.')[0] # assuming just one dot (windows)

    basename = os.path.basename(path)
    if '.' in path:
        # Strip off the extension
        basename = '.'.join(basename.split('.')[:-1])
    times[basename] = get_times(path)

# Now look for target files to set timestamps on. If there are multiple, set timestamps on them all.
files_changed = 0
for basename, (atime, mtime) in times.items():
    files = glob.glob("%s/%s.*" % (dst_dir, basename))
    for file in files:
        # NOTE: Having overlapping wildcards (like if you have 1.2.txt and 1.txt it results in
        #       dst_dir/1.* and dst_dir/1.2.* being used) can cause some strange behavior. This
        #       is probably not typical.

        #print("-> Would have set time on %s to %s/%s" % (file, time.ctime(atime), time.ctime(mtime)))
        os.utime(file, (atime, mtime))
        files_changed += 1

print("%d timestamps cloned from %s to %s" % (files_changed, src_dir, dst_dir))
