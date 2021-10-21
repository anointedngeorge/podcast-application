from account.models import Gallary




def gallery(image_number):
    image = Gallary.objects.all().get(id = int(image_number))
    return image.file