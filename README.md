# PyMage

Magento UI testing with Python and Selenium along with the Python UnitTest
library.

This is mostly for me to experiment with Selenium and document some different
ways of doing things.

These tests run against a local network  web server running a default install
of Magento Community Edition v2.4.2. At present the average time per test is
around three to five seconds in this environment. Each test case is
self-contained, meaning that any dependency on system state is set within the
test case and does not depend on the result of any previous test - i.e. each
test could be run individually.

The currently implemented tests are:
- Log In
- Log Out
- Change Password
- Create Account
- Add to Cart
- Edit Cart Quantity
- Apply a Valid Coupon Code
- Apply an Invalid Coupon Code
- Proceed from Cart to Checkout
- Remove Product from Cart
- Check Footer Links Column A
- Check Footer Links Column B
- Navigate to Login Page
- Navigate to Create Account Page
- Sign up for Newsletter

Over time I will add to the tests and improve test handling/execution as well
as reporting of test results.
