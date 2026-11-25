
from typing import TypeVar, Generic

# Define a generic type variable
T = TypeVar("T")


# 1. Create Generic Stack Class
class Stack(Generic[T]):

    def __init__(self):
        self.items: list[T] = []

    # Add an element to the stack
    def push(self, item: T) -> None:
        self.items.append(item)

    # Remove and return the top element
    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack!")
        return self.items.pop()

    # Return the top element without removing it
    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack!")
        return self.items[-1]

    # Check if stack is empty
    def is_empty(self) -> bool:
        return len(self.items) == 0

    # Return the number of elements
    def size(self) -> int:
        return len(self.items)

    def __str__(self):
        return str(self.items)


# 2. Create Stack[int] Example
print("--- Integer Stack ---")

int_stack: Stack[int] = Stack()

int_stack.push(10)
int_stack.push(20)
int_stack.push(30)

print("Stack:", int_stack)
print("Top Element:", int_stack.peek())
print("Stack Size:", int_stack.size())
print("Is Empty:", int_stack.is_empty())

print("Popped Element:", int_stack.pop())
print("Stack After Pop:", int_stack)


# 3. Create Stack[str] Example
print("\n--- String Stack ---")

str_stack: Stack[str] = Stack()

str_stack.push("Python")
str_stack.push("Java")
str_stack.push("C++")

print("Stack:", str_stack)
print("Top Element:", str_stack.peek())
print("Stack Size:", str_stack.size())

print("Popped Element:", str_stack.pop())
print("Stack After Pop:", str_stack)


# 4. Test Popping from Empty Stack
print("\n--- Empty Stack Test ---")

empty_stack: Stack[int] = Stack()

try:
    empty_stack.pop()
except IndexError as error:
    print("Error:", error)

print("Is Empty:", empty_stack.is_empty())


# 5. Optional: Generic Queue Class
class Queue(Generic[T]):

    def __init__(self):
        self.items: list[T] = []

    # Add an element to the queue
    def enqueue(self, item: T) -> None:
        self.items.append(item)

    # Remove the first element
    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue!")
        return self.items.pop(0)

    # Check if queue is empty
    def is_empty(self) -> bool:
        return len(self.items) == 0

    # Return queue size
    def size(self) -> int:
        return len(self.items)

    def __str__(self):
        return str(self.items)


# 6. Test Generic Queue
print("\n--- Generic Queue ---")

queue: Queue[str] = Queue()

queue.enqueue("Ahmad")
queue.enqueue("Ali")
queue.enqueue("Farid")

print("Queue:", queue)
print("Removed:", queue.dequeue())
print("Queue After Dequeue:", queue)
print("Queue Size:", queue.size())
