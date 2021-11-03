from django.contrib import admin
from .models import Human_model_img
from .models import Cloth_img
from .models import made_cloth

admin.site.register(Human_model_img)
admin.site.register(Cloth_img)
admin.site.register(made_cloth)