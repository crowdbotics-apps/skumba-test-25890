import os
import environ

env = environ.Env()

ENVIRONMENT = env.str('ENVIRONMENT', default='dev')

exec('from .{} import *'.format(ENVIRONMENT))
