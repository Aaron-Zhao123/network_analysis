def read_fb():
    file_name = 'facebook/0.edges'
    raw_in = []
    node_hash = {}
    with open(file_name, 'r') as f:
        for line in f:
            val = [int(item) for item in line.split(' ')]
            if (val[0] in node_hash):
                node_hash[val[0]].append(val[1])
            else:
                node_hash[val[0]] = [val[1]]
            if (val[1] in node_hash):
                node_hash[val[1]].append(val[0])
            else:
                node_hash[val[1]] = [val[0]]
    print(node_hash)
if __name__ == '__main__':
    read_fb()
