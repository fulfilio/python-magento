Magento Python API
==================

Python library to connect to Magento Webservices.

Usage
-----

.. code-block:: python

    import magento

    url = 'http://domain.com/'
    apiuser = 'user'
    apipass = 'password'

    # Create an instance of API
    client = magento.API(url, apiuser, apipass)

    # A filter expression as dictionary. 
    order_filter = {'created_at':{'from':'2011-09-15 00:00:00'}}
    products = client.product.list(order_filter)

    # Get a list of product types
    product_types = client.product_types.list()
        
    # Get a specific product
    sku = 'prod1'
    product = client.product.info(sku)

    # Add comment to an order
    order_increment_id = '100000001 '
    status = 'canceled'
    client.order.addcomment(order_increment_id, status)


All available APIs
-------------------

* Cart (`client.cart`)
* CartCoupon (`client.cart_coupon`)
* CartCustomer (`client.cart_customer`)
* CartPayment (`client.cart_payment`)
* CartProduct (`client.cart_product`)
* CartShipping (`client.cart_shipping`)
* Category (`client.category`)
* CategoryAttribute (`client.category_attribute`)
* Country (`client.country`)
* CreditMemo (`client.credit_memo`)
* Customer (`client.customer`)
* CustomerAddress (`client.customer_address`)
* CustomerGroup (`client.customer_group`)
* Inventory (`client.inventory`)
* Invoice (`client.invoice`)
* Magento (`client.magento`)
* Order (`client.order`)
* Product (`client.product`)
* ProductAttribute (`client.product_attribute`)
* ProductAttributeSet (`client.product_attribute_set`)
* ProductConfigurable (`client.product_configurable`)
* ProductImages (`client.product_images`)
* ProductLinks (`client.product_links`)
* ProductTierPrice (`client.product_tier_price`)
* ProductTypes (`client.product_types`)
* Region (`client.region`)
* Shipment (`client.shipment`)
* Store (`client.store`)

Old deprecated example
----------------------

The API was originally written with the requirement to call APIs
individually with all the credentials. This led to very verbose code and a
lot of repitition. While the behavior has not been deprecated, it is
recommended to write all new code with the pattern shown in the above
example.

.. code-block:: python

    import magento

    url = 'http://domain.com/'
    apiuser = 'user'
    apipass = 'password'

    with magento.Order(url, apiuser, apipass) as order_api:
        order_increment_id = '100000001 '
        status = 'canceled'
        order_api.addcomment(order_increment_id, status)

    with magento.Store(url, apiuser, apipass) as store_api:
        store_id = '1'
        store_view_info = store_api.info(store_id)
        store_views = store_api.list()

     with magento.Magento(url, apiuser, apipass) as magento_api:
        magento_info = magento_api.info()


Calling custom classes from your own API extensions
---------------------------------------------------

You can ddirectly invoke the underlying `call` method
to make calls directly.

.. code-block:: python

    result = client.call('custom_model.list', [])


Alternatively, you can also build sub classes of API to have
a more pythonic structure. The subclasses are automatically
registered with API when classes are created. 

To ensure that they are registered before you create the first API
instance, always have all your imports on the top of your magento module.

.. code-block:: python

    class CustomModel(API):
        def list(self):
            return self.call('custom_model.list', [])

which would be automatically registered as `custom_model` by the API
metaclass. So you can now use

.. code-block:: python

    import magento
    from my_custom_module import CustomModel

    url = 'http://domain.com/'
    apiuser = 'user'
    apipass = 'password'

    # Create an instance of API
    client = magento.API(url, apiuser, apipass)
    
    client.custom_model.list()


License
-------

BSD 3-Clause

See LICENSE for more details
