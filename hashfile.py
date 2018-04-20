import hashlib

class HashedFile(object):
    def __init__(self, filename, hasher, block):
        self.name   = filename
        self.hasher = hasher
        self.block  = block
        self._id    = None
        
    @property
    def id(self):
        if self._id is None:
            self._id = self._hash_file(filename)

    def _hash_file(self, path):    
        with open(path, 'rb') as f:
            hash_buffer = f.read(self.block)
            while 0 < len(hash_buffer):
                self.hasher.update(hash_buffer)
                hash_buffer = f.read(self.block)
    
        return self.hasher.hexdigest()
