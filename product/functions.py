import pandas as pd

from product.models import Product, Category, Color, Brand, UploadedFile


# this function will handle the file as per the extension and store the data into DB.

def handle_file(file_id):

    file = UploadedFile.objects.get(id=file_id).file

    if file.name.endswith('.csv'):
        all_data = pd.read_csv(file)
    if file.name.endswith('.xlsx'):
        all_data = pd.read_excel(file)

    for data in all_data.to_dict('records'):
        try:
            pass
            _, created = Product.objects.get_or_create(
                product_name=data.get('product_name'),
                description=data.get('description'),
                category=Category.objects.get(id=data.get('category')),
                brand=Brand.objects.get(id=data.get('brand')),
                color=Color.objects.get(id=data.get('color')),
                price=data.get('price'),
                size=data.get('size'),
                type=data.get('type')
            )
        except Exception as e:
            print(e)
            break
