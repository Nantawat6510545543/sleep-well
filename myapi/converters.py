class FloatUrlParameterConverter:
    regex = r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
