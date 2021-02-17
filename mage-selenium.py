import unittest
import time
import requests
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
	coupon_invalid = "invalidcoupon50"
	coupon_valid = "AUTO_TEST_COUPON"


class Utilities:
	def wait_for_js(driver):
		done = driver.execute_script("return document.readyState")
		if str(done) == "complete":
			return True
		else:
			return False

	def wait_for_jquery(driver):
		done = driver.execute_script("return jQuery.active")
		if int(done) == 0:
			return True
		else:
			return False
	
	#for when all else fails
	def click_with_js(driver, element):
		driver.execute_script("arguments[0].click();", element)
		

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
	obj_promo_expand = "div#block-discount.block.discount"
	obj_promo_input = "input#coupon_code.input-text"
	obj_promo_button = "button.action.apply.primary"
	obj_promo_err = "div.message-error.error.message"
	obj_promo_success = "div.message-success.success.message"
	obj_discount = "span.discount-coupon"
	obj_ship_page = "li#shipping.checkout-shipping-address"
	obj_subtotal = "tr.total.sub"

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

	def test_proceed_to_checkout(self):
		self.driver.get(GlobalVariable.cart_url)

		#wait for cart to load fully
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, self.obj_minicart_count))
		)

		#wait for javascript and jquery to finish loading
		elapsed = 0
		while True:
			if Utilities.wait_for_js(self.driver) and Utilities.wait_for_jquery(self.driver):
				break
			if elapsed > GlobalVariable.timeout:
				raise TimeoutError
			time.sleep(0.1)
			elapsed += 0.1
			
		#click proceed to checkout button
		proceed = self.driver.find_element_by_css_selector(self.obj_proceed_checkout)
		Utilities.click_with_js(self.driver, proceed)

		#verify shipping info visible
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_ship_page)


	def test_apply_invalid_promo_code(self):
		self.driver.get(GlobalVariable.cart_url)

		#wait for cart to load fully
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, self.obj_minicart_count))
		)

		#expand promo field
		btn_expand_promo = self.driver.find_element_by_css_selector(self.obj_promo_expand)
		btn_expand_promo.click()

		#input invalid coupon code
		input_coupon = self.driver.find_element_by_css_selector(self.obj_promo_input)
		input_coupon.send_keys(GlobalVariable.coupon_invalid)

		#click apply
		btn_apply = self.driver.find_element_by_css_selector(self.obj_promo_button)
		btn_apply.click()

		#verify error present
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_promo_err)

	def test_apply_valid_promo_code(self):
		self.driver.get(GlobalVariable.cart_url)

		#wait for cart to load fully
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, self.obj_minicart_count))
		)

		#expand promo field
		btn_expand_promo = self.driver.find_element_by_css_selector(self.obj_promo_expand)
		btn_expand_promo.click()

		#input valid coupon code
		input_coupon = self.driver.find_element_by_css_selector(self.obj_promo_input)
		input_coupon.send_keys(GlobalVariable.coupon_valid)

		#click apply
		btn_apply = self.driver.find_element_by_css_selector(self.obj_promo_button)
		btn_apply.click()

		#verify success msg present
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_promo_success)

	
	def test_remove_from_cart(self):
		self.driver.get(GlobalVariable.cart_url)

		#wait for loading to finish
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, self.obj_proceed_checkout))
		)

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
