import unittest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GlobalVariable:
	timeout = 10
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
	account_url = site_url + "customer/account"
	changepass_url = account_url + "/edit/changepass/1/"


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

	def wait_for_js_jq(driver):
		#wait for javascript and jquery to finish loading
		elapsed = 0
		while True:
			if Utilities.wait_for_js(driver) and Utilities.wait_for_jquery(driver):
				break
			if elapsed > GlobalVariable.timeout:
				raise TimeoutError
			time.sleep(0.1)
			elapsed += 0.1
			
	
	#for when all else fails
	def click_with_js(driver, element):
		driver.execute_script("arguments[0].click();", element)
		

class Tests(unittest.TestCase):
	obj_promo_expand = "div#block-discount.block.discount"
	obj_promo_button = "button.action.apply.primary"
	obj_promo_input = "input#coupon_code.input-text"
	obj_proceed_checkout = "button.action.primary.checkout"
	obj_minicart_count = "span.counter-number"
	obj_err_msg = "div.message-error.error.message"
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


	def test_login(self):
		obj_username_form = "input#email.input-text"
		obj_password_form = "input#pass.input-text"
		obj_login_button = "button#send2.action.login.primary"
		obj_login_success = "span.logged-in"
		obj_dashboard = "div.block.block-dashboard-info"

		passwd = GlobalVariable.login_password

		#magento loves to give invalid form key errors on login
		#if this happens, try again 
		for i in range(3):
			#in case the changepass test case fails to revert the password
			if i == 2:
				passwd = passwd + "new"

			#go to login url
			self.driver.get(GlobalVariable.login_url)

			#input email
			email_input = self.driver.find_element_by_css_selector(obj_username_form)
			email_input.send_keys(GlobalVariable.login_username)

			#input password
			pass_input = self.driver.find_element_by_css_selector(obj_password_form)
			pass_input.send_keys(passwd)

			#click login button
			login_click = self.driver.find_element_by_css_selector(obj_login_button)
			login_click.click()

			self.driver.get(GlobalVariable.account_url)
			try:
				self.driver.implicitly_wait(GlobalVariable.timeout)
				self.driver.find_element_by_css_selector(obj_dashboard)
			except:
				continue
			else:
				return
		
		#if loop finishes with no success msg, fail the test
		self.fail(msg="Loop completed with no success message seen")

	
	def test_logout(self):
		obj_dropdown_btn = "button.action.switch"
		obj_signout = "li.link.authorization-link>a[href*='/customer/account/logout/']"
		obj_welcome = "li.greet.welcome>span.logged-in"

		#login precondition
		self.test_login()

		#unfortunately I can't get anything else to work here for waiting
		#for the menu to load
		time.sleep(1)

		#click dropdown menu
		btn_dropdown = self.driver.find_element_by_css_selector(obj_dropdown_btn)
		Utilities.click_with_js(self.driver, btn_dropdown)

		#click signout button
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, obj_signout))
		)
		btn_signout = self.driver.find_element_by_css_selector(obj_signout)
		btn_signout.click()

		#if success, navigating to account dashboard will go to login page
		self.driver.get(GlobalVariable.account_url)
		cur_url = self.driver.current_url
		assert '/login/' in cur_url


	def test_create_account(self):
		obj_first_name = "input#firstname.input-text.required-entry"
		obj_last_name = "input#lastname.input-text.required-entry"
		obj_email_form = "input#email_address.input-text"
		obj_passwd = "input#password.input-text"
		obj_conf_passwd = "input#password-confirmation.input-text"
		obj_create_button = "button.action.submit.primary"
		obj_success_msg = "div.message-success.success.message"

		#create unique username
		unique_email = GlobalVariable.first_name + \
						GlobalVariable.last_name + \
						str(time.time()) + \
						"@protonmail.com"

		#try up to 3 times in case of magento's famous invalid form key error
		for i in range(3):
			#navigate to sign up page
			self.driver.get(GlobalVariable.create_account_url)
			
			WebDriverWait(self.driver, GlobalVariable.timeout).until(
				EC.visibility_of_element_located((By.CSS_SELECTOR, obj_first_name))
			)

			#input first and last names
			self.driver.implicitly_wait(GlobalVariable.timeout)
			input_fn = self.driver.find_element_by_css_selector(obj_first_name)
			input_fn.send_keys(GlobalVariable.first_name)
			input_ln = self.driver.find_element_by_css_selector(obj_last_name)
			input_ln.send_keys(GlobalVariable.last_name)

			#input email
			input_email = self.driver.find_element_by_css_selector(obj_email_form)
			input_email.send_keys(unique_email)

			#input password and confirm password
			input_pass = self.driver.find_element_by_css_selector(obj_passwd)
			input_pass.send_keys(GlobalVariable.login_password)
			input_confpass = self.driver.find_element_by_css_selector(obj_conf_passwd)
			input_confpass.send_keys(GlobalVariable.login_password)

			#click sign up button
			btn_signup = self.driver.find_element_by_css_selector(obj_create_button)
			btn_signup.click()

			#wait for success msg
			try:
				self.driver.implicitly_wait(GlobalVariable.timeout)
				self.driver.find_element_by_css_selector(obj_success_msg)
			except:
				continue
			else:
				return

			self.fail(msg="Loop completed with no success message seen")


	def test_add_to_cart(self):
		obj_add_cart = "button#product-addtocart-button.action.primary.tocart"
		obj_add_success = "div.message-success.success.message"

		#navigate to test product page
		self.driver.get(GlobalVariable.product_url)
		self.driver.implicitly_wait(GlobalVariable.timeout)

		#click add to cart
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, obj_add_cart))
		)
		addcart_btn = self.driver.find_element_by_css_selector(obj_add_cart)
		addcart_btn.click()

		#wait for success message
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_add_success)


	def test_edit_cart_qty(self):
		obj_qty = "input.input-text.qty"
		obj_update_cart = "button.action.update"

		self.test_add_to_cart()
		self.driver.get(GlobalVariable.cart_url)
		
		#update qty field
		input_qty = self.driver.find_element_by_css_selector(obj_qty)
		input_qty.send_keys("2")

		#click update cart button
		btn_update = self.driver.find_element_by_css_selector(obj_update_cart)
		btn_update.click()

		#wait for visibility in minicart icon
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_proceed_checkout)

	def test_proceed_to_checkout(self):
		obj_ship_page = "li#shipping.checkout-shipping-address"

		self.test_add_to_cart()
		self.driver.get(GlobalVariable.cart_url)

		#wait for cart to load fully
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, self.obj_minicart_count))
		)

		Utilities.wait_for_js_jq(self.driver)
		
		#click proceed to checkout button
		proceed = self.driver.find_element_by_css_selector(self.obj_proceed_checkout)
		Utilities.click_with_js(self.driver, proceed)

		#verify shipping info visible
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_ship_page)


	def test_apply_invalid_promo_code(self):
		obj_promo_err = "div.message-error.error.message"

		self.test_add_to_cart()
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
		self.driver.find_element_by_css_selector(obj_promo_err)

	def test_apply_valid_promo_code(self):
		obj_promo_success = "div.message-success.success.message"

		self.test_add_to_cart()
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
		self.driver.find_element_by_css_selector(obj_promo_success)

	
	def test_remove_from_cart(self): 
		obj_delete_cart = "a.action.action-delete"
		obj_cart_empty = "div.cart-empty"

		self.test_add_to_cart()
		self.driver.get(GlobalVariable.cart_url)

		#wait for loading to finish
		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, self.obj_proceed_checkout))
		)

		Utilities.wait_for_js_jq(self.driver)

		#click remove from cart button
		btn_remove = self.driver.find_element_by_css_selector(obj_delete_cart)
		btn_remove.click()

		#wait for remove success
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_cart_empty)

	def test_nav_to_login(self):
		obj_login_button = "li.link.authorization-link"
		obj_login_verify = "input#pass.input-text"

		self.test_add_to_cart()

		#click login button
		self.driver.get(GlobalVariable.site_url)
		btn_login = self.driver.find_element_by_css_selector(obj_login_button)

		#verify login page visible
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_login_verify)

	def test_nav_create_account(self):
		obj_create_button = "a[href*='/customer/account/create/']"
		obj_create_verify = "input#password-confirmation.input-text"

		self.driver.get(GlobalVariable.site_url)
		create_btn = self.driver.find_element_by_css_selector(obj_create_button)
		create_btn.click()

		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_create_verify)

	def test_footer_column_A(self):
		obj_about_us = "li.nav.item>a[href*='/about-us/']"
		obj_customer_service = "li.nav.item>a[href*='/customer-service/']"
		obj_not404_aboutus = "p.cms-content-important"
		obj_not404_cservice = "div.cms-content-important"

		self.driver.get(GlobalVariable.site_url)

		#check about-us link
		btn_about_us = self.driver.find_element_by_css_selector(obj_about_us)
		btn_about_us.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_aboutus)

		#check customer service link
		btn_customer_service = self.driver.find_element_by_css_selector(obj_customer_service)
		btn_customer_service.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_cservice)
	
	def test_footer_column_B(self):
		obj_search_terms = "li.nav.item>a[href*='/search/term/popular/']"
		obj_not404_search = "li#term-1.item"

		obj_privacy_policy = "li.nav.item>a[href*='privacy-policy-cookie-restriction-mode']"
		obj_not404_privacy = "h2#privacy-policy-title-2"

		obj_advanced_search = "li.nav.item>a[href*='/catalogsearch/advanced/']"
		obj_not404_advanced = "input#sku.input-text"

		obj_contactus = "li.nav.item>a[href*='/contact/']"
		obj_not404_contact = "textarea#comment.input-text"

		self.driver.get(GlobalVariable.site_url)

		#check search terms link
		btn_searchterms = self.driver.find_element_by_css_selector(obj_search_terms)
		btn_searchterms.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_search)

		#check privacy policy link
		btn_privacy = self.driver.find_element_by_css_selector(obj_privacy_policy)
		btn_privacy.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_privacy)

		#check advanced search link
		btn_advanced = self.driver.find_element_by_css_selector(obj_advanced_search)
		btn_advanced.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_advanced)
		
		#check contact us link
		btn_contact = self.driver.find_element_by_css_selector(obj_contactus)
		btn_contact.click()
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(obj_not404_contact)

	def test_change_password(self):
		obj_currentpass = "input#current-password.input-text"
		obj_newpass = "input#password.input-text"
		obj_confpass = "input#password-confirmation.input-text"
		obj_save_btn = "button.action.save.primary"
		obj_signed_out = "button.action.login.primary"

		oldpass = GlobalVariable.login_password
		newpass = oldpass + "new"

		#we change to new password, sign in with new, then revert back to old
		for i in range(2):
			self.test_login()
			self.driver.get(GlobalVariable.changepass_url)

			WebDriverWait(self.driver, GlobalVariable.timeout).until(
				EC.visibility_of_element_located((By.CSS_SELECTOR, obj_currentpass))
			)

			#enter current password
			cur_pass = self.driver.find_element_by_css_selector(obj_currentpass)
			cur_pass.send_keys(oldpass)

			#enter new password
			new_pass = self.driver.find_element_by_css_selector(obj_newpass)
			new_pass.send_keys(newpass)

			#confirm new password
			conf_pass = self.driver.find_element_by_css_selector(obj_confpass)
			conf_pass.send_keys(newpass)

			#click save and verify logged out
			btn_save = self.driver.find_element_by_css_selector(obj_save_btn)
			btn_save.click()
			self.driver.implicitly_wait(GlobalVariable.timeout)
			self.driver.find_element_by_css_selector(obj_signed_out)

			#change global login password so that it now matches new password
			GlobalVariable.login_password = newpass
			oldpass, newpass = newpass, oldpass

	def test_newsletter_subscribe(self):
		obj_newsletter = "input#newsletter"
		obj_submit = "button.action.subscribe.primary"
		obj_pageload = "span.not-logged-in"

		unique_email = GlobalVariable.first_name + \
						GlobalVariable.last_name + \
						str(time.time()) + \
						"@protonmail.com"

		self.driver.get(GlobalVariable.site_url)

		WebDriverWait(self.driver, GlobalVariable.timeout).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, obj_pageload))
		)

		#input email and submit
		input_nl = self.driver.find_element_by_css_selector(obj_newsletter)
		input_nl.send_keys(unique_email)
		btn_submit = self.driver.find_element_by_css_selector(obj_submit)
		btn_submit.click()

		#check for success message
		self.driver.implicitly_wait(GlobalVariable.timeout)
		self.driver.find_element_by_css_selector(self.obj_success_msg)


	@classmethod
	def tearDownClass(inst):
		inst.driver.quit()

if __name__ == "__main__":
	unittest.main()
