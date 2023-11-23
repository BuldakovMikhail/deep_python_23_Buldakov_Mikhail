import logging
import argparse


class FilterOutEven(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2


logging.basicConfig(
    filename="cache.log",
    level=logging.DEBUG,
    format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s",
)

logger = logging.getLogger(__name__)


class ListNode:
    def __init__(self, key=None, val=None):
        self.val = val
        self.key = key
        logger.debug("ListNode created (key=%s, value=%s)", key, val)
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, limit=42):
        if limit <= 0:
            logger.critical("Creating an LRUCache with incorrect limit")
            raise ValueError("Limit must be greater than zero")

        logger.debug("LRUCache object created")

        self.cache = {}
        self.head = None
        self.tail = None
        self.limit = limit

    def __delete_node(self, node):
        logger.debug("Delete node: (key=%s, value=%s)", node.key, node.val)
        if node == self.tail:
            logger.debug("Tail node was deleted")
            self.tail = node.next
            if self.tail:
                self.tail.prev = None
            else:
                logger.debug("All nodes were deleted")
                self.head = None

        elif node == self.head:
            logger.debug("Head node was deleted")
            self.head = node.prev
            if self.head:
                self.head.next = None
            else:
                logger.debug("All nodes were deleted")
                self.tail = None

        else:
            logger.debug("Neither head or tail was deleted")

            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

    def __add_node(self, node):
        logger.debug("Add node: (key=%s, value=%s)", node.key, node.val)
        if not self.head:
            logger.debug("Node added as a head")

            self.head = node
            self.tail = node
        else:
            self.head.next = node
            node.prev = self.head
            self.head = node

    def get(self, key):
        if key in self.cache:
            logger.info("Get: successfully get from cache by key %s", key)

            temp = self.cache[key]
            self.__delete_node(temp)
            self.__add_node(temp)

            return temp.val
        logger.error("Get: key %s not in cache", key)
        return None

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value

            logger.info("Set: the value=%s is set to the existing key=%s", value, key)

            self.__delete_node(node)
            self.__add_node(node)
        else:
            if len(self.cache) >= self.limit:
                self.cache.pop(self.tail.key)
                self.__delete_node(self.tail)
                logger.warning(
                    "Set: cache size exceeded, least recently key was deleted"
                )

            new_node = ListNode(key, value)
            self.__add_node(new_node)
            self.cache[key] = new_node
            logger.info("Set: added a new pair key=%s with a value=%s", key, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Some logged operations with LRU Cache"
    )
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-f", action="store_true")

    args = parser.parse_args()

    if args.s:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(
            logging.Formatter("LOGGER:\t%(levelname)s\t%(name)s\t%(message)s")
        )
        logger.addHandler(stdout_handler)

    if args.f:
        logger.addFilter(FilterOutEven())

    cache = LRUCache(3)
    cache.set(1, "v1")
    cache.set(2, "v2")
    cache.set(3, "v3")

    print(cache.get(3))
    print(cache.get(4))

    cache.set(4, "v4")
    cache.set(2, "v2_2")
