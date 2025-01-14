import main
def test_file_content():
    file = open('Lista-zakupow.txt', 'r')
    txt = ''
    for product in main.product_list:
        txt += f'{main.product_list.index(product)+1}. {product}\n'

    assert txt == file.read()
