from oauthentication.contrib.google import views as google


class LoginView(google.LoginView):
    googleapps_domain = None
    
    def get_googleapps_domain(self):
        if self.googleapps_domain:
            domain = self.googleapps_domain
        elif 'hd' in self.request.GET:
            domain = self.request.GET.get('hd')
        else:
            domain = None
        return domain
        
    def get_oauth2_authorization_parameters(self):
        params = super(LoginView, self).get_oauth2_authorization_parameters()
        domain = self.get_googleapps_domain()
        if domain:
            params.update({
                'hd': domain,
            })
        return params
        

class AuthenticationView(google.AuthenticationView):
    pass
