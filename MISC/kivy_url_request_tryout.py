import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest


class MyApp(App):

    def print_result(self,args,result):
        return print(self.req.result)

    def build(self):
        self.req = UrlRequest("http://localhost:8081/webapi/theme_concept/themes",on_success=self.print_result)
        return Label(text='Get Url')

if __name__ == '__main__':
    MyApp().run()

#
#
# class MainApp(App):
#
#     def get_url(self,url):
#         req = UrlRequest(url)
#         return print(req.result)
#
#     def build(self):
#
# MainApp().run()
# req = UrlRequest("postman-echo.com/get")
#
# def got_json(req, result):
#     for key, value in result['headers'].items():
#         print('{}: {}'.format(key, value))

# def print_succes():
#     print("succes!")
#
# def print_fail():
#     print("failed!")


# , on_success, on_redirect, on_failure, on_error,
#                  on_progress, req_body, req_headers, chunk_size,
#                  timeout, method, decode, debug, file_path, ca_file,
#                  verify)
