# vor dem Ausführen aus dem GIT repository den app Ordner aus dem MVP kopieren und im eigenen, neuen MVP einfügen
# rename old project folder if existent
mv app app2


# create MindMeld blueprint
mindmeld blueprint template app

# copy files from old project folder to new one
cp -R ./app2/* ./app/

# remove old project files
rm -r app2