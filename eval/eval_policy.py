#!/usr/bin/env python3

#
# Additional Modification Copyright (c) 2016-2018 North Carolina State University.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions and use are permitted for internal research purposes only, 
# and commercial use is strictly prohibited under this license. Inquiries 
# regarding commercial use should be directed to the Office of Technology 
# Transfer at North Carolina State University, 919‐515‐7199, https://research.
# ncsu.edu/otcnv/contact/, techtransfer@ncsu.edu.
# 
# 2. Commercial use means the sale, lease, export, transfer, conveyance or other 
# distribution to a third party for financial gain, income generation or other 
# commercial purposes of any kind, whether direct or indirect. Commercial use 
# also means providing a service to a third party for financial gain, income 
# generation or other commercial purposes of any kind, whether direct or 
# indirect.
# 
# 3. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 4. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/
# or other materials provided with the distribution.
# 
# 5. The names “North Carolina State University”, “NCSU” and any trade‐name,
# personal name, trademark, trade device, service mark, symbol, image, icon, or 
# any abbreviation, contraction or simulation thereof owned by North Carolina 
# State University must not be used to endorse or promote products derived from 
# this software without prior written permission. For written permission, please
# contact trademarks@ncsu.edu.
# 
# Disclaimer: THIS SOFTWARE IS PROVIDED “AS IS” AND ANY EXPRESSED OR IMPLIED 
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
# EVENT SHALL THE APACHE SOFTWARE FOUNDATION OR ITS CONTRIBUTORS BE LIABLE FOR 
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (
# INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
#


#
# Copyright (c) 2013,  Regents of the Columbia University 
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other 
# materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import configparser
import argparse
import os
import sys
import errno
import logging
import coloroutput
import re
import subprocess
import time
import signal
import threading

## Module init

# setting log format
logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                              "%Y%b%d-%H:%M:%S")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

# get environment variable
try:
    XTERN_ROOT = os.environ["XTERN_ROOT"]
    logging.debug('XTERN_ROOT = ' + XTERN_ROOT)
except KeyError as e:
    logging.error("Please set the environment variable " + str(e))
    sys.exit(1)
    
def getXternDefaultOptions():
    default = {}
    try:
        with open(XTERN_ROOT+'/default.options') as f:
            for line in f:
                line = line.partition('#')[0].rstrip()
                if not line:
                    continue
                s1, s2 = [p.strip() for p in line.split("=")]
                if not s1 or not s2:
                    logging.warning(
                        'cannot get default value from "%s" (ignored)' % line)
                    continue
                default[s1] = s2
    except IOError as e:
        logging.error("There is no 'default.options' file")
        sys.exit(1)
    #logging.debug("default.options : ")
    #for key in default:
    #    logging.debug("\t{0} = '{1}'".format(key,default[key]))
    return default
    
# get default xtern options
default_options = getXternDefaultOptions()
root_dir = os.getcwd()
    
def getConfigFullPath(config_file):
    try:
        with open(config_file) as f: pass
    except IOError as e:
        if config_file == 'xtern.cfg':
            logging.warning("'xtern.cfg' does not exist in current directory"
                    + ", use default one in XTERN_ROOT/eval")
            return os.path.abspath(XTERN_ROOT + "/eval/xtern.cfg")
        else:
            logging.warning("'%s' does not exist" % config_file)
            return None
    return os.path.abspath(config_file)

def readConfigFile(config_file):
    try:
        newConfig = configparser.ConfigParser( {"REPEATS": "100", 
                                                "INPUTS": "",
                                                "REQUIRED_FILES": "",
                                                "DOWNLOAD_FILES": "",
                                                "TARBALL": "",
                                                "GZIP": "",
                                                "EXPORT": "",
                                                "DTHREADS": "",
                                                "DMP_O": "",
                                                "DMP_B": "",
                                                "DMP_PB": "",
                                                "DMP_HB": "",
                                                "INIT_ENV_CMD": "",
                                                "C_WITH_XTERN": "0",
                                                "C_CMD": "",
                                                "C_TERMINATE_SERVER": "0",
                                                "C_STATS": "0",
                                                "EVALUATION": "",
                                                "DBUG": "-1",
                                                "DBUG_PREFIX": "",
                                                "DBUG_INPUT": "",
                                                "DBUG_OUTPUT": "",
                                                "DBUG_CLIENT": "",
                                                "DBUG_CLIENT_INPUTS": "",
                                                "DBUG_ARBITER_PORT": "12345",
                                                "DBUG_EXPLORER_PORT": "12346",
                                                "DBUG_DPOR": "true",
                                                "DBUG_TIMEOUT": "60"},
                                                inline_comment_prefixes=(';',) )
        ret = newConfig.read(config_file)
    except configparser.MissingSectionHeaderError as e:
        logging.error(str(e))
    except configparser.ParsingError as e:
        logging.error(str(e))
    except configparser.Error as e:
        logging.critical("strange error? " + str(e))
    else:
        if ret:
            return newConfig

# TODO: will fail if there is no git information to get
def getCommandOutput(*args, **kwargs):
    pout = subprocess.getoutput(*args, **kwargs)
    return pout
    
def getGitInfo():
    git_show = 'cd '+XTERN_ROOT+' && git show '
    githash = getCommandOutput(git_show+'| head -1 | sed -e "s/commit //"')
    git_diff = 'cd '+XTERN_ROOT+' && git diff --quiet'
    diff = getCommandOutput('cd ' +XTERN_ROOT+ ' && git diff')
    if diff:
        gitstatus = '_dirty'
    else:
        gitstatus = ''
    commit_date = getCommandOutput( git_show+
            '| head -4 | grep "Date:" | sed -e "s/Date:[ \t]*//"' )
    date_tz  = re.compile(r'^.* ([+-]\d\d\d\d)$').match(commit_date).group(1)
    date_fmt = ('%%a %%b %%d %%H:%%M:%%S %%Y %s') % date_tz
    import datetime
    gitcommitdate = str(datetime.datetime.strptime(commit_date, date_fmt))
    logging.debug( "git 6 digits hash code: " + githash[0:6] )
    logging.debug( "git reposotory status: " + gitstatus)
    logging.debug( "git commit date: " + gitcommitdate)
    return [githash[0:6], gitstatus, gitcommitdate, diff]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # for newer python version; can specify flags
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            logging.warning("%s already exists" % path)
            pass
        else: raise

def genRunDir(config_file):
    if args.model_checking:
        dir_name = "M"
    else:
        dir_name = ""
    from os.path import basename
    config_name = os.path.splitext( basename(config_file) )[0]
    from time import strftime
    dir_name += config_name + strftime("%Y%b%d_%H%M%S")
    mkdir_p(dir_name)
    logging.debug("creating %s" % dir_name)
    return os.path.abspath(dir_name)

def extract_apps_exec(bench, apps_dir=""):
    bench = bench.partition('"')[0].partition("'")[0]
    apps = bench.split()
    if apps.__len__() < 1:
        raise Exception("cannot parse executible file name")
    elif apps.__len__() == 1:
        return apps[0], os.path.abspath(apps_dir + '/' + apps[0] + '/' + apps[0])
    else:
        return apps[0], os.path.abspath(apps_dir + '/' + apps[0] + '/' + apps[1])


def generate_local_options(config, bench, run_config="hinted"):
    """ run_config options: 
        hinted(default), no-hint, csf, nextn, scwf, hpq, buc,
        scwf+nextn, csf+nextn, csf+scwf+nextn, csf+scwf+nextn+hpq, csf+scwf+nextn+hpq+buc
        
    """
    config_options = config.options(bench)

    out_config = {}
    
    for option in default_options:
        if option in config_options:
            out_config[option] = config.get(bench, option)
            logging.debug(option + ' = ' + config.get(bench, option))
        else:
            out_config[option] = default_options[option]
    
    if run_config == "hinted":
        # do nothing, use everything we read from file.
        pass
    else:
        # set to no-hint as base
        out_config["disable_soba"] = 1
        out_config["enforce_non_det_annotations"] = 0

        if run_config == "no-hint":
            pass
        elif run_config == "no-pcs-hint":
            out_config["disable_soba"] = 0
        elif run_config == "csf":
            out_config["scheduling_policy"] = 1
        elif run_config == "nextn":
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "scwf":
            out_config["scheduling_policy"] = 2
        elif run_config == "hpq":
            out_config["scheduling_policy"] = 4
        elif run_config == "buc":
            out_config["enforce_dummy_sync"] = 1
        elif run_config == "hpq+nextn":
            out_config["scheduling_policy"] = 4
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "hpq+nextn+csf":
            out_config["scheduling_policy"] = 5
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "csf+nextn":
            out_config["scheduling_policy"] = 1
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "scwf+nextn":
            out_config["scheduling_policy"] = 2
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "csf+scwf+nextn":
            out_config["scheduling_policy"] = 3
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "csf+scwf+nextn+hpq" or run_config == "hpq+nextn+csf+scwf":
            out_config["scheduling_policy"] = 7
            out_config["enforce_next_n_annotations"] = 1
        elif run_config == "csf+scwf+nextn+hpq+buc" or run_config == "hpq+nextn+csf+scwf+buc" or run_config == "all-policies":
            out_config["scheduling_policy"] = 7
            out_config["enforce_next_n_annotations"] = 1
            out_config["enforce_dummy_sync"] = 1
        elif run_config == "csf+scwf+nextn+buc":
            out_config["scheduling_policy"] = 3
            out_config["enforce_next_n_annotations"] = 1
            out_config["enforce_dummy_sync"] = 1
        else:
            raise ValueError("Unsupported run config: %s"%run_config)

    with open("local.options", "w") as option_file:
        for key, value in out_config.items():
            option_file.write(key + ' = ' + str(value) + '\n')

    # save this configuration for verification purpose
    copy_file("local.options", run_config+".options")

def checkExist(file, flags=os.X_OK):
    if not os.path.exists(file) or not os.path.isfile(file) or not os.access(file, flags):
        return False
    return True

def copy_file(src, dst):
    import shutil
    shutil.copy(src, dst)

# ref: twisted-12.3.0 procutils.py
def which(name, flags=os.X_OK):
    result = []
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
    return result

def write_stats(bench, xtern, nondet, repeats):
    try:
        import numpy
    except ImportError:
        logging.error("please install 'numpy' module")
        sys.exit(1)

    import math

    valid_times = [t for t in nondet if t > 0]
    nondet_avg = numpy.average(valid_times)
    nondet_std = numpy.std(valid_times)
    nondet_sem = nondet_std/math.sqrt(len(valid_times)) if len(valid_times) > 0 else -1
   
    #overhead_std = math.fabs(overhead_avg)*(math.sqrt(((nondet_std/nondet_avg)**2) + (xtern_std/xtern_avg)**2))
    with open("stats.txt", "w") as stats:
        stats.write('bench, config, avg_time, sem, overhead, all times...\n')
        stats.write('{0}, non-det, {1}, {2}, 0%, '.format(bench, nondet_avg, nondet_sem))
        stats.write(', '.join('{}'.format(i) for i in nondet))
        stats.write('\n')

        for run_config, times in xtern.items():
            valid_times = [t for t in times if t > 0]
            xtern_avg = numpy.average(valid_times)
            xtern_std = numpy.std(valid_times)
            overhead_avg = xtern_avg/nondet_avg - 1.0
            xtern_sem = xtern_std/math.sqrt(len(valid_times)) if len(valid_times) > 0 else -1
            stats.write('{0}, {1}, {2}, {3}, {4:.3f}%, '.format(bench, run_config, xtern_avg, xtern_sem, overhead_avg*100))
            stats.write(', '.join('{}'.format(i) for i in times))
            stats.write('\n')

def write_other_stats(nondet, repeats, name):
    cost=[]
    for i in range(int(repeats)):
        log_file_name = '%s/output.%d' % (name, i)
        for line in reversed(open(log_file_name, 'r').readlines()):
            if re.search('^real [0-9]+\.[0-9][0-9][0-9]$', line):
                cost += [float(line.split()[1])]
                break
    try:
        import numpy
    except ImportError:
        logging.error("please install 'numpy' module")
        sys.exit(1)
    avg = numpy.average(cost)
    std = numpy.std(cost)
    nondet_avg = numpy.average(nondet)
    nondet_std = numpy.std(nondet)
    overhead_avg = avg/nondet_avg - 1.0
    import math
    #overhead_std = math.fabs(overhead_avg)*(math.sqrt(((nondet_std/nondet_avg)**2) + (dthread_std/dthread_avg)**2))
    with open("stats.txt", "a") as stats:
        stats.write('{2}-overhead: {1:.3f}%\n\tavg {0}\n'.format(overhead_avg, overhead_avg*100, name))
        stats.write('{2}:\n\tavg {0}\n\tsem {1}\n'.format(avg, std/math.sqrt(repeats), name))


def copy_required_files(app, files):
    for f in files.split():
        logging.debug("copying required file : %s" % f)
        dst = os.path.basename(f)
        if os.path.isabs(f):
            src = f
        else:
            src = os.path.abspath('%s/apps/%s/%s' % (XTERN_ROOT, app, f))
        try:
            copy_file(os.path.realpath(src), dst)
        except IOError as e:
            logging.warning(str(e))
            return False
    return True

def download_files_from_web(links):
    #from urllib import urlretrieve
    import urllib.request
    for link in links.split():
        logging.debug("Downloading file from %s" % link)
        try:
            urllib.request.urlretrieve(link, link.split('/')[-1])
        except IOError as e:
            logging.warning(str(e))
            return False
    return True

def extract_tarball(app, files):
    for f in files.split():
        logging.debug("extracting file : %s" % f)
        if os.path.isabs(f):
            src = f
        else:
            src = os.path.abspath('%s/apps/%s/%s' % (XTERN_ROOT, app, f))
        
        import tarfile
        try:
            tarfile.is_tarfile(src)
            with tarfile.open(src, 'r') as t:
                t.extractall()
        except IOError as e:
            logging.warning(str(e))
            return False
        except tarfile.TarError as e:
            logging.warning(str(e))
            return False
    return True

def extract_gzip(app, files):
    for f in files.split():
        logging.debug("extracting gzip file : %s" % f)
        if os.path.isabs(f):
            src = f
        else:
            src = os.path.abspath('%s/apps/%s/%s' % (XTERN_ROOT, app, f))
        
        import tarfile
        try:
            tarfile.is_tarfile(src)
            with tarfile.open(src, 'r:gz') as t:
                t.extractall()
        except IOError as e:
            logging.warning(str(e))
            return False
        except tarfile.TarError as e:
            logging.warning(str(e))
            return False
    return True

def preSetting(config, bench, apps_name):
    # copy required files
    required_files = config.get(bench, 'required_files')
    if not copy_required_files(apps_name, required_files):
        logging.warning("error in config [%s], skip" % bench)
        return

    # download files if needed
    download_files = config.get(bench, 'download_files')
    if not download_files_from_web(download_files):
        logging.warning("cannot download one of files in config [%s], skip" % bench)
        return

    # extract *.tar files
    tar_balls = config.get(bench, 'tarball')
    if not extract_tarball(apps_name, tar_balls):
        logging.warning("cannot extract files in config [%s], skip" % bench)
        return

    gzips = config.get(bench, 'gzip')
    if not extract_gzip(apps_name, gzips):
        logging.warning("cannot extract files in config [%s], skip" % bench)
        return
    
 
def execBench(cmd, repeats, out_dir,
              client_cmd="", client_terminate_server=False,
              init_env_cmd=""):
    mkdir_p(out_dir)
    for i in range(int(repeats)):
        sys.stderr.write("        PROGRESS: %5d/%d\r" % (i+1, int(repeats))) # progress
        with open('%s/output.%d' % (out_dir, i), 'w', 102400) as log_file:
            if init_env_cmd:
                os.system(init_env_cmd)
            #proc = subprocess.Popen(xtern_command, stdout=sys.stdout, stderr=sys.stdout,
            proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT,
                                    shell=True, executable=bash_path, bufsize = 102400, preexec_fn=os.setsid)
            if client_cmd:
                time.sleep(1)
                with open('%s/client.%d' % (out_dir, i), 'w', 102400) as client_log_file:
                    client_proc = subprocess.Popen(client_cmd, stdout=client_log_file, stderr=subprocess.STDOUT,
                                                   shell=True, executable=bash_path, bufsize = 102400)
                    try:
                        client_proc.wait(timeout=3600)
                    except (KeyboardInterrupt, subprocess.TimeoutExpired) as e: 
                        try:
                            os.killpg(client_proc.pid, signal.SIGTERM)
                            os.killpg(proc.pid, signal.SIGTERM)
                        except:
                            pass
                        raise e
                if client_terminate_server:
                    os.killpg(proc.pid, signal.SIGTERM)
                proc.wait()
                time.sleep(2)
            else:
                try: # TODO should handle whole block
                    proc.wait(timeout=3600)
                except (KeyboardInterrupt, subprocess.TimeoutExpired) as k:
                    try:
                        os.killpg(proc.pid, signal.SIGTERM)
                    except:
                        pass
                    raise k

        # move log files into 'xtern' directory
        try:
            os.renames('out', '%s/out.%d' % (out_dir, i))
        except OSError:
            pass

def processBench(config, bench):
    # slient the output in parallel model-checking
    if args.model_checking and args.parallel > 1:
        logger.setLevel(logging.INFO)

    # for each bench, generate running directory
    logging.debug("processing: " + bench)
    specified_evaluation = config.get(bench, 'EVALUATION')
    apps_name, exec_file = extract_apps_exec(bench, APPS)
    logging.debug("app = %s" % apps_name)
    logging.debug("executible file = %s" % exec_file)
    if not specified_evaluation and not checkExist(exec_file, os.X_OK):
        logging.warning('%s does not exist, skip [%s]' % (exec_file, bench))
        return

    segs = re.sub(r'(\")|(\.)|/|\'', '', bench).split()
    if args.model_checking and not args.check_all:
        dir_name = config.get(bench, 'DBUG') + '_'
    else:
        dir_name = ""
    dir_name +=  '_'.join(segs)
    mkdir_p(dir_name)
    os.chdir(dir_name)

    inputs = config.get(bench, 'inputs')
    repeats = config.get(bench, 'repeats')

    # if specified evaluation script; use it
    if specified_evaluation:
        specified = __import__(specified_evaluation, globals(), locals(), [], 0)
        specified.evaluation(config, int(repeats))
        return

    # get required files
    preSetting(config, bench, apps_name)

    ### dbug ###
    if args.model_checking:
        import dbug
        dbug.model_checking(config, bench, args)
        os.chdir("..")
        return

    # get 'export' environment variable
    export = config.get(bench, 'EXPORT')
    if export:
        logging.debug("export %s", export)

    # git environment presetting command
    init_env_cmd = config.get(bench, 'INIT_ENV_CMD')
    if init_env_cmd:
        logging.info("presetting cmd in each round %s" % init_env_cmd)

    # check if this is a server-client app
    client_cmd = config.get(bench, 'C_CMD')
    client_terminate_server = bool(int(config.get(bench, 'C_TERMINATE_SERVER')))
    client_with_xtern = bool(int(config.get(bench, 'C_WITH_XTERN')))
    use_client_stats = bool(int(config.get(bench, 'C_STATS')))
    if client_cmd:
        if client_with_xtern:
            client_cmd = XTERN_PRELOAD + ' ' + client_cmd
        client_cmd = 'time ' + client_cmd
        logging.info("client command : %s" % client_cmd)
        logging.debug("terminate server after client finish job : " + str(client_terminate_server))
        logging.debug("evaluate performance by using stats of client : " + str(use_client_stats))

    # generate command for xtern [time LD_PRELOAD=... exec args...]
    if client_cmd and client_with_xtern:
        xtern_command = ' '.join(['time', export, exec_file] + inputs.split())
    else:
        xtern_command = ' '.join(['time', XTERN_PRELOAD, export, exec_file] + inputs.split())
    if not args.compare_only:
        logging.info("executing '%s'" % xtern_command)
        # Do other run configurations
        run_configs = config.get(bench, 'RUN_CONFIGS')
        if run_configs:
            run_configs = [ s.strip() for s in run_configs.split(',')]
            for extra_run_config in run_configs:
                generate_local_options(config, bench, extra_run_config)
                logging.info("Executing with xtern-%s"%extra_run_config)
                try:
                    execBench(xtern_command, repeats, 'xtern-'+ extra_run_config, client_cmd, client_terminate_server, init_env_cmd)
                except Exception as e:
                    logging.warn("Exception %s occured. Skipping this configuration."%e) 
                except KeyboardInterrupt:
                    logging.info("Interrupted by user. Skipping this configuration.")
        else:
            logging.warn("No run configuration found! Skipping...")

    client_cmd = config.get(bench, 'C_CMD')
    if client_cmd:
        if client_with_xtern:
            client_cmd = RAND_PRELOAD + ' ' + client_cmd
        client_cmd = 'time ' + client_cmd
    # generate command for non-det [time LD_PRELOAD=... exec args...]
    if client_cmd and client_with_xtern:
        nondet_command = ' '.join(['time', export, exec_file] + inputs.split())
    else:
        nondet_command = ' '.join(['time', RAND_PRELOAD, export, exec_file] + inputs.split())
    logging.info("executing '%s'" % nondet_command)
    if not args.compare_only:
        execBench(nondet_command, repeats, 'non-det', client_cmd, client_terminate_server, init_env_cmd)

    # run additional benchmark for dthreads
    dthread = config.get(bench, 'DTHREADS')
    if dthread:
        if client_cmd:
            logging.error("client-server with dthreads has not yet tested...")
            sys.exit(1)
        dthread_exec_file = os.path.abspath('%s/apps/%s/%s' % (DMTTOOL_ROOT, os.path.basename(exec_file), dthread))
        if checkExist(dthread_exec_file):
            dthread_command = ' '.join(['time', export, dthread_exec_file] + inputs.split())
            logging.info("executing '%s'" % dthread_command)
            execBench(dthread_command, repeats, 'dthreads', "", False, init_env_cmd)
        else:
            logging.warning("cannot find %s" % dthread)
            dthread = ""

    dmp_o = config.get(bench, 'DMP_O')
    if dmp_o:
        dmp_o_exec_file = os.path.abspath('%s/apps/%s/%s-dmp_o' % (DMTTOOL_ROOT, os.path.basename(exec_file), os.path.basename(exec_file)))
        if checkExist(dmp_o_exec_file):
            dmp_o_command = ' '.join(['time', export, 'DMP_SCHEDULING_CHUNK_SIZE=%s' % dmp_o, dmp_o_exec_file] + inputs.split())
            logging.info("executing '%s'" % dmp_o_command)
            execBench(dmp_o_command, repeats, 'dmp_o', "", False, init_env_cmd)
        else:
            logging.warning("cannot find %s-dmp_o" % os.path.basename(exec_file))
            dmp_o = ""

    dmp_b = config.get(bench, 'DMP_B')
    if dmp_b:
        dmp_b_exec_file = os.path.abspath('%s/apps/%s/%s-dmp_b' % (DMTTOOL_ROOT, os.path.basename(exec_file), os.path.basename(exec_file)))
        if checkExist(dmp_b_exec_file):
            dmp_b_command = ' '.join(['time', export, 'DMP_SCHEDULING_CHUNK_SIZE=%s' % dmp_b, dmp_b_exec_file] + inputs.split())
            logging.info("executing '%s'" % dmp_b_command)
            execBench(dmp_b_command, repeats, 'dmp_b', "", False, init_env_cmd)
        else:
            logging.warning("cannot find %s-dmp_b" % os.path.basename(exec_file))
            dmp_b = ""

    dmp_pb = config.get(bench, 'DMP_PB')
    if dmp_pb:
        dmp_pb_exec_file = os.path.abspath('%s/apps/%s/%s-dmp_pb' % (DMTTOOL_ROOT, os.path.basename(exec_file), os.path.basename(exec_file)))
        if checkExist(dmp_pb_exec_file):
            dmp_pb_command = ' '.join(['time', export, 'DMP_SCHEDULING_CHUNK_SIZE=%s' % dmp_pb, dmp_pb_exec_file] + inputs.split())
            logging.info("executing '%s'" % dmp_pb_command)
            execBench(dmp_pb_command, repeats, 'dmp_pb', "", False, init_env_cmd)
        else:
            logging.warning("cannot find %s-dmp_pb" % os.path.basename(exec_file))
            dmp_pb = ""

    dmp_hb = config.get(bench, 'DMP_HB')
    if dmp_hb:
        dmp_hb_exec_file = os.path.abspath('%s/apps/%s/%s-dmp_hb' % (DMTTOOL_ROOT, os.path.basename(exec_file), os.path.basename(exec_file)))
        if checkExist(dmp_hb_exec_file):
            dmp_hb_command = ' '.join(['time', export, 'DMP_SCHEDULING_CHUNK_SIZE=%s' % dmp_hb, dmp_hb_exec_file] + inputs.split())
            logging.info("executing '%s'" % dmp_hb_command)
            execBench(dmp_hb_command, repeats, 'dmp_hb', "", False, init_env_cmd)
        else:
            logging.warning("cannot find %s-dmp_hb" % os.path.basename(exec_file))
            dmp_hb = ""

    # get stats
    xtern_cost = {}
    for run_config in run_configs:
        xtern_cost_this_config = []
        log_file_path = 'xtern-'+run_config
        for i in range(int(repeats)):
            if args.compare_only:
                xtern_cost_this_config += [1.0]
                continue
            if client_cmd and use_client_stats:
                log_file_name = log_file_path + '/client.%d' % i
            else:
                log_file_name = log_file_path + '/output.%d' % i
            try:    
                for line in (open(log_file_name, 'r').readlines() if args.stl_result else reversed(open(log_file_name, 'r').readlines())):
                    if re.search('^real [0-9]+\.[0-9][0-9][0-9]$', line):
                        xtern_cost_this_config += [float(line.split()[1])]
                        break
            except Exception as e:
                logging.warn("Failed to read output file #%d."%i)
                xtern_cost_this_config += [-1]
        xtern_cost['xtern-'+ run_config] = xtern_cost_this_config
                
    nondet_cost = []
    for i in range(int(repeats)):
        if args.compare_only:
            nondet_cost += [1.0]
            continue
        if client_cmd and use_client_stats:
            log_file_name = 'non-det/client.%d' % i
        else:
            log_file_name = 'non-det/output.%d' % i
        try:
            for line in (open(log_file_name, 'r').readlines() if args.stl_result else reversed(open(log_file_name, 'r').readlines())):
                if re.search('^real [0-9]+\.[0-9][0-9][0-9]$', line):
                    nondet_cost += [float(line.split()[1])]
                    break
        except Exception as e:
            logging.warn("Failed to read output file #%d"%i)
            nondet_cost += [-1]

    write_stats(bench, xtern_cost, nondet_cost, int(repeats))
    if dthread:
        write_other_stats(nondet_cost, int(repeats), 'dthreads')
    if dmp_o:
        write_other_stats(nondet_cost, int(repeats), 'dmp_o')
    if dmp_b:
        write_other_stats(nondet_cost, int(repeats), 'dmp_b')
    if dmp_pb:
        write_other_stats(nondet_cost, int(repeats), 'dmp_pb')
    if dmp_hb:
        write_other_stats(nondet_cost, int(repeats), 'dmp_hb')

    # copy exec file
    copy_file(os.path.realpath(exec_file), os.path.basename(exec_file))
    if dthread:
        copy_file(os.path.realpath(dthread_exec_file), os.path.basename(dthread_exec_file))
    if dmp_o:
        copy_file(os.path.realpath(dmp_o_exec_file), os.path.basename(dmp_o_exec_file))
    if dmp_b:
        copy_file(os.path.realpath(dmp_b_exec_file), os.path.basename(dmp_b_exec_file))
    if dmp_pb:
        copy_file(os.path.realpath(dmp_pb_exec_file), os.path.basename(dmp_pb_exec_file))
    if dmp_hb:
        copy_file(os.path.realpath(dmp_hb_exec_file), os.path.basename(dmp_hb_exec_file))

    os.chdir("..")


def workers(semaphore, lock, configs, bench):
    from multiprocessing import Process
    with semaphore:
        p = Process(target=processBench, args=(configs, bench))
        with lock:
            logging.debug("STARTING %s" % bench)
            p.start()
        p.join()
        with lock:
            logging.debug("FINISH %s" % bench)

if __name__ == "__main__":

    APPS = os.path.abspath(XTERN_ROOT + "/apps/")
    try: #TODO: refine this part..
        DMTTOOL_ROOT = os.environ["DMTTOOL_ROOT"]
    except:
        DMTTOOL_ROOT = ""
 
    # parse input arguments
    parser = argparse.ArgumentParser(
        description="Evaluate the perforamnce of xtern")
    parser.add_argument('filename', nargs='*',
        type=str,
        default = ["xtern.cfg"],
        help = "list of configuration files (default: xtern.cfg)")
    parser.add_argument("-mc", "--model-checking",
                        action="store_true", 
                        help="run model-checking tools only")
    parser.add_argument("-p", "--parallel",
                        default=1,
                        type=int,
                        metavar='NUM',
                        help = "number of processes (model checking only)")
    parser.add_argument("--check-all",
                        action="store_true",
                        help="run model-checking on all configs. (By default, only check those with 'DBUG' id in configs)")
    parser.add_argument("--stl-result",
                        action="store_true",
                        help="get stl result of parallel portion only")
    parser.add_argument("--compare-only",
                        action="store_true",
                        help="skip 'xtern' and 'non-det' evaluation")
    parser.add_argument("--generate-xml-only",
                        action="store_true",
                        help="do not run model-checking in model-checking mode")
    parser.add_argument("--dbug-only",
                        action="store_true",
                        help="run only dbug model-checking in model-checking mode")
    parser.add_argument("--smtmc-only",
                        action="store_true",
                        help="run only run dbug+xtern model-checking in model-checking mode")
    args = parser.parse_args()

    if args.filename.__len__() == 0:
        logging.critical('no configuration file specified??')
        sys.exit(1)
    elif args.filename.__len__() == 1:
        logging.debug('config file: ' + ''.join(args.filename))
    else:
        logging.debug('config files: ' + ', '.join(args.filename))

    if args.model_checking:
        if args.parallel < 1:
            logging.error("# of processes is %d", args.parallel)
            sys.exit(1)
        logging.info("# of processes is %d", args.parallel)
    
    # check xtern files
    if not checkExist("%s/dync_hook/interpose.so" % XTERN_ROOT, os.R_OK):
        logging.error('thre is no "$XTERN_ROOT/dync_hook/interpose.so"')
        sys.exit(1)
    if not checkExist("%s/eval/rand-intercept/rand-intercept.so" % XTERN_ROOT, os.R_OK):
        logging.warning('there is no "$XTERN_ROOT/eval/rand-intercept/rand-intercept.so"')
    XTERN_PRELOAD = "LD_PRELOAD=%s/dync_hook/interpose.so" % XTERN_ROOT
    RAND_PRELOAD = "LD_NOTPRELOAD=%s/eval/rand-intercept/rand-intercept.so" % XTERN_ROOT
    # set environment variable
    logging.debug("set timeformat to '\\nreal %E\\nuser %U\\nsys %S'")
    os.environ['TIMEFORMAT'] = "\nreal %E\nuser %U\nsys %S"

    # run command in shell, currently uses 'bash'
    bash_path = which('bash')
    if not bash_path:
        logging.critical("cannot find shell 'bash'")
        sys.exit(1)
    else:
        bash_path = bash_path[0]
        logging.debug("find 'bash' at %s" % bash_path)


    for config_file in args.filename:
        logging.info("processing '" + config_file + "'")
        # get absolute path of config file
        full_path = getConfigFullPath(config_file)

        # config parser  
        local_config = readConfigFile(full_path)
        if not local_config:
            logging.warning("skip " + full_path)
            continue

        # generate running directory
        run_dir = genRunDir(full_path)
        try:
            os.unlink('current')
        except OSError:
            pass
        os.symlink(run_dir, 'current')
        if not run_dir:
            continue
        os.chdir(run_dir)

        benchmarks = local_config.sections()
        all_threads = []
        semaphore = threading.BoundedSemaphore(args.parallel if args.model_checking else 1)
        log_lock = threading.Lock()
        for benchmark in benchmarks:
            if benchmark == "default" or benchmark == "example":
                continue
            if args.model_checking:
                if not args.check_all:
                    if local_config.getint(benchmark, 'DBUG') < 0:
                        logging.debug("Skip '%s'. Use '--check-all' option to check all configs." % benchmark)
                        continue
                if args.parallel > 1:
                    t = threading.Thread(target=workers, args=(semaphore, log_lock, local_config, benchmark))
                    t.start()
                    all_threads.append(t)
                else:
                    processBench(local_config, benchmark)
            else:
                processBench(local_config, benchmark)

        if args.model_checking:
            for t in all_threads:
                t.join()

        os.chdir(root_dir)
       
