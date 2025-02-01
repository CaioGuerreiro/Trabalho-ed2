class Node:
    def __init__(self, key, color='RED'):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, color='BLACK')
        self.root = self.NIL

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.color = 'RED'

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node.parent and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._left_rotate(node.parent.parent)

            if node == self.root:
                break

        self.root.color = 'BLACK'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def deleteByVal(self, key):
        node = self._search(self.root, key)
        if node == self.NIL:
            return
        self._delete_node(node)

    def _delete_node(self, node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == 'BLACK':
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._left_rotate(x.parent)
                    sibling = x.parent.right

                if sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK':
                    sibling.color = 'RED'
                    x = x.parent
                else:
                    if sibling.right.color == 'BLACK':
                        sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self._right_rotate(sibling)
                        sibling = x.parent.right

                    sibling.color = x.parent.color
                    x.parent.color = 'BLACK'
                    sibling.right.color = 'BLACK'
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._right_rotate(x.parent)
                    sibling = x.parent.left

                if sibling.right.color == 'BLACK' and sibling.left.color == 'BLACK':
                    sibling.color = 'RED'
                    x = x.parent
                else:
                    if sibling.left.color == 'BLACK':
                        sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self._left_rotate(sibling)
                        sibling = x.parent.left

                    sibling.color = x.parent.color
                    x.parent.color = 'BLACK'
                    sibling.left.color = 'BLACK'
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = 'BLACK'

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    def _maximum(self, node):
        while node.right != self.NIL:
            node = node.right
        return node


    def _search(self, node, key):
        while node != self.NIL and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node
    
    def find(self, key):
        node = self._search(self.root, key)
        if node == self.NIL:
            return 'Nó não encontrado'
        return 'Nó encontrado   ' + str(node.key)
    
    def findMin(self):
        if self.root == self.NIL:
            return None
        return self._minimum(self.root).key
    
    def findMax(self):
        if self.root == self.NIL:
            return None
        return self._maximum(self.root).key
    
    def findKth(self, k):
        if k < 1:
            return None
        self.kth_count = 0
        return self._find_kth_helper(self.root, k)

    def _find_kth_helper(self, node, k):
        if node == self.NIL:
            return None

        # Percorre a subárvore esquerda
        left_result = self._find_kth_helper(node.left, k)
        if left_result is not None:
            return left_result

        # Conta o nó atual
        self.kth_count += 1
        if self.kth_count == k:
            return node.key

        # Percorre a subárvore direita
        return self._find_kth_helper(node.right, k)
    
    def printTree(self):
        self._print_tree_helper(self.root, "", True)

    def _print_tree_helper(self, node, indent, last):
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("└── ", end="")
                indent += "    "
            else:
                print("├── ", end="")
                indent += "│   "

            # Exibe o valor do nó e sua cor
            color = "V" if node.color == 'RED' else "P"
            print(f"{node.key} ({color})")

            # Recursivamente imprime os filhos
            self._print_tree_helper(node.left, indent, False)
            self._print_tree_helper(node.right, indent, True)



    def printInOrder(self):
        self._in_order_traversal(self.root)
        print()

    def _in_order_traversal(self, node):
        if node != self.NIL:
            self._in_order_traversal(node.left)
            print(node.key, end=' ')
            self._in_order_traversal(node.right)    

#1. Insira as chaves 5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1, nesta ordem.
rb_tree = RedBlackTree()
rb_tree.insert(5)
rb_tree.insert(16)
rb_tree.insert(22)
rb_tree.insert(45)
rb_tree.insert(2)
rb_tree.insert(10)
rb_tree.insert(18)
rb_tree.insert(30)
rb_tree.insert(50)
rb_tree.insert(12)
rb_tree.insert(1)

print("árvore antes da inserção")
rb_tree.printInOrder()

#2. Procure pelas chaves 22 e 15.
print("find nó: ", rb_tree.find(22))
print("find nó: ", rb_tree.find(15))


#3. Exclua as chaves 30, 10 e 22, nesta ordem. Insira as chaves 25, 9, 33 e 50, nesta ordem.
rb_tree.deleteByVal(30)
rb_tree.deleteByVal(10)
rb_tree.deleteByVal(22)

print('árvore depois da exclusão do 30, 10 e 22:')
rb_tree.printInOrder()

rb_tree.insert(25)
rb_tree.insert(9)
rb_tree.insert(33)
rb_tree.insert(50)

print('árvore depois da inserção do 25, 9, 33 e 50:')
rb_tree.printInOrder()

#4. Encontre o maior, o menor e o quinto menor valor da  ́arvore.
print("find min: ", rb_tree.findMin())
print("find max: ", rb_tree.findMax())
print("find kth: ", rb_tree.findKth(5))

rb_tree.printTree()

