# Take5_download

This is a simple piece of code to automatically download the SPOT-Take5 products provided by Theia land data center : https://spot-take5.org. 

This code was written thanks to the precious help of one my colleague at CNES [Jérôme Gasperi](https://www.linkedin.com/pulse/rocket-earth-your-pocket-gasperi-jerome) who developped the "rocket" interface which is used by Theia, and the mechanism to get a token.

This code relies on python 2.7 and on the curl utility. Because of that, I guess it only works with linux.

## Examples
This software is still quite basic, but if you have an account at theia, you may download products using command lines like 

- `python ./take5_download.py -s 'ToulouseFrance' -a auth_theia.txt -c SPOT5 -d 2015-04-01 -f 2015-05-01 -l LEVEL2A`

 which downloads all the SPOT5 (Take5), LEVEL2A products above ToulouseFrance site, acquired in April 2015.

 - `python ./take5_download.py -s 'ToulouseFrance' -a auth_theia.txt -c SPOT5`

 which downloads all the SPOT5 (Take5), LEVEL1C products above ToulouseFrance site.


##Authentification 

The file auth_theia.txt must contain your email address and your password on the same line, such as follows :
`your.email@address.fr top_secret`

The program first fetches a token using your email address and password, and then uses it to download the products. As the token is only valid for two hours, itis advised to request only a reasonable number of products. 

