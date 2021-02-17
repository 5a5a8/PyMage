# PyMage

Magento UI testing with Python and Selenium along with the Python UnitTest
library.

This is mostly for me to experiment with Selenium and document some different
ways of doing things.

These tests run against a local web server running a default install of Magento
Community Edition v2.4.2. At present the average time per test is around three
seconds in this environment.

The currently implemented tests are:
- Log In
- Create Account
- Add to Cart
- Edit Cart Quantity
- Apply a Valid Coupon Code
- Apply an Invalid Coupon Code
- Proceed from Cart to Checkout
- Remove Product from Cart

Over time I will add to the tests and improve test handling/execution as well
as reporting of test results.
