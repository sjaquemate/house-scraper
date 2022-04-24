import app 

def test_driver_with_pararius():
    result = app.get_leiden_pararius_page_source(1, app.get_local_chrome_driver)
    print( result )
        