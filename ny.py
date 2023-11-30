import mysql.connector

config = {
    'host': 'localhost',
    'database': 'northwind',
    'user': 'root',
    'password': 'password',
}

def print_table_info(table_info):
    for key, value in table_info.items():
        print(f'{key}: {value}')

def show_all_tables(cursor):
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    for table in tables:
        print(table)

def main():
    tables_info = {
        'Categories': {
            '1': 'CategoryID',
            '2': 'CategoryName',
            '3': 'Description',
            '4': 'Picture',
        },
        'Customers': {
            '1': 'CustomerID',
            '2': 'CompanyName',
            '3': 'ContactName',
            '4': 'ContactTitle',
            '5': 'Address',
            '6': 'City',
            '7': 'Region',
            '8': 'PostalCode',
            '9': 'Country',
            '10': 'Phone',
            '11': 'Fax',
        },
        'Employees': {
            '1': 'EmployeeID',
            '2': 'LastName',
            '3': 'FirstName',
            '4': 'Title',
            '5': 'TitleOfCourtesy',
            '6': 'BirthDate',
            '7': 'HireDate',
            '8': 'Address',
            '9': 'City',
            '10': 'Region',
            '11': 'PostalCode',
            '12': 'Country',
            '13': 'HomePhone',
            '14': 'Extension',
            '15': 'Photo',
            '16': 'Notes',
            '17': 'ReportsTo',
            '18': 'PhotoPath',
        },
        'OrderDetails': {
            '1': 'OrderID',
            '2': 'ProductID',
            '3': 'UnitPrice',
            '4': 'Quantity',
            '5': 'Discount',
        },
        'Orders': {
            '1': 'OrderID',
            '2': 'CustomerID',
            '3': 'EmployeeID',
            '4': 'OrderDate',
            '5': 'RequiredDate',
            '6': 'ShippedDate',
            '7': 'ShipVia',
            '8': 'Freight',
            '9': 'ShipName',
            '10': 'ShipAddress',
            '11': 'ShipCity',
            '12': 'ShipRegion',
            '13': 'ShipPostalCode',
            '14': 'ShipCountry',
        },
        'Products': {
            '1': 'ProductID',
            '2': 'ProductName',
            '3': 'SupplierID',
            '4': 'CategoryID',
            '5': 'QuantityPerUnit',
            '6': 'UnitPrice',
            '7': 'UnitsInStock',
            '8': 'UnitsOnOrder',
            '9': 'ReorderLevel',
            '10': 'Discontinued',
        },
        'Shippers': {
            '1': 'ShipperID',
            '2': 'CompanyName',
            '3': 'Phone',
        },
        'Suppliers': {
            '1': 'SupplierID',
            '2': 'CompanyName',
            '3': 'ContactName',
            '4': 'ContactTitle',
            '5': 'Address',
            '6': 'City',
            '7': 'Region',
            '8': 'PostalCode',
            '9': 'Country',
            '10': 'Phone',
            '11': 'Fax',
            '12': 'HomePage',
        },
        'Territories': {
            '1': 'TerritoryID',
            '2': 'TerritoryDescription',
            '3': 'RegionID',
        },
        'Region': {
            '1': 'RegionID',
            '2': 'RegionDescription',
        },
    }

    connection = None
    try:
        while True:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print('Ansluten till MySQL-databasen')
                menu = input('1:Select, 2:Insert, 3:Update, 4:Delete, 5:Exit:\n>>>')
                if menu == '1':
                    print('Vilken tabell vill du läsa från?: ')
                    count = 1
                    for key, value in tables_info.items():
                        print(f'{count}:{key}')
                        count += 1
                    table_number = input('Välj tabellnummer: ')
                    table_name = list(tables_info.keys())[int(table_number) - 1]
                    
                    if table_name in tables_info:
                        print('Vilka kolumner vill du läsa?: ')
                        print_table_info(tables_info[table_name])
                        columns_number = input('Välj kolumnnummer: ')
                        columns = ', '.join(list(tables_info[table_name].values())[int(columns_number) - 1].split())
                        with connection.cursor() as cursor:
                            cursor.execute(f'SELECT {columns} FROM {table_name}')
                            rows = cursor.fetchall()
                            for row in rows:
                                print(f'{columns}: {row[0]}')
                    else:
                        print('Felaktig inmatning')
                        break
                else:
                    break

    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        if connection and connection.is_connected():
            connection.close()
            print('Anslutningen stängd')

if __name__ == "__main__":
    main()
