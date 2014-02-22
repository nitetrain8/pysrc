"""

Created by: Nathan Starkweather
Created on: 02/19/2014
Created in: PyCharm Community Edition

Hold some snippets that come in handy
when auto-generating python files.
"""
from collections.abc import Iterable
from datetime import datetime
from platform import python_version


_header_template = '''"""

Created by: Nathan Starkweather
Created on: {date}
Created in: PyCharm Community Edition

File autogenerated from {src_name}.

{msg_body}

"""

'''


default_src_name = "Python v%s" % python_version()


def make_header(src_name=default_src_name, body=''):
    """
    @param src_name: name of source to reference.
    @type src_name: str
    @param body: message body to write in header.
    @type body: collections.Iterable[str] | str
    @return: str
    @rtype: str
    """

    if isinstance(body, Iterable) and not isinstance(body, str):
        body = '\n'.join(body)

    date = datetime.now().strftime("%m/%d/%Y")

    header = _header_template.format(date=date,
                                     src_name=src_name,
                                     msg_body=body)
    return header

