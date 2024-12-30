
class Configurer(object):

    def __init__(self, file_type: str, config: object):
        """
        Create a configurer object. You need to provide file_type and the object that is intended to be persisted
        :param file_type: File type of the configuration
        :param config: expects the configuration object and will load it in matching the filetype
        """
        self.file_type = file_type
        self.object = config