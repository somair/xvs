import StringIO
import hashlib

from PIL import Image

class ImageProcessor(object):
    """Holds a list of processes to be applied to an image, and manages a cache of the results."""
    def __init__(self, cache, process):
        self.cache = cache
        self._process = process
        self._process_key = self.serialise_process()

    def process(self, path):
        key = self.make_key(path)
        try:
            return self.cache.get(key)
        except ImageCache.KeyNotFound:
            # Load the image
            image = self.load(path)
            # Apply the process
            for operation in self._process:
                image = operation(image)
            # Convert to JPEG
            o = StringIO.StringIO()
            image.save(o, "JPEG")
            data = o.getvalue()
            # Store the image
            self.cache.put(key, data)

            return data

    def load(self, path):
        """Return an Image from a path"""
        image = Image.open(path)
        
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        
        return image

    def make_key(self, path):
        """Makes a unique key for the image and process."""
        # Hash the path
        m = hashlib.md5()
        m.update(path)
        return m.hexdigest() + "_" + self._process_key

    
    def serialise_process(self):
        """Returns a unique string description of the process applied to the image."""
        return "_".join([op.serial for op in self._process])

        


class ImageCache(object):
    """Provides a persistence mechanism for processed images. Typically a disk store."""
    class KeyNotFound(Exception):
        pass

    def __init__(self, path):
        self.path = path

    def get(self, key):
        raise ImageCache.KeyNotFound()

    def put(self, key, data):
        pass
        
    def delete(self, key):
        pass

