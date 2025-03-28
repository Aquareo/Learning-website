def detect_cycle(head):
    if head is None:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def create_cycle_list(values, pos):
    head = ListNode(values[0])
    current = head
    cycle_node = None

    for i in range(1, len(values)):
        current.next = ListNode(values[i])
        current = current.next
        if i == pos:
            cycle_node = current

    if cycle_node:
        current.next = cycle_node

    return head

# Example usage
if __name__ == "__main__":
    values = [3, 2, 0, -4]
    pos = 1
    head = create_cycle_list(values, pos)
    print(detect_cycle(head))  # Output: True