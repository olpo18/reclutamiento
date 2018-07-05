import os
import uuid

def get_file_path(instace, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('files/' ,filename)