from basic import BaseModel, Collection, _ts2dt

class Report(BaseModel):
    def __init__(self, api):
        super().__init__(api)

        self.id = d.pop('id')
        self.owner = d.pop('owner')
        self.start = _ts2dt(d.pop('start'))
        self.end = _ts2dt(d.pop('end'))
        self.title = d.pop('title')
        self.zone = api.zones[d.pop('zone')]

        if d:
            raise ValueError("Unrecognized keys")
