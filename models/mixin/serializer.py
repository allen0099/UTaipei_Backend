from sqlalchemy.inspection import inspect


# https://stackoverflow.com/a/27951648
class Serializer:

    def serialize(self):
        _tmp = [[_, getattr(self, _)] for _ in inspect(self).attrs.keys() if not _.startswith("_") and not _.endswith("_")]
        for _ in _tmp:
            if isinstance(_[1], list):
                _[1] = [c.serialize() for c in _[1]]

        return {
            _[0]: _[1] for _ in _tmp
        }

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
