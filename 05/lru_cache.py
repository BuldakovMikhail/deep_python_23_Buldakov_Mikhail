class ListNode:
    def __init__(self, key=None, val=None):
        self.val = val
        self.key = key
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError("Limit must be greater than zero")

        self.cache = {}
        self.head = None
        self.tail = None
        self.limit = limit

    def __delete_node(self, node):
        if node == self.tail:
            self.tail = node.next
            if self.tail:
                self.tail.prev = None
            else:
                self.head = None

        elif node == self.head:
            self.head = node.prev
            if self.head:
                self.head.next = None
            else:
                self.tail = None

        else:
            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

    def __add_node(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.head.next = node
            node.prev = self.head
            self.head = node

    def get(self, key):
        if key in self.cache:
            temp = self.cache[key]
            self.__delete_node(temp)
            self.__add_node(temp)

            return temp.val

        return None

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value

            self.__delete_node(node)
            self.__add_node(node)
        else:
            if len(self.cache) >= self.limit:
                self.cache.pop(self.tail.key)
                self.__delete_node(self.tail)

            new_node = ListNode(key, value)
            self.__add_node(new_node)
            self.cache[key] = new_node
