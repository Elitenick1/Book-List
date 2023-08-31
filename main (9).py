#I have been having this recursive bug. im not sure how to fix it without having to write all this code without recursion(which i dont think is possible)
import sys
print(sys.getrecursionlimit())
import csv
class Node:
    #creates a new node and sets the next node to be none
  def __init__(self, data, parent = None):
    self.data = data
    self.left_node = None 
    self.right_node = None
    self.parent = None
    
  #returns the string representation of the node
  def __repr__(self):
    return str(self.data)

    
class BinarySearchTree:
  #initializes an instance variable called root to None in the constructor
  def __init__(self):
    self.root = None

  #inserts a new node with a given data into a tree structure, creating a new root node if there isnt one already
  def insert(self, data):
    if self.root is None:
      self.root = Node(data)
    else:
      self.insert_node(data, self.root)  

    #recursivly inserts a new node with a given data into a binary search tree structure thing based on its title attribute, navigating to the left or right child node of each existing node depending on the result of the comparison until an empty node is found.
  def insert_node(self, data, node):
    if data.title < node.data.title:
      #print(f"{data.title} is less than {node.data.title}, going left...")
      
      if node.left_node is not None:
        self.insert_node(data, node.left_node)
      else:
        #print(f"there is no left child, so we will create one")
        node.left_node = Node(data, node)

    else:
      #print(f"{data.title} is greater than or equal to {node}, going right...")
      if node.right_node is not None:
        self.insert_node(data, node.right_node)
      else:
        #print(f"there is no right child, so we will create one")
        node.right_node = Node(data, node)

  #returns the minimun(aka the left most) value from the bst by traversing through the left most child node of the root node until it reaches the end. then it returns the title atribute of the data stored in that node
  def get_min(self):
    node = self.root
    while node.left_node is not None:
      node = node.left_node
    return node.data.title

  #returns the max(aka the right most) value from the bst by traversing throught the right most child node of the root node until it reaches the end. then it returns the title atribute of the data stored in that node
  def get_max(self):
    node = self.root
    while node.right_node is not None:
      node = node.right_node
    return node.data.title

  #searches for the node in the bst based of the title atribute of its data, comparing the title of each node to a given title until it finds a match. then it returns the title atribute of the matched node
  def get_book(self, find_title):
    node = self.root
    while node.data.title.upper() != find_title.upper():
      if find_title.upper() < node.data.title.upper():
        node = node.left_node
      elif find_title.upper() > node.data.title.upper():
        node = node.right_node
    return node.data.title

  #does the same thing as get_book, but instead it returns the matched node object
  def get_node(self, find_title):
    node = self.root
    while node.data.title.upper() != find_title.upper():
      if find_title.upper() < node.data.title.upper():
        node = node.left_node
      elif find_title.upper() > node.data.title.upper():
        node = node.right_node
    return node

  #removes a node given the title from a bst by finding the node based on the title attribute, and then removing it based on three things. (1) if the node is at the end. (2) if the node has one child node, then that child node will take the OG nodes place. (3) if the node has two children, then it replaces the node with the right most child node, and recursivly removes that child node. the code then returns the removed node
  def remove_book(self, title):
    book = Book.all_books.get_node(title)
    while book is not None:
      if book.left_node is None and book.right_node is None:
        if book == book.parent.right_node:
          book.parent.right_node = None
        else:
          book.parent.left_node = None
      elif book.left_node is None or book.right_node is None:
        if book == book.parent.right_node:
          if book.right_node is None:
            book.parent.right_node = book.left_node
          else:
            book.parent.right_node = book.right_node
        else:
          if book.left_node is None:
            book.parent.left_node = book.right_node
          else:
            book.parent.left_node = book.left_node
      else:
        temp_node = book.left_node
        while temp_node.right_node is None:
          temp_node = temp_node.right_node
        book.data = temp_node.data
        book = Book.all_books.get_node(title)
        #Book.all_books.remove_book(temp_node.data.title) #this might be causing an infinite loop?
    return book

      
class Book:
  all_books = BinarySearchTree()
  #defines a Book class constructor with attributes for publisher, author, title, ISBN, date, weeks_on_list. sets the status attribute to "In Stock". also inserts the book object into the bst of all books
  def __init__(self, publisher, author, title, ISBN, date, weeks_on_list):
    self.publisher = publisher
    self.author = author
    self.title = title
    self.ISBN = ISBN
    self.date = date
    self.weeks_on_list = weeks_on_list
    self.status = "In Stock"
    Book.all_books.insert(self)

  #returns a string of a book objects title and author
  def __repr__(self):
    #return f"Publisher: {self.publisher}, Author: {self.author}, Title: {self.title}, ISBN: {self.ISBN}, Date: {self.date}, Weeks on List: {self.weeks_on_list}"
    return f"{self.title} by {self.author}"
    
  @classmethod
  #imports books from the csv file. creats a new book object for each book, with attributes for publisher, author, ISBN, date, title, and weeks on the list.
  def import_books(cls, filename: str):
    with open(filename, "r") as f:
      reader = csv.DictReader(f)
      items = list(reader)
    for item in items:
      Book(
        publisher=item.get('Publisher'),
        author=item.get('Author'),
        ISBN=item.get('Primary ISBN10'),
        date=item.get('Date'), 
        title=item.get('Title'),
        weeks_on_list=int(float(item.get('Weeks on list')))
        )
    
    
#tests our code
if __name__ == '__main__':
  Book.import_books("New York Times.csv")
  bst = BinarySearchTree()
  print(Book.all_books.remove_book("THE LONGEST RIDE"))
  print(Book.all_books.get_book("THE LONGEST RIDE"))
  #print(Book.all_books.root)
  #print(Book.all_books.get_min())
  #print(Book.all_books.get_max())