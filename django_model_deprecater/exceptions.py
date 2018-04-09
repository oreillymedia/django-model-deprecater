class DeprecatedModelException(Exception):
    base_msg = ("Use of the '{}' model is deprecated and not allowed at the "
                "database level. Please review the calling context and fix "
                "your usage of this model.")

    def __init__(self, model_path, extra_msg=''):
        msg = self.base_msg.format(model_path)
        if extra_msg:
            msg = "{} {}".format(msg, extra_msg)
        super(DeprecatedModelException, self).__init__(msg)
