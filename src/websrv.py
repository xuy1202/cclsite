#coding: utf-8

import os, sys
import logging
import optparse
import traceback

import tornado.ioloop
import tornado.web
import tornado.httpserver

import conf
from webmod import ui_methods
from webmod import process


url_patterns = [
        (r"/"        , process.IndexHandler),
        (r"/post/.*" , process.ShowsHandler),
]


def main(Port=8080):
    application = tornado.web.Application(url_patterns
        , ui_methods = ui_methods
        , **conf.tornado_settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(Port)
    http_server.start(conf.MainConf.single().process)
    logger.info("PyServer Listen On: %s"%Port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    global options

    parser = optparse.OptionParser()
    parser.add_option('-d', '--daemon', 
                    action="store_true", dest="daemon", help="run as daemon")
    parser.add_option('-p', '--port', 
                    action="store", default=80, dest="port", type="int", 
                    help="listen port. default:%default")
    parser.add_option('-v', '--verbose', 
                    action="store_true", dest="verbose", help="set log level to debug")
    parser.add_option('-M', '--modules'
        , action="store", dest="modules"
        , type = "string", default="", help="set log level to debug"
    )
    options, args = parser.parse_args()

    if options.verbose:
        log_level = logging.DEBUG
    else:
        log_level = conf.LOG_LEVEL

    log_stdout = False if options.daemon else True
    conf.LogConfig("websrv", log_level, conf.LOG_FMT, conf.LOG_DATE_FMT, conf.LOG_PATH, log_stdout)
    logger = logging.getLogger("websrv.server")
    
    port =  args[0] if len(args) else options.port
    if options.daemon:
        conf.MainConf.single().DEBUG = False
        daemon.daemonize(main, port)
    else:
        main(port)


