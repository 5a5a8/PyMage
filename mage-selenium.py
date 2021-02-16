import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GlobalVariable:
	timeout = 30
	domain = "192.168.20.11"
	site_url = "http://" + domain + "/"
	login_url = site_url + "customer/account/login"
	create_account_url = site_url + "customer/account/create"
	login_username = "xormapmap@protonmail.com"
	login_password = "password123#"
	first_name = "xor"
	last_name = "mapmap"
	product_url = site_url + "fusion-backpack.html"
	cart_url = site_url + "checkout/cart"

class Account(unittest.TestCase):
	#login objects
	obj_username_form = "input#email.input-text"
	obj_password_form = "input#pass.input-text"
	obj_login_button = "button#send2.action.login.primary"
	obj_login_success = "span.logged-in"

	#create account objects
	obj_first_name = "input#firstname.input-text.required-entry"
	obj_last_name = "input#lastname.input-text.required-entry"
	obj_email_form = "input#email_address.input-text"
	obj_passwd = "input#password.input-text"
	obj_conf_passwd = "input#password-confirmation.input-text"
	obj_create_button = "button.action.submit.primary"
	obj_success_msg = "div.message-success.success.message"


	#this runs before every class, so all tests in this class use the same
	#browser session
	@classmethod
	def setUpClass(inst):
		inst.driver = webdriver.Firefox()
		inst.driver.implicitly_wait(GlobalVariable.timeout)
		inst.driver.maximize_window()

	#but we make sure to clear cookies before each test. if a test needs
	#a certain cookie state, we can set them in that test
	def setUp(self):
		self.driver.delete_all_cookies()

	#TODO we would have a separate test on homepage to verify create account
	#page and login page could be accessed from there
	def test_login(self):
		#go to login url
		self.driver.get(GlobalVariable.login_url)

		#input email
		email_input = self.driver.find_element_by_css_selector(self.obj_username_form)
		email_input.send_keys(GlobalVariable.login_username)

		#input password
		pass_input = self.driver.find_element_by_css_selector(self.obj_password_form)
		pass_input.send_keys(GlobalVariable.login_password)

		#click login button
		login_click = self.driver.find_element_by_css_selector(self.obj_login_button)
		login_click.click()

		#verify user sees logged in status in header
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_login_success)

	def test_create_account(self):
		#create unique username
		unique_email = GlobalVariable.first_name + \
						GlobalVariable.last_name + \
						str(time.time()) + \
						"@protonmail.com"

		#navigate to sign up page
		self.driver.get(GlobalVariable.create_account_url)
		
		#input first and last names
		self.driver.implicitly_wait(GlobalVariable.timeout)
		input_fn = self.driver.find_element_by_css_selector(self.obj_first_name)
		input_fn.send_keys(GlobalVariable.first_name)
		input_ln = self.driver.find_element_by_css_selector(self.obj_last_name)
		input_ln.send_keys(GlobalVariable.last_name)

		#input email
		input_email = self.driver.find_element_by_css_selector(self.obj_email_form)
		input_email.send_keys(unique_email)

		#input password and confirm password
		input_pass = self.driver.find_element_by_css_selector(self.obj_passwd)
		input_pass.send_keys(GlobalVariable.login_password)
		input_confpass = self.driver.find_element_by_css_selector(self.obj_conf_passwd)
		input_confpass.send_keys(GlobalVariable.login_password)

		#click sign up button
		btn_signup = self.driver.find_element_by_css_selector(self.obj_create_button)
		btn_signup.click()

		#wait for success
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_success_msg)

	@classmethod
	def tearDownClass(inst):
		inst.driver.quit()

class Cart(unittest.TestCase):
	obj_add_cart = "button#product-addtocart-button.action.primary.tocart"
	obj_add_success = "div.message-success.success.message"
	obj_qty = "input.input-text.qty"
	obj_update_cart = "button.action.update"
	obj_delete_cart = "a.action.action-delete"
	obj_cart_empty = "div.cart-empty"
	obj_minicart_count = "span.counter-number"
	obj_proceed_checkout = "button.action.primary.checkout"

	@classmethod
	def setUpClass(inst):
		inst.driver = webdriver.Firefox()
		inst.driver.implicitly_wait(GlobalVariable.timeout)
		inst.driver.maximize_window()

	def setUp(self):
		#self.driver.delete_all_cookies()
		pass

	def test_add_to_cart(self):
		#navigate to test product page
		self.driver.get(GlobalVariable.product_url)
		self.driver.implicitly_wait(GlobalVariable.timeout)

		#click add to cart
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, self.obj_add_cart))
		)
		addcart_btn = self.driver.find_element_by_css_selector(self.obj_add_cart)
		addcart_btn.click()

		#wait for success message
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_add_success)

	#TODO set cart via API and clear cookies between tests
	def test_edit_cart_qty(self):
		self.driver.get(GlobalVariable.cart_url)
		
		#update qty field
		input_qty = self.driver.find_element_by_css_selector(self.obj_qty)
		input_qty.send_keys("2")

		#click update cart button
		btn_update = self.driver.find_element_by_css_selector(self.obj_update_cart)
		btn_update.click()

		#wait for visibility in minicart icon
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_proceed_checkout)

	def test_remove_from_cart(self):
		self.driver.get(GlobalVariable.cart_url)

		#wait for loading to finish
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, self.obj_proceed_checkout))
		)

		#self.driver.implicitly_wait(GlobalVariable.timeout)
		#self.driver.find_element_by_css_selector(self.proceed_checkout)

		#click remove from cart button
		btn_remove = self.driver.find_element_by_css_selector(self.obj_delete_cart)
		btn_remove.click()

		#wait for remove success
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_cart_empty)

	@classmethod
	def tearDownClass(inst):
		inst.driver.quit()
		
if __name__ == "__main__":
	unittest.main()
