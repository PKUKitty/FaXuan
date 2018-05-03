# coding=utf-8
import redis


class RedisProcessor:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def insert_single_choice(self, question, answer):
        """

        :param question:
        :param answer:
        :return:
        """
        self.r.set(question, answer)

    def get_single_choice(self, question):
        """

        :param question:
        :return:
        """
        return self.r.get(question)

    def insert_multi_choice(self, question, answer_array):
        """

        :param question:
        :param answer_array:
        :return:
        """
        answer_str = ''
        for answer in answer_array:
            answer_str += answer + '^&^&'
        self.r.set(question, answer_str)

    def get_multi_choice(self, question):
        """

        :param question: multi choice question
        :return: array
        """
        answer_str = self.r.get(question)
        return answer_str.split('^&^&')

    def insert_true_false(self, question, value):
        """

        :param question:
        :param value: true-1,false-0
        :return:
        """
        self.r.set(question, value)

    def get_true_false(self, question):
        """

        :param question:
        :return:
        """
        return self.r.get(question)


if __name__ == "__main__":
    redis_processor = RedisProcessor()
    req = '下列关于党和共产主义青年团的关系的说法不准确的一项是（ ）。'
    # redis_processor.insert_true_false(req, 1)
    # print redis_processor.get_true_false(req)

    answer1 = '人民'
    # redis_processor.insert_single_choice(req, answer1)
    tmp = redis_processor.get_single_choice(req)
    print 'tmp answer: ' + tmp
    if answer1 == tmp:
        print '=='

    answer_array1 = ['人民', '党国', '北京']
    redis_processor.insert_multi_choice(req, answer_array1)
    answer_array2 = redis_processor.get_multi_choice(req)
    for answer2 in answer_array2:
        print answer2

