import os
from src.utils.supabase_client import supabase
import pkg_resources

API_KEY = os.getenv('API_KEY')
print(API_KEY)
print(supabase)

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
print(installed_packages_list)
