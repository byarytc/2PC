import psycopg2
import container_config

# setting up connections

conn_customer = psycopg2.connect(dbname=container_config.DB_NAME_CUSTOMER, user=container_config.DB_USER_CUSTOMER, password=container_config.DB_PASS_CUSTOMER, host=container_config.DB_HOST_CUSTOMER, port=container_config.DB_PORT_CUSTOMER)
conn_shop = psycopg2.connect(dbname=container_config.DB_NAME_SHOP, user=container_config.DB_USER_SHOP, password=container_config.DB_PASS_SHOP, host=container_config.DB_HOST_SHOP, port=container_config.DB_PORT_SHOP)
conn_shipping = psycopg2.connect(dbname=container_config.DB_NAME_SHIPPING, user=container_config.DB_USER_SHIPPING, password=container_config.DB_PASS_SHIPPING, host=container_config.DB_HOST_SHIPPING, port=container_config.DB_PORT_SHIPPING)


cur_customer = conn_customer.cursor()
cur_customer.execute("CREATE TABLE IF NOT EXISTS Customer  (id int, name varchar (50), account int check (account > 0));")
conn_customer.commit()
cur_customer.close()

cur_shop = conn_shop.cursor()
cur_shop.execute("CREATE TABLE IF NOT EXISTS Wine  (Id int, WineName varchar (50), price int);")
conn_shop.commit()
cur_shop.close()

cur_shipping = conn_shipping.cursor()
cur_shipping.execute("CREATE TABLE IF NOT EXISTS Shipping  (Id int, Quantity int);")
conn_shipping.commit()
cur_shipping.close()



###############################################
# #
#
id = 1
ACCOUNT = 100
while ACCOUNT > -100:
    try:
        cur_customer = conn_customer.cursor()
        cur_customer.execute(
            "BEGIN TRANSACTION;"
            "Insert into Customer (id,name,account) VALUES (%s, %s, %s);", (id, "Petro", ACCOUNT)
        )
        cur_customer.execute("PREPARE TRANSACTION 'Customer';")

        cur_shop = conn_shop.cursor()
        cur_shop.execute(
            "BEGIN TRANSACTION;"
            "Insert into Wine (id,WineName,price) VALUES (%s, %s, %s);", (id, "Red", '10')
        )
        cur_shop.execute("PREPARE TRANSACTION 'Shop';")

        cur_shipping = conn_shipping.cursor()
        cur_shipping.execute("BEGIN TRANSACTION;"
                            "Insert into Shipping (id,Quantity) VALUES (%s, %s);", (id, '1')
        )
        cur_shipping.execute("PREPARE TRANSACTION 'shipping';")

    except:

        cur_customer.execute('Rollback;')
        conn_customer.commit()
        #
        cur_shop.execute('Rollback;')
        conn_shop.commit()
        # #
        cur_shipping.execute('Rollback;')
        conn_shipping.commit()
    else:

        cur_customer.execute("COMMIT PREPARED 'Customer';")
        conn_customer.commit()
        #
        cur_shop.execute("COMMIT PREPARED 'Shop';")
        conn_shop.commit()
        # #
        cur_shipping.execute("COMMIT PREPARED 'shipping';")
        conn_shipping.commit()

    ACCOUNT = ACCOUNT-10
    id += 1

print(ACCOUNT)