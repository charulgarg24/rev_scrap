from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
## urlopen is library which is available inside urllib.request
from urllib.request import urlopen as uReq

app = Flask(__name__) ## creating object of flask

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin() ## it is not required for local execution system it is required when u r going to deploy ur programm on clopuid platform
## we don't know the location of deployment bca cloud server is deploy on different locastion
## it will help to accesxss our url from different locastion
def homePage():
    return render_template("index.html") ## this is justr to showcase my pages
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
## when we hit review in index .html then it will hit above method
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            ## beloow code says that try to extract the content part of the form(index.html)
            ## this replace means if by misatake ur input havce mistake then it will replace spaces to no spaces
            searchString = request.form['content'].replace(" ","")
            ## in below code we are appending the avobe ciode with flipkaret base url
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString## here we have created a variable
            uClient = uReq(flipkart_url)## it will ping to that flipkart url and we will reach to that particular url
            flipkartPage = uClient.read() ## by this we will reach to the page after searching our product it contain view source code of that page
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0] ## hrre we are trying to pull out one of these boxes
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']## here is the base url and then we are trying to append something
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            filename = searchString + ".csv" ## here we are trying to create searchString.csv file
            fw = open(filename, "w") # HERE WE ARE OPENING THAT FILE IN writing mode
            headers = "Product, Customer Name, Rating, Heading, Comment \n" ## we are trying to create header of that file
            fw.write(headers)# in this we are writing header
            reviews = [] # it is the empty list that we have created for pzarticular reviews
            for commentbox in commentboxes: ## we are applying for every sinlge comment in many comments
                try:
                    #name.encode(encoding='utf-8')
                    ## below will basically tell name of the person who gave rating
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text ## we are trying to find paragraph,and inside a pragraph we are trying to find specificn 2 classes

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text ## it will give the rating


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text ## it will basically tell the comment

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text## it wil basically tells the comments without div tags
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} ## here we will have my all thing rating name and comments adn reviews
                reviews.append(mydict) ## appending dictionary to reviews
                ## below code we are again callling rendor_template means try to showcase somehting in web[age
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
