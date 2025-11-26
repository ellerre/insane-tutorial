import hashlib
import ctypes

"""Convert a topic name to a unique topic ID using SHA-1 hashing."""
def topic_name_to_id(topic_name):
    hash = hashlib.sha1(topic_name.encode()).hexdigest()
    return int(hash[:8], 16)

"""Fill the given buffer with the specified character."""
def fill_buffer_with_char(buffer, char, size):
    ctypes.memset(buffer.contents.data, ord(char), size)