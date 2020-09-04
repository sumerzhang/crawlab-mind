class HtmlBase(object):
    @staticmethod
    def get_mean_value(o_list, o_attr) -> float:
        values = []
        for o in o_list:
            values.append(getattr(o, o_attr))
        return sum(values) / len(values)

    @staticmethod
    def get_total_value(o_list, o_attr) -> float:
        values = []
        for o in o_list:
            values.append(getattr(o, o_attr))
        return sum(values)

    @staticmethod
    def get_total_count(o_list) -> int:
        return len(o_list)

    def get_score(self, method) -> float:
        return NotImplementedError
