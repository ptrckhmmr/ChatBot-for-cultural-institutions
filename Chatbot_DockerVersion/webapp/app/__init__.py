# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from mindmeld import Application
from mindmeld.components import QuestionAnswerer

# suggestions
from fuzzywuzzy import process

# data import
import pandas as pd

import os
app_path = os.path.dirname(__file__)

# setting up knowledge base for query
qa = QuestionAnswerer(app_path)
qa.load_kb('app', 'exhibition', app_path + '/data/exhibition.json')
qa.load_kb('app', 'artists', app_path + '/data/artists.json')
#qa.load_kb('app', 'event', app_path + '/data/event.json')
qa.load_kb('app', 'openinghours', app_path + '/data/openinghours.json')
qa.load_kb('app', 'jokes', app_path + '/data/jokes.json')

# retrieving all suggestions
suggestions = pd.read_csv(app_path + '/data/all_possible_questions.txt',header=None, sep='\n')

#suggestions_exhibition = pd.read_csv(app_path + '/data/all_possible_questions.txt',header=None, sep='\n')

suggestions_exhibition = pd.read_csv(app_path + '/data/all_exhibition_questions.txt',header=None, sep='\n')

app = Application(__name__)

__all__ = ['app']

### Methods used within dialoque states###

def string_current_exhibitions(exhibition):
    from datetime import datetime

    now = datetime.now()
    heute = now.strftime("%Y-%m-%d")

    ausstellung_offen = ''

    for item in exhibition:
        if (item['ende_tag'] > heute):
            ausstellung_offen = ausstellung_offen + item['titel_de'] + ', '

    return ausstellung_offen


def draw_ten_artists_from_current_exhibition(exhibition):
    from datetime import datetime
    now = datetime.now()
    heute = now.strftime("%Y-%m-%d")

    s = qa.build_search(index='exhibition')
    ausstellung_offen = []
    artists_ausstellungen_offen = ''

    for item in exhibition:
        if (item['ende_tag'] > heute):
            ausstellung_offen.append(item['titel_de'])

    for item in ausstellung_offen:
        tmpt = s.query(titel_de=item).execute(size=1)
        artists_ausstellungen_offen = artists_ausstellungen_offen + tmpt[0]['person_freie_rolle'] + ', '
        artists_ausstellungen_offen = artists_ausstellungen_offen + tmpt[0]['person_feste_rolle'] + ', '

    import re
    artists_ausstellungen_offen = re.sub("\(.*?\)", "", artists_ausstellungen_offen)
    artists_ausstellungen_offen = re.sub("not available, ", "", artists_ausstellungen_offen)

    artists_ausstellungen_offen = artists_ausstellungen_offen.split(',')
    artists_ausstellungen_offen = pd.DataFrame(artists_ausstellungen_offen, columns=['Artists Current Exhibitions'])
    artists_ausstellungen_offen = artists_ausstellungen_offen[
        artists_ausstellungen_offen['Artists Current Exhibitions'] != '']
    artists_ausstellungen_offen = artists_ausstellungen_offen.iloc[:-1, :]
    artists_ausstellungen_offen = artists_ausstellungen_offen.sample(n=10)

    artists = ''
    for index, row in artists_ausstellungen_offen.iterrows():
        artists = artists + row['Artists Current Exhibitions'] + ','

    artists = re.sub(" , ", ", ", artists)
    artists = artists[:-1]

    return artists


def filter_regular_expressions(beschreibung):
    import re
    beschreibung = re.sub("<.*?>", "", beschreibung)
    beschreibung = re.sub("&.*?;", "", beschreibung)

    return beschreibung


def filter_drupal(beschreibung):
    import re
    beschreibung = re.sub("\(.*?\)", "", beschreibung)

    return beschreibung


def übermorgen_in_datum():
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    übermorgen = now + timedelta(days=2)
    übermorgen = übermorgen.strftime("%Y-%m-%d")

    return übermorgen


def übermorgen_in_wochentag():
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    übermorgen = now + timedelta(days=2)

    wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tagnummer = übermorgen.weekday()

    return wochentag[tagnummer]


def morgen_in_datum():
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    morgen = now + timedelta(days=1)
    morgen = morgen.strftime("%Y-%m-%d")

    return morgen


def morgen_in_wochentag():
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    morgen = now + timedelta(days=1)

    wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tagnummer = morgen.weekday()

    return wochentag[tagnummer]


def heute_in_wochentag():
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()
    heute = now

    wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tagnummer = heute.weekday()

    return wochentag[tagnummer]


def datum_in_wochentag(entry):
    from datetime import datetime
    from datetime import timedelta

    year = str(datetime.now().year)
    wochentag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    if (entry.find('-') != -1):
        if (entry.count('-') == 1):
            datum = entry + '-' + year
            datum = datetime.strptime(datum, "%d-%m-%Y")
            tagnummer = datum.weekday()

            return wochentag[tagnummer]

        if (entry.count('-') == 2):
            year = str(datetime.now().year)
            datum = entry
            try:
                datum = datetime.strptime(datum, "%d-%m-%Y")
                tagnummer = datum.weekday()

                return wochentag[tagnummer]
            except:
                return 'null'

    elif (entry.find('/') != -1):
        if (entry.count('/') == 1):
            datum = entry + '/' + year
            datum = datetime.strptime(datum, "%d/%m/%Y")
            tagnummer = datum.weekday()

            return wochentag[tagnummer]

        elif (entry.count('/') == 2):
            year = str(datetime.now().year)
            datum = entry
            try:
                datum = datetime.strptime(datum, "%d/%m/%Y")
                tagnummer = datum.weekday()

                return wochentag[tagnummer]
            except:
                return 'null'


    elif (entry.find('.') != -1):
        if (entry.count('.') == 1):
            datum = entry + '.' + year
            try:
                datum = datetime.strptime(datum, "%d.%m.%Y")
                tagnummer = datum.weekday()

                return wochentag[tagnummer]
            except:
                return 'null'

        if (entry.count('.') == 2):
            if (entry[-1] == '.'):
                datum = entry + year
                datum = datetime.strptime(datum, "%d.%m.%Y")
                tagnummer = datum.weekday()
                return wochentag[tagnummer]

            else:
                year = str(datetime.now().year)
                datum = entry
                try:
                    datum = datetime.strptime(datum, "%d.%m.%Y")
                    tagnummer = datum.weekday()

                    return wochentag[tagnummer]
                except:
                    return 'null.'
    else:
        return 'null'


def hasNumbers(inputString):
    import re
    return bool(re.search(r'\d', inputString))


class Entity_memory:
    def __init__(self, name=''):
        self._name = name

        # getter method

    def get_entity(self):
        return self._name

        # setter method

    def set_entity(self, x):
        self._name = x

em = Entity_memory()
em.set_entity('')


#### intents from 'basic' domain ####

@app.handle(intent='greet')
def welcome(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    #responder.frame = {}

    # Respond with a random selection from one of the canned "goodbye" responses.
    responder.reply(['Hallo, ich bin dein persönlicher Chatbot! 😍', 'Hey! Freut mich dich kennenzulernen! 😄'])



@app.handle(intent='how_are_you')
def say_I_am_doing_great(request, responder):

    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    responder.reply(['Bei mir ist alles besten. Ich hoffe, dass bei dir auch alles klar ist! Wie kann ich dir weiterhelfen?', 'Mir geht es super, vielen Dank. Wie kann ich dir weiterhelfen?',
                     'Bei mir ist alles klar. Danke der Nachfrage! Wie kann ich dir weiterhelfen?'])


@app.handle(intent='exit')
def say_goodbye(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    # Respond with a random selection from one of the canned "goodbye" responses.
    responder.reply(['Ciao!', 'Auf Wiedersehen!', 'Adios.', 'Tschüss! Bis zum nächsten Mal!.'])


#### intents from 'zkm' domain ####

@app.handle(intent='zkm_general')
def say_zkm_general(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    beschreibung = 'Das ZKM wurde 1989 von der Stadt Karlsruhe und dem Land Baden-Würtemberg gegründet. Gründungsdirektor Heinrich Klotz formte die Mission des ZKMs, die klassischen Künste ins digitale Zeitalter fortzuschreiben. Die einzigartige Kulturinstitution ist seit 1997 in einem ehemaligen, denkmalgeschützten Industriebau, dem sogenannten Hallenbau A untergebracht, der zu seiner Entstehungszeit einer der architektonisch fortschrittlichsten in Deutschland war. Hier findest du weitere Infos dazu: https://zkm.de/de/das-zkm '

    # Respond
    responder.reply(beschreibung)


@app.handle(intent='zkm_content')
def say_zkm_content(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    beschreibung = 'Es ist ein Haus aller Medien und Gattungen, ein Haus sowohl der raumbasierten Künste wie Malerei, Fotografie und Skulptur als auch der zeitbasierten Künste wie Film, Video, Medienkunst, Musik, Tanz, Theater und Performance.'

    # Respond
    responder.reply(beschreibung)

@app.handle(intent='zkm_cinema')
def say_zkm_cinema(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    beschreibung = 'Anders als viele Menschen denken, ist das ZKM kein Kino. Das Kino, „der Filmpalast am ZKM“ befindet sich neben dem ZKM. Hier findest du das Kinoprogramm: https://www.filmpalast.net. Bei uns im ZKM kannst du allerdings auch sehr viel Spaß haben. Schau doch auch mal bei uns vorbei, wir haben spannende interaktive Ausstellungen und ein sehr nettes Café bei uns. Hier findest du uns: https://zkm.de/de/ueber-das-zkm/kontakte '

    # Respond
    responder.reply(beschreibung)


@app.handle(intent='zkm_journey_car')
def say_zkm_journey_car(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    beschreibung = 'Das ZKM ist mit dem Auto sehr gut zu erreichen. Es befindet sich in der Lorenzstraße 19 in Karlsruhe (https://goo.gl/maps/gdmpM8VNrHyNZmFu5). Im Parkhaus des ZKMs stehen etwa 700 kostenpflichtige Parkplätze zur Verfügung. Zu erreichen ist das Parkhaus »ZKM« über die Südendstraße 44 (https://goo.gl/maps/U983qzbWB3dvE6s89). Für Elektroautos stehen zwei Stromladestationen zur Verfügung. Hier findest du weitere Infos zur Anfahrt mit dem Auto: https://zkm.de/de/ausstellungen-veranstaltungen/anfahrt '

    # Respond
    responder.reply(beschreibung)


@app.handle(intent='zkm_journey_bus')
def say_zkm_journey_bus(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    beschreibung = 'Das ZKM ist mit öffentlichen Verkehrsmitteln sehr gut zu erreichen. Es befindet sich in der Lorenzstraße 19 in Karlsruhe (https://goo.gl/maps/gdmpM8VNrHyNZmFu5). Die Straßenbahn Haltestelle „ZKM“ ist mit der Linie 2 am besten zu erreichen. Aufgrund von Baumaßnahmen kommt es im Raum Karlsruhe zeitweise zu geänderten Fahrtzeiten. Wir bitten Sie, die aktuelle Verkehrslage auf der Webpräsenz des Karlsruher Verkehrsverbunds (KVV) zu überprüfen. Mit dem Bus, fährt man am besten zur Haltestelle „Lorenzstraße – ZKM“. Hierhin fährt die Buslinie 55. Hier findest du weitere Infos zur Anfahrt mit den öffentlichen Verkehrsmitteln: https://zkm.de/de/ausstellungen-veranstaltungen/anfahrt '

    # Respond
    responder.reply(beschreibung)


@app.handle(intent='exhibition_duration')
def say_exhibition_duration(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}



    # textfile = open(app_path + '/entities/exhibition/gazetteer.txt', 'r')
    # zeilen = textfile.readlines()
    # liste = []
    # for item in zeilen:
    #     cleanentry = item.rstrip()
    #     liste.append(cleanentry)
    #
    #
    #
    # exhibition_list = liste
    # responder.params.dynamic_resource['gazetteers'] = {'exhibition': dict((exhibitions, 1.0) for exhibitions in exhibition_list)}

    try:

        # Extract id from query
        id = request.entities[0]['value'][0]['id']

        exhibtion = qa.get(index='exhibition', id=id)

        title = exhibtion[0]['titel_de']
        start = exhibtion[0]['start_tag']
        end = exhibtion[0]['ende_tag']


        response = 'Die Ausstellung ' + title + ' hat von ' + start + ' bis ' + end + ' geöffnet.'

        # Respond
        responder.reply(response)

    except:

        # query = request.text
        #
        # score = process.extractOne(query, suggestions[0])[1]
        # suggestion = process.extractOne(query, suggestions[0])[0]
        # responder.frame['suggestion'] = suggestions[0]
        #
        # if (score > 80):
        #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
        # else:
        response = 'Sorry, das habe ich nicht verstanden.'

        responder.reply(response)



@app.handle(intent='exhibition_description')
def say_exhibition_description(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}



    # textfile = open(app_path + '/entities/exhibition/gazetteer.txt', 'r')
    # zeilen = textfile.readlines()
    # liste = []
    # for item in zeilen:
    #     cleanentry = item.rstrip()
    #     liste.append(cleanentry)
    #
    #
    #
    # exhibition_list = liste
    # responder.params.dynamic_resource['gazetteers'] = {'exhibition': dict((exhibitions, 1.0) for exhibitions in exhibition_list)}

    try:
        # Extract id from query
        id = request.entities[0]['value'][0]['id']

        exhibtion = qa.get(index='exhibition', id=id)

        title = exhibtion[0]['titel_de']
        beschreibung = exhibtion[0]['kurzbeschreibung_seo_de']

        beschreibung = filter_regular_expressions(beschreibung)

        if (beschreibung == 'not available'):
            responder.reply('Leider habe ich keine Informationen zur Ausstellung ' + title + '.')
        else:
            # Respond
            responder.reply(beschreibung)

    except:
        query = request.text

        recommendation = process.extractOne(query, suggestions_exhibition[0])
        score = recommendation[1]
        suggestion = recommendation[0]

        if (score > 90):
            response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion

        else:
            response = 'Sorry, das habe ich nicht verstanden.'

        responder.reply(response)


@app.handle(intent='exhibition_artist')
def say_exhibition_artist(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}


    # textfile = open(app_path + '/entities/exhibition/gazetteer.txt', 'r')
    # zeilen = textfile.readlines()
    # liste = []
    # for item in zeilen:
    #     cleanentry = item.rstrip()
    #     liste.append(cleanentry)
    #
    #
    #
    # exhibition_list = liste
    # responder.params.dynamic_resource['gazetteers'] = {'exhibition': dict((exhibitions, 1.0) for exhibitions in exhibition_list)}

    try:

        # Extract id from query
        id = request.entities[0]['value'][0]['id']

        exhibtion = qa.get(index='exhibition', id=id)

        title = exhibtion[0]['titel_de']
        beschreibung = exhibtion[0]['person_freie_rolle']

        beschreibung = filter_drupal(beschreibung)

        if (beschreibung == 'not available'):
            responder.reply('Leider habe ich keine Informationen zur Ausstellung ' + title + '.')
        else:
            # Respond
            responder.reply('Bei der Ausstellung ' + title + ' haben folgende Künstler mitgewirkt: ' + beschreibung)

    except:

        # query = request.text
        #
        # score = process.extractOne(query, suggestions[0])[1]
        # suggestion = process.extractOne(query, suggestions[0])[0]
        # responder.frame['suggestion'] = suggestions[0]
        #
        # if (score > 80):
        #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
        # else:
        response = 'Sorry, das habe ich nicht verstanden.'

        responder.reply(response)




@app.handle(intent='artist_information')
def say_artist_information(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}


    entity = request.entities
    print(entity)



    if (entity == ()):



        if (em.get_entity() == ''):
            responder.reply('Über welchen Künstler möchstest du mehr wissen?')
            print('Ohne entity IF artist info: Über welchen Künstler möchstest du mehr wissen?')
        else:

            name = em.get_entity()
            print('Name try else')
            print(name)


            try:

                s = qa.build_search(index='artists')
                id = s.filter(name=name).execute()[0]['id']

                print('Ohne entity ELSE artist info')
                    #print(responder.history[0]['request']['intent'])
                    #print(responder.history[0]['request']['entities'][0]['text'])

                artists = qa.get(index='artists', id=id)

                title = artists[0]['name']
                beschreibung = artists[0]['beschreibung_de']

                beschreibung = filter_regular_expressions(beschreibung)

                if (beschreibung == 'not available'):
                    responder.reply('Leider habe ich keine Informationen zu ' + title + '.')
                else:
                    # Respond
                    responder.reply('Hintergrundinformationen zu ' + title + ' : ' + beschreibung)

            except:

                # query = request.text
                #
                # score = process.extractOne(query, suggestions[0])[1]
                # suggestion = process.extractOne(query, suggestions[0])[0]
                # responder.frame['suggestion'] = suggestions[0]
                #
                # if (score > 80):
                #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
                # else:
                response = 'Sorry, das habe ich nicht verstanden.'

                responder.reply(response)


    else:

        em.set_entity(entity[0]['text'])

        print('Mit entity ELSE artist info')
        print(entity[0]['text'])
        print(em.get_entity())



        # textfile = open(app_path + '/entities/artists/gazetteer.txt', 'r')
        # zeilen = textfile.readlines()
        # liste = []
        # for item in zeilen:
        #     cleanentry = item.rstrip()
        #     liste.append(cleanentry)
        #
        #
        #
        # artists_list = liste
        # responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artist, 1.0) for artist in artists_list)}

        #artists_list = ['Torsten Belschner', 'Michael Bielicky', 'Peter Callas']
        #responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artists, 1.0) for artists in artists_list)}

        try:

            # Extract id from query
            id = request.entities[0]['value'][0]['id']

            artists = qa.get(index='artists', id=id)

            title = artists[0]['name']
            beschreibung = artists[0]['beschreibung_de']

            beschreibung = filter_regular_expressions(beschreibung)

            if (beschreibung == 'not available'):
                responder.reply('Leider habe ich keine Informationen zu ' + title + '.')
            else:
                # Respond
               responder.reply('Hintergrundinformationen zu ' + title + ' : ' + beschreibung)




        except:

            # query = request.text
            #
            # score = process.extractOne(query, suggestions[0])[1]
            # suggestion = process.extractOne(query, suggestions[0])[0]
            # responder.frame['suggestion'] = suggestions[0]
            #
            # if (score > 80):
            #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
            # else:
            response = 'Sorry, das habe ich nicht verstanden.'

            responder.reply(response)


    # import pickle
    # # open a file, where you ant to store the data
    # file = open(app_path + '/data/history' + '.pickle', 'wb')
    # # dump information to that file
    # pickle.dump(responder.history, file)
    # # close the file
    # file.close()





@app.handle(intent='artist_birthyear')
def say_artist_birthyear(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}

    entity = request.entities
    # name =  request.entities[0]['text']

    if (entity == ()):

        if (em.get_entity() == ''):
            responder.reply('Von welchem Künstler möchstest du das Geburtsjahr wissen?')
            print('Ohne entity IF artist birthyear: Von welchem Künstler möchstest du das Geburtsjahr wissen?')
        else:

            name = em.get_entity()
            print('Name try else')
            print(name)


            try:

                s = qa.build_search(index='artists')
                id = s.filter(name=name).execute()[0]['id']


                print('Ohne Entity ELSE artist birthyear')
                #print(responder.history[0]['request']['intent'])
                #print(responder.history[0]['request']['entities'][0]['text'])

                artists = qa.get(index='artists', id=id)

                title = artists[0]['name']
                geburtsjahr = artists[0]['born_year']

                if (geburtsjahr == 'not available'):
                    responder.reply('Leider habe ich keine Informationen über das Geburtsjahr von ' + title + '.')
                else:
                    # Respond
                    responder.reply(title + ' ist im Jahr ' + geburtsjahr + ' geboren.')

            except:

                # query = request.text
                #
                # score = process.extractOne(query, suggestions[0])[1]
                # suggestion = process.extractOne(query, suggestions[0])[0]
                # responder.frame['suggestion'] = suggestions[0]
                #
                # if (score > 80):
                #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
                # else:
                response = 'Sorry, das habe ich nicht verstanden.'

                responder.reply(response)



    else:

        em.set_entity(entity[0]['text'])

        print('Mit Entity ELSE artist birthyear')


        # textfile = open(app_path + '/entities/artists/gazetteer.txt', 'r')
        # zeilen = textfile.readlines()
        # liste = []
        # for item in zeilen:
        #     cleanentry = item.rstrip()
        #     liste.append(cleanentry)
        #
        #
        #
        # artists_list = liste
        # responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artist, 1.0) for artist in artists_list)}

        #artists_list = ['Torsten Belschner', 'Michael Bielicky', 'Peter Callas']
        #responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artists, 1.0) for artists in artists_list)}

        try:

            # Extract id from query
            id = request.entities[0]['value'][0]['id']

            artists = qa.get(index='artists', id=id)

            title = artists[0]['name']
            geburtsjahr = artists[0]['born_year']


            if (geburtsjahr == 'not available'):
                responder.reply('Leider habe ich keine Informationen über das Geburtsjahr von ' + title + '.')
            else:
                # Respond
                responder.reply(title + ' ist im Jahr ' + geburtsjahr + ' geboren.')

        except:

            # query = request.text
            #
            # score = process.extractOne(query, suggestions[0])[1]
            # suggestion = process.extractOne(query, suggestions[0])[0]
            # responder.frame['suggestion'] = suggestions[0]
            #
            # if (score > 80):
            #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
            # else:
            response = 'Sorry, das habe ich nicht verstanden.'

            responder.reply(response)



@app.handle(intent='artist_birthplace')
def say_artist_birthplace(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}



    entity = request.entities
    # name =  request.entities[0]['text']

    if (entity == ()):

        if (em.get_entity() == ''):
            responder.reply('Von welchem Künstler möchstest du den Geburtsort wissen?')
            print('Ohne entity IF artist birthyear: Von welchem Künstler möchstest du den Geburtsort wissen?')

        else:

            name = em.get_entity()


            try:

                s = qa.build_search(index='artists')
                id = s.filter(name=name).execute()[0]['id']


                print('Ohne Entity ELSE artist birthplace')
                #print(responder.history[0]['request']['intent'])
                #print(responder.history[0]['request']['entities'][0]['text'])



                artists = qa.get(index='artists', id=id)

                title = artists[0]['name']
                geburtsort = artists[0]['born_city_de']

                if (geburtsort == 'not available'):
                    responder.reply('Leider habe ich keine Informationen über den Geburtsort von ' + title + '.')
                else:
                    # Respond
                    responder.reply(title + ' wurde in ' + geburtsort + ' geboren.')

            except:

                # query = request.text
                #
                # score = process.extractOne(query, suggestions[0])[1]
                # suggestion = process.extractOne(query, suggestions[0])[0]
                # responder.frame['suggestion'] = suggestions[0]
                #
                # if (score > 80):
                #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
                # else:
                response = 'Sorry, das habe ich nicht verstanden.'

                responder.reply(response)


    else:

        em.set_entity(entity[0]['text'])


        # textfile = open(app_path + '/entities/artists/gazetteer.txt', 'r')
        # zeilen = textfile.readlines()
        # liste = []
        # for item in zeilen:
        #     cleanentry = item.rstrip()
        #     liste.append(cleanentry)
        #
        #
        #
        # artists_list = liste
        # responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artist, 1.0) for artist in artists_list)}

        #artists_list = ['Torsten Belschner', 'Michael Bielicky', 'Peter Callas']
        #responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artists, 1.0) for artists in artists_list)}

        try:

            # Extract id from query
            id = request.entities[0]['value'][0]['id']

            print('Mit Entity ELSE artist birthplace')
            artists = qa.get(index='artists', id=id)

            title = artists[0]['name']
            geburtsort = artists[0]['born_city_de']

            if (geburtsort == 'not available'):
                responder.reply('Leider habe ich keine Informationen über den Geburtsort von ' + title + '.')
            else:
                # Respond
                responder.reply(title + ' wurde in ' + geburtsort + ' geboren.')


        except:

            # query = request.text
            #
            # score = process.extractOne(query, suggestions[0])[1]
            # suggestion = process.extractOne(query, suggestions[0])[0]
            # responder.frame['suggestion'] = suggestions[0]
            #
            # if (score > 80):
            #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
            # else:
            response = 'Sorry, das habe ich nicht verstanden.'

            responder.reply(response)



@app.handle(intent='artist_age')
def say_artist_age(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    # Clear the dialogue frame to start afresh for the next user request.
    responder.frame = {}


    entity = request.entities
    # name =  request.entities[0]['text']

    if (entity == ()):


        if (em.get_entity() == ''):
            responder.reply('Von welchem Künstler möchstest du das Alter wissen?')
            print('Ohne entity IF artist birthyear: Von welchem Künstler möchstest du das Alter wissen?')

        else:

            name = em.get_entity()
            print('Name try else')
            print(name)


            try:

                s = qa.build_search(index='artists')
                id = s.filter(name=name).execute()[0]['id']

                artists = qa.get(index='artists', id=id)

                title = artists[0]['name']
                geburtjahr = artists[0]['born_year']
                todesjahr = artists[0]['died_year']

                from datetime import date
                heute = date.today()
                diesesJahr = heute.year

                if (geburtjahr == 'not available'):
                    responder.reply('Leider habe ich keine Informationen zum Alter von ' + title + '.')
                else:
                    if (todesjahr == 'not available'):
                        alter = diesesJahr - int(geburtjahr)
                        # Respond
                        responder.reply(title + ' ist ' + str(alter) + ' alt.')

                    else:
                        alter = int(todesjahr) - int(geburtjahr)
                        # Respond
                        responder.reply(
                                    title + ' ist im Jahre ' + todesjahr + ' im Alter von ' + str(alter) + ' verstorben.')

            except:

                # query = request.text
                #
                # score = process.extractOne(query, suggestions[0])[1]
                # suggestion = process.extractOne(query, suggestions[0])[0]
                # responder.frame['suggestion'] = suggestions[0]
                #
                # if (score > 80):
                #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
                # else:
                response = 'Sorry, das habe ich nicht verstanden.'

                responder.reply(response)




    else:
        em.set_entity(entity[0]['text'])


        # textfile = open(app_path + '/entities/artists/gazetteer.txt', 'r')
        # zeilen = textfile.readlines()
        # liste = []
        # for item in zeilen:
        #     cleanentry = item.rstrip()
        #     liste.append(cleanentry)
        #
        #
        #
        # artists_list = liste
        # responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artist, 1.0) for artist in artists_list)}

        #artists_list = ['Torsten Belschner', 'Michael Bielicky', 'Peter Callas']
        #responder.params.dynamic_resource['gazetteers'] = {'artists': dict((artists, 1.0) for artists in artists_list)}

        try:

            # Extract id from query
            id = request.entities[0]['value'][0]['id']

            artists = qa.get(index='artists', id=id)

            title = artists[0]['name']
            geburtjahr = artists[0]['born_year']
            todesjahr = artists[0]['died_year']

            from datetime import date
            heute = date.today()
            diesesJahr = heute.year

            if (geburtjahr == 'not available'):
                responder.reply('Leider habe ich keine Informationen zum Alter von ' + title + '.')
            else:
                if (todesjahr == 'not available'):
                    alter = diesesJahr - int(geburtjahr)
                    # Respond
                    responder.reply(title + ' ist ' + str(alter) + ' alt.')

                else:
                    alter = int(todesjahr) - int(geburtjahr)
                    # Respond
                    responder.reply(title + ' ist im Jahre ' + todesjahr + ' im Alter von ' + str(alter) + ' verstorben.')

        except:

            # query = request.text
            #
            # score = process.extractOne(query, suggestions[0])[1]
            # suggestion = process.extractOne(query, suggestions[0])[0]
            # responder.frame['suggestion'] = suggestions[0]
            #
            # if (score > 80):
            #     response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
            # else:
            response = 'Sorry, das habe ich nicht verstanden.'

            responder.reply(response)



@app.handle(intent='openinghours')
def say_openinghours(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    em.set_entity('')

    text = request.text
    print(text)

    entity = request.entities

    if (entity == ()):
        responder.params.allowed_intents = ['zkm.openinghours'] #, 'basic.*']
        responder.reply('Von welchem Wochentag möchtest du die Öffnungszeiten wissen?')
        print(entity)

    else:
        print(entity)
        print(entity[0]['text'])


        if (entity[0]['text'] == 'heute'):
            print('HEUTE')
            s = qa.build_search(index='openinghours')
            id = s.filter(tag=heute_in_wochentag()).execute()[0]['id']

            openinghours = qa.get(index='openinghours', id=id)
            #day = openinghours[0]['tag']
            start = openinghours[0]['start']
            end = openinghours[0]['ende']
            # Respond
            if (start == "geschlossen"):
                response = 'Heute ist das ZKM geschlossen. 😢'
            else:
                response = 'Heute öffnet das ZKM um ' + start + ' Uhr und schließt um ' + end + ' Uhr.'

            responder.reply(response)


        elif (entity[0]['text'] == 'übermorgen'):
            print('ÜBERMORGEN')
            s = qa.build_search(index='openinghours')
            id = s.filter(tag=übermorgen_in_wochentag()).execute()[0]['id']

            openinghours = qa.get(index='openinghours', id=id)
            day = openinghours[0]['tag']
            start = openinghours[0]['start']
            end = openinghours[0]['ende']
            # Respond
            if (start == "geschlossen"):
                response = "Am " + day + ' ist das ZKM geschlossen. 😢'
            else:
                response = 'Am ' + day + ' öffnet das ZKM um ' + start + ' Uhr und schließt um ' + end + ' Uhr.'

            responder.reply(response)


        elif(entity[0]['text'] == 'morgen'):
            print('MORGEN')
            s = qa.build_search(index='openinghours')
            id = s.filter(tag=morgen_in_wochentag()).execute()[0]['id']

            openinghours = qa.get(index='openinghours', id=id)
            day = openinghours[0]['tag']
            start = openinghours[0]['start']
            end = openinghours[0]['ende']
            # Respond
            if (start == "geschlossen"):
                response = "Am " + day + ' ist das ZKM geschlossen. 😢'
            else:
                response = 'Am ' + day + ' öffnet das ZKM um ' + start + ' Uhr und schließt um ' + end + ' Uhr.'

            responder.reply(response)

        elif (hasNumbers(entity[0]['text'])):
            print('TEXT')
            s = qa.build_search(index='openinghours')

            if (datum_in_wochentag(entity[0]['text']) == 'null'):
                responder.params.allowed_intents = ['zkm.openinghours']  # , 'basic.*']
                responder.reply('Könntest du das Datum noch einmal im Zahlenformat eingeben, damit ich dir weiterhelfen kann?')
            else:
                id = s.filter(tag=datum_in_wochentag(entity[0]['text'])).execute()
                id = id[0]['id']

                openinghours = qa.get(index='openinghours', id=id)
                day = openinghours[0]['tag']
                start = openinghours[0]['start']
                end = openinghours[0]['ende']
                # Respond
                if (start == "geschlossen"):
                    response = "Am " + day + ' den ' + entity[0]['text'] + ' ist das ZKM geschlossen. 😢'
                else:
                    response = 'Am ' + day + ' den ' + entity[0]['text'] + ' öffnet das ZKM um ' + start + ' Uhr und schließt um ' + end + ' Uhr.'

                responder.reply(response)

        else:
            #Verarbeitung von Wochentagen
            print('Verarbeitung Wochentage')
            id = request.entities[0]['value'][0]['id']

            openinghours = qa.get(index='openinghours', id=id)
            day = openinghours[0]['tag']
            start = openinghours[0]['start']
            end = openinghours[0]['ende']
            # Respond
            if (start == "geschlossen"):
                response = "Am " + day + ' ist das ZKM geschlossen. 😢'
            else:
                response = 'Am ' + day + ' öffnet das ZKM um ' + start + ' Uhr und schließt um ' + end + ' Uhr.'

            responder.reply(response)


@app.dialogue_flow(domain='zkm', intent='exhibition_current')
def say_exhibition_current(request, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """

    em.set_entity('')
    # Clear the dialogue frame to start afresh for the next user request.

    text = request.text
    print(text)

    if (text == 'ZKM gerade Ausstellungen &+*bnbn?'):

        print('ausstellungzkmaktuell')
        exhibition = qa.get(index='exhibition', size=50, _sort='ende_tag', _sort_type='desc')

        ausstellung_offen = string_current_exhibitions(exhibition)

        #responder.reply('Ich habe Informationen über Ausstellungen des ZKMs, deren Zeitraum und Inhalte sowie die mitwirkenden Künstler für dich. Aktuell sind folgende Ausstellungen im ZKM zu sehen: ' + ausstellung_offen)
        responder.reply(ausstellung_offen)


    if (text == 'ZKM gerade Ausstellungen &+*bnbn??'):

        print('ZKM gerade Ausstellungen &+*bnbn??')
        exhibition = qa.get(index='exhibition', size=50, _sort='ende_tag', _sort_type='desc')

        artists = draw_ten_artists_from_current_exhibition(exhibition)

        #responder.reply('Ich habe Informationen über das Geburtsjahr, das Alter, den Geburtsort und über den allgemeinen Werdegang der jeweiligen Künstler. Diese zehn Künstler sind beispielsweise aktuell in unseren Ausstellungen zu sehen: ' + artists)
        responder.reply(artists)


    responder.frame = {}

    exhibition = qa.get(index='exhibition', size=50, _sort='ende_tag', _sort_type='desc')
    ausstellung_offen = string_current_exhibitions(exhibition)

    # Respond
    responder.reply('Folgende Ausstellungen sind aktuell geöffnet: ' + ausstellung_offen)
    responder.exit_flow()

@say_exhibition_current.handle(default=True)
def default_handler(request, responder):
    responder.reply('Damit kann ich dir leider nicht weiterhelfen.')
    responder.exit_flow()

@say_exhibition_current.handle(intent='exhibition_current')
def say_exhibition_current_in_flow_handler(request, responder):
    say_exhibition_current(request, responder)


#### intents from 'fun' domain ####
@app.handle(intent='jokes')
def say_jokes(request, responder):

    em.set_entity('')

    responder.frame = {}

    import random
    number = int(random.randint(1, 14))

    joke = qa.get(index='jokes', id=number)
    joke = joke[0]['joke']

    responder.reply(joke)



#### intents from 'unknown' domain ####

@app.handle(default=True)
@app.handle(intent='unsupported')
def default(request, responder):
    """
    When the user asks an unrelated question, convey the lack of understanding for the requested
    information and suggest an alternative.
    """
    em.set_entity('')

    query = request.text

    score = process.extractOne(query, suggestions[0])[1]
    suggestion = process.extractOne(query, suggestions[0])[0]

    if (score > 90):
        response = 'Sorry, das habe ich nicht verstanden, aber meintest du vielleicht: ' + suggestion
    else:
        response = 'Sorry, das habe ich nicht verstanden.'

    responder.reply(response)