import MySQLdb, os, tarfile
from urllib2 import urlopen, URLError, HTTPError

# SET VARIABLES 
wordpress = 'http://wordpress.org/latest'

# Connect to MySQL database
db_connection = MySQLdb.connect(host='localhost', user='root')

# Variable to execute database calls with MySQL
cursor = db_connection.cursor()

# Enter folder name for WordPress Install 
print "Enter folder name for local site install: "
folder = raw_input("> ")
dest_folder = '/var/www/html/'+folder

# Save user input for database name into variable
print "New database name: "
db_name = raw_input("> ")

# Save user input for database user name into variable
print "Enter database user: "
db_user = raw_input("> ")

# Save user created password into variable
print "Enter user's password: "
db_pass = raw_input("> ")

# create database with MySQL query
create_db = "CREATE DATABASE IF NOT EXISTS %s" % db_name
cursor.execute(create_db)

# Create database user with MySQL query
granting = "grant usage on *.* to %s@localhost identified by '%s'" % (db_user, db_pass)
cursor.execute(granting) 

# Add user to newly created database
add_user_to_db = "grant all privileges on %s.* to %s@localhost" % (db_name, db_user)
cursor.execute(add_user_to_db)

def dlfile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "Downloading WordPress..."

        # Open our local file for writing
        with open(os.path.basename(url+'.tar.gz'), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url



# Initialize WordPress Download
zippedwp = dlfile(wordpress) 

# Open tar.gz file with TarFile module
tfile = tarfile.open('latest.tar.gz', 'r:gz')

# Extract all contents to the destination folder
tfile.extractall(dest_folder)

# Close the file 
tfile.close()

# Move contents up one diretory, out of WordPress Folder
os.system('mv '+dest_folder+'/wordpress/* '+dest_folder+'/.')

# Delete the now empty WordPress Folder
os.system('rm -r -f '+dest_folder+'/wordpress')

# Git Install SASSnasty starter theme
os.system('git clone git@bitbucket.org:buildcreatestudios/sassnasty.git ' +dest_folder+'/wp-content/themes/'+folder+'')

# Open up stock WP Config Sample file
wpconfig = open(dest_folder+'/wp-config-sample.php')

# Open up new file for new WP Config  
new_wp_config = open(dest_folder+'/wp-config.php', 'wb') 

# Loop through each line in original wp-config-sample and change the necessary lines, and print each line
for line in wpconfig:
	if "define('DB_NAME', 'database_name_here');" in line:
		line = "define('DB_NAME', '%s');" % db_name
	elif "define('DB_USER', 'username_here');" in line: 
		line = "define('DB_USER', '%s');" % db_user
	elif "define('DB_PASSWORD', 'password_here');" in line :
		line = "define('DB_PASSWORD', '%s');" % db_pass
	new_wp_config.write(line)

# Close out both files 
wpconfig.close()
new_wp_config.close() 