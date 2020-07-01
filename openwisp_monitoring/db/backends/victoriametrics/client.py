import json
from datetime import datetime

import requests
from django.utils.functional import cached_property

# TODO: Remove these. Added them just for reference ;)
# CuRL Flags
# -d - data
# -X - Specifies custom requests method {POST, PUT, DELETE} to be used in place of default 'GET'
# -G - get


class DatabaseClient(object):
    """
    Python Client for Victoria Metrics
    """

    # TODO: Authentication needs to be allowed
    # eg. requests.get('https://api.github.com/user', auth=('user', 'pass'))
    base_url = 'http://localhost:8428/'

    def create_database(self):
        pass

    def create_or_alter_retention_policy(self, *args):
        pass

    @cached_property
    def session(self):
        return requests.Session()

    def _change_format(self, dictionary):
        """
        Takes in dictionary and outputs string in format
        suitable for line protocol
        """
        if not isinstance(dictionary, dict):
            return
        dict_list = [f'{k}="{str(v)}"' for k, v in dictionary.items()]
        return ','.join(dict_list)

    def write(self, name, values, tags, **kwargs):
        """ Write metrics via the line protocol """
        # TODO: Have timeout and repeat in case of failure
        # TODO: Define expected status code on success
        tags = self._change_format(tags)
        fields = self._change_format(values)
        data = f'{name},{tags} {fields}'
        timestamp = kwargs.get('timestamp') or datetime.now()
        if timestamp:
            if isinstance(timestamp, datetime):
                timestamp = float(timestamp.strftime('%s.%f'))
            # nanoseconds precision is required by line
            # protocol and convert to suitable format
            timestamp = format(timestamp, '.9f').replace('.', '')
            data = f'{data} {timestamp}'
        self.session.post(f'{self.base_url}write', data)
        # TODO: Database and retention policy selection
        # It might be done by modifying the link, as in case of InfluxDB
        # 'http://localhost:8428/write?db=mydb&rp=myrp'

    def read(self, key, fields, tags, **kwargs):
        """ returns all fields with the given key and tags """
        url = f'{self.base_url}api/v1/export'
        # TODO: Add support for  limit, since, order parameters
        # TODO: This will break currently, if there are no tags, fix it.
        params = {
            'match': '{__name__=~"{key}_.*"'.replace('{key}', key)
            + ', {tags}}'.replace('{tags}', self._change_format(tags))
        }
        response = self.session.get(url, params=params)
        if response.status_code == 400:
            return []
        points = [json.loads(p) for p in response.content.decode('utf-8').split('\n')[:-1]]
        return points
