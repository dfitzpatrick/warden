from warden.scripts import Script

script_meta = [
	#Display
	Script("crtScripts\Display\KeyIndicator.py",
		categories = ['Display'],
		name = "Key Indicator",
		requires_date_range = False),

	Script("crtScripts\Display\CouponRedemption-Display-DateRange.py",
		categories = ['Display', 'Retrieve'],
		name = "Coupon Redemption Report",
		requires_date_range = True),


	#Retrieve
	Script("crtScripts\Retrieve\Exceptions-OrderEdits-Retrieve-DateRange.py",
		categories = ['Retrieve'],
		name = "Order Edit Report for Utility Script",
		requires_date_range = True),

	Script("crtScripts\Retrieve\TargetInventory-DateRange.py",
		categories = ['Retrieve'],
		name = "Target Inventory Report",
		requires_date_range = True,
		retrieve_file_name = "INVTAR.rtf"),

	Script("crtScripts\Retrieve\TimeClock-Retrieve-DateRange.py",
		categories = ['Retrieve'],
		name = "Time Clock Report",
		requires_date_range = True),

	#Utility
	Script("crtScripts\Utility\inventory\inventory.py",
		categories = ['Utility'],
		name = "Target Inventory Flash View",
		requires_date_range = False)
			 ]

