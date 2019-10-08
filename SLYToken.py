class Token(object):
    '''
    Representation of a single token.
    '''
    __slots__ = ('type', 'value', 'lineno', 'index')
    def __repr__(self):
        return f'Token(type={self.type!r}, value={self.value!r}, lineno={self.lineno}, index={self.index})'