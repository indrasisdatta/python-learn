import requests

def getProducts():
    url = "https://api.freeapi.app/api/v1/public/randomproducts?page=1&limit=10&inc=category%2Cprice%2Cthumbnail%2Cimages%2Ctitle%2Cid&query=mens-watches"
    response = requests.get(url)
    data = response.json()   
    products_list = {}
    if data['success'] and 'data' in data:
        products_list = data['data']
        # Store product title and price of each item
        result_prod = []
        if len(products_list['data']) > 0:
            for prod in products_list['data']:
                result_prod.append((prod['title'], prod['price']))
        return result_prod
    else: 
        raise Exception('Failed to fetch data')    

def main():
    try:
        prod_items = getProducts()
        print(prod_items)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()