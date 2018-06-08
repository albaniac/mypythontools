The target of this python script is to verify the price of web site. And in case of one thing change a mail is send.

You need to add the beautifull soup by the following command : pip install beautifulsoup4

The needed entry are needed to the script to work fine :

    "entre" : Informations about the website to survey (put in it 3 parameters : URL of the page / tag HTML for price / tag HTML for name). You can use the file on this git to have an example.
    "mail" : Informations to use to send mail. You can use the file on this git to have an example too.

This script is test for some website and work for my use (bikester.fr, probikeshop.fr, topachat.fr, bikediscount.de), but a lot of thing could be better, for example :

    Manager the HTML tag by website instead URL
    Add to database
    Manage multiples page of a website
    Better format of the mail
    A web page to consult the modification
    Add the URL of the product .....

