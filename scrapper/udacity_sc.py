import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.udacity.com/courses/all")
browser.select_form("#userSearchForm")

print(browser.get_current_form().__dict__)

browser["form"] = "vr"
browser.submit_selected()
print(browser.get_current_page())



'''file = open("page", "w")
file.write(str(browser.get_current_page()))'''