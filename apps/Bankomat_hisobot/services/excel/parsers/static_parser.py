class StaticParser:

    @classmethod
    def apply(cls, row, column, value):

        setattr(
            row,
            column.field,
            value,
        )