import pyml


def load_data(file_path):
    with open(file_path, 'r') as f:
        return list(map(lambda x: x.strip().split(','), f.readlines()))


if __name__ == '__main__':
    data = load_data('crx.data.csv')
    print(type(data))
    print(data[0])



