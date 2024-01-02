# -*-coding:utf-8 -*-
from kafka import KafkaConsumer
from kafka import KafkaProducer


class KafkaFunction():

    def __init__(self):
        pass

    def kafka_producer(self, conectinfo, topic, message):
        '''
        往kafka指定的topic生产数据，目前只支持单条数据，注意需要kafka开启listen，允许访问
        :param conectinfo: 必填，kafka连接信息，格式为ip:port,例如：10.21.47.143:9092
        :param topic: 必填，生产数据的topic名称
        :param message: 必填，生产的数据，单条
        :return: 无返回值

        举例：Kafka Producer     10.21.47.143:9092    test     this is a apple
             表示连接10.21.47.143:9092的kafka，往topic：test里生成一条数据：this is a apple
        '''
        producer = KafkaProducer(bootstrap_servers=[conectinfo])
        producer.send(topic, bytes(message, encoding='utf-8'))
        producer.close()

    def kafka_consumer(self, conectinfo, topic, auto_offset_reset='latest', consumerNum=1, timeout=30):
        '''
        从kafka指定的topic消费数据，注意需要kafka开启listen，允许访问
        :param conectinfo: 必填，kafka连接信息，格式为ip:port,例如：10.21.47.143:9092
        :param topic: 必填，消费数据的topic名称
        :param auto_offset_reset: 可选，消费策略:earliest,表示重头开始消费；latest，表示从最新的数据开始消费，默认为latest
        :param consumerNum:可选，需要消费的数据条数，默认为1
        :param timeout:可选，超过多少时间没有消费到数据，直接断开，默认为30s
        :return:返回消费到的数据，用@|@隔开

        举例：Kafka Consumer   10.21.47.143:9092   test    latest  10  10
             表示连接10.21.47.143:9092的kafka，从topic：test里从最新开始消费数据，消费10条，如果10s内消费不到数据，断开连接
        '''
        try:
            timeout = int(timeout)
            assert 600 >= timeout >= 0
        except:
            raise RuntimeError('超时时间只能是不超过600的正整数')
        if timeout > 0:
            consumer = KafkaConsumer(topic,
                                     bootstrap_servers=[conectinfo], auto_offset_reset=auto_offset_reset,
                                     consumer_timeout_ms=timeout * 1000
                                     )
            data = ''
            count = 0
            for message in consumer:
                if message is not None:
                    print(message)
                    data = data + str(message.value, encoding="utf-8") + '@|@'
                    count += 1
                if count >= consumerNum:
                    break
            consumer.close()
            if data == '':
                raise RuntimeError('{}秒内没有消费到数据'.format(timeout))
            elif count < consumerNum:
                raise RuntimeError('期望消费到{}条数据，实际消费到{}条数据'.format(consumerNum, count))
            data = data.rstrip('@|@')
            return (data)


if __name__ == '__main__':
    conectinfo = '10.21.47.143:9092'
    a = KafkaFunction()
    a.kafka_consumer(conectinfo, 'test', consumerNum=20, timeout=5)
    # a.kafka_producer(conectinfo,'test',count)
