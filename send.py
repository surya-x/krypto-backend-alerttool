import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declaring the queue
channel.queue_declare(queue='hello')

# Publishing to the queue
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent msg")
connection.close()