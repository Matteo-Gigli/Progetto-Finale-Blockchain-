from django.contrib.auth.mixins import UserPassesTestMixin


'''Definition for 'UserPassesTestMixin'

'Deny a request with a permission error if the test_func() method returns False'

From the documentation we can use the default test_func to specified who is an Admin
We can come back to our app/views.py'''

class StaffMixins(UserPassesTestMixin):


    def test_func(self):
        return self.request.user.is_staff