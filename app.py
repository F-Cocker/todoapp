from website import create_app

#The website folder is used as a module to define the create_app function
#This helps to separate the purposes of each file and make code more readable
#The app file's only purpose is to run the function and launch the website

if __name__=="__main__":
    app=create_app()
    app.run(debug=True, port=8000)