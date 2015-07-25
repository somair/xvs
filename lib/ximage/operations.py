from PIL import Image, ImageOps

def square():
    """Returns the image cropped to a square."""
    def _square(image):
        # Find the shorter dimension
        width = min(*image.size)
        return ImageOps.fit(image, (width,width), Image.NEAREST, 0, (0.5, 0.5)) 
    _square.serial = "s"
        
    return _square

def resize(w, h):
    """Returns a resized image. Aspect ratio is not preserved."""
    def _resize(image):
        return image.resize((w,h), Image.ANTIALIAS)
    _resize.serial = "r%dx%d" % (w, h)

    return _resize
