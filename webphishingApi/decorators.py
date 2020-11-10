from functools import wraps
from django.http import HttpResponse

# Import settings
#from webphishingApi.models import *
#from webphishingAuth.models import *
#from webphishingCore.models import *
#from webphishingClient.models import *
#from webphishingManagement.models import *

import importlib
import sys

# Grab class
def _GetClass(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

# Decortaros
def required_fields(required_list):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :
            for variable, model in required_list:

                # Check if its object
                if type(model) is str:
                    # Get class
                    classObj = _GetClass(model)
                    if classObj is None:
                            return HttpResponse('', status=404)
                    
                    # Get variable
                    if variable not in request.POST:
                            return HttpResponse(f'Needed data is not present.', status=500)
                    else:
                            varName = variable
                            variable = request.POST.get(variable)
                            setattr(request, varName, variable)

                    if not classObj.Exists(variable):
                            return HttpResponse(f'{varName}, doest not match nor exists.', status=500)
                
                # Check if its a choice variable
                elif type(model) is list:
                    value = request.POST.get(variable)
                    if value not in model:
                        return HttpResponse(f'{variable}, value not valid nor found.', status=500)
                    else:
                        setattr(request, variable, value)

                # Check if free data
                elif model is None:
                    if variable not in request.POST:
                        return HttpResponse(f'Needed data is not present.', status=500)

                    value = request.POST.get(variable)
                    setattr(request, variable, value)
                    
            return view_method(request, *args, **kwargs)            
                
        return _arguments_wrapper
    return _method_wrapper
