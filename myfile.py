class Topic:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        self.messages = []

    def add_subscriber(self, user):
        if user not in self.subscribers:
            self.subscribers.append(user)

    def add_message(self, message):
        self.messages.append(message)


class Message:
    def __init__(self, id, topic_name, text, timestamp=None):
        self.id = id
        self.topic_name = topic_name
        self.text = text
        self.timestamp = timestamp


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.subscribed_topics = []

    def subscribe(self, topic):
        if topic not in self.subscribed_topics:
            self.subscribed_topics.append(topic)


class Publisher:
    def __init__(self, topics):
        self.topics = topics

    def publish_message(self, message):
        topic = next((t for t in self.topics if t.name == message.topic_name), None)
        if topic:
            topic.add_message(message)
            print("msg published")
            return message
        print(f"no topic: {message.topic_name}")
        return None


class Consumer:
    def __init__(self, topics):
        self.topics = topics

    def process_messages(self):
        print("processing...")
        for topic in self.topics:
            for message in topic.messages:
                for user in topic.subscribers:
                    print(f"{{\ntopic: {topic.name},\nmessage: {message.text}\nsent to: {user.username}\n}}")
                    print("messages successfully processed.")
        print("done")


def add_topic(topics, topic_name, admin_username, users):
    if admin_username not in users or users[admin_username].role != "ADMIN":
        print("only admin")
        return
    topic = Topic(topic_name)
    topics[topic_name] = topic
    print("topic added")


def add_user(users, username, role):
    if username in users:
        print("user exists")
        return
    user = User(username, role)
    users[username] = user
    print("user added")


def publish_message(publisher, message_body):
    message = Message(message_body['id'], message_body['topicName'], message_body['text'])
    publisher.publish_message(message)


def subscribe_topic(users, topics, topic_name, username):
    if username not in users:
        print("user not found")
        return
    user = users[username]
    topic = topics.get(topic_name)
    if not topic:
        print("topic not found")
        return
    user.subscribe(topic)
    topic.add_subscriber(user)
    print("subscribed")


def process_messages(consumer):
    consumer.process_messages()


def main():
    users = {}
    topics = {}

    while True:
        print("\ncommand:")
        command = input().strip()
        parts = command.split()
        if not parts:
            continue

        cmd = parts[0].lower()

        if cmd == "adduser" and len(parts) == 3:
            username = parts[1]
            role = parts[2].upper()
            if role not in ["ADMIN", "USER"]:
                print("invalid role")
                continue
            add_user(users, username, role)

        elif cmd == "addtopic" and len(parts) == 3:
            topic_name = parts[1]
            admin_username = parts[2]
            add_topic(topics, topic_name, admin_username, users)

        elif cmd == "subscribetopic" and len(parts) == 3:
            topic_name = parts[1]
            username = parts[2]
            subscribe_topic(users, topics, topic_name, username)

        elif cmd == "publishmessage" and len(parts) >= 3:
            try:
                message_id = parts[1]
                topic_name = parts[2]
                text = " ".join(parts[3:])
                message_body = {"id": message_id, "topicName": topic_name, "text": text}
                publisher = Publisher(topics.values())
                publish_message(publisher, message_body)
            except IndexError:
                print("usage: publishmessage <id> <topic> <text>")

        elif cmd == "processmessages":
            consumer = Consumer(topics.values())
            process_messages(consumer)

        elif cmd == "exit":
            print("bye")
            break

        else:
            print("invalid cmd")


if __name__ == "__main__":
    main()
