import pika


def main(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declaring the queue
    channel.queue_declare(queue='hello')

    # Publishing to the queue
    channel.basic_publish(exchange='', routing_key='hello', body=msg)
    print(" [x] Sent msg")
    connection.close()


if __name__ == '__main__':
    my_msg = "ALERT!!"
    main(my_msg)