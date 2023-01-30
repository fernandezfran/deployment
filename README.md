# deployment

in this branch we use our developed classification model and deploy an 
application with FastAPI

## simple instructions to run with tox

+ to test the application run `tox -e test_app`
+ and to run it `tox -e run_app`

note that you have to make sure that the model is installed in the virtual 
environment (line commented in the requirements as it is not loaded in PyPI) of 
tox
