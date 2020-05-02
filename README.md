![Lynda](https://test1.mannu.me/LyndaRobot.jpg)
# LyndaRobot
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/04423a6d18ab43d396ab738fca5ba804)](https://www.codacy.com/manual/Dank-del/EnterpriseAL?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Dank-del/EnterpriseAL&amp;utm_campaign=Badge_Grade)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AmaanAhmed/LydiaRobot)


A modular telegram Python bot running on python3 with an sqlalchemy database.

Originally a [Kigyō](https://t.me/kigyorobot) fork - Lynda has evolved further and was built to be more useful for Anime Chats. 

Can be found on telegram as [Lynda // Cyborg](https://t.me/LyndaRobot).

The Support group can be reached out to at [Eagle Union](https://t.me/YorktownEagleUnion), where you can ask for help setting up your bot, discover/request new features, report bugs, and stay in the loop whenever a new update is available. 

 

## Setting up the bot (Read this before trying to use!):

# How to setup
<details>
  <summary>Click to expand!! </summary>
  
 
 
 Note: [Eagle Union](https://t.me/YorktownEagleUnion) aims to handle support for [Lynda // Cyborg](https://t.me/LyndaRobot) and now how to setup your own fork, if you find this bit confusing/tough to understand then we recommend you ask a dev, kindly avoid asking how to setup the bot instance in the support chat, it aims to help our own instance of the bot. 
  
  ## Setting up the bot (Read this before trying to use!):
Please make sure to use python3.6, as I cannot guarantee everything will work as expected on older python versions!
This is because markdown parsing is done by iterating through a dict, which are ordered by default in 3.6.



## How to setup on Heroku 
For starters click on this button


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AmaanAhmed/LydiaRobot)

Fill in all the details , Deploy.
Now go to https://dashboard.heroku.com/apps/(app-name)/resources ( Replace (app-name) with your app name )
Turn on worker dyno (Don't worry It's free :D)
Now send the bot /start , If it doesn't respond go to https://dashboard.heroku.com/apps/(app-name)/settings and remove webhook and port.
</details>






## Credits
The bot is based of on the original work done by [PaulSonOfLars](https://github.com/PaulSonOfLars)
This repo was just reamped to suit an Anime-centric community. All original credits go to Paul and his dedication, Without his efforts, this fork would not have been possible!

Most modules including Blacklists, Lyrics and much more are taken from [TheRealPhoenixBot](https://t.me/TheRealPhoenixBot)

Thank you for contributing with me in this Project:
+ [TheRealPhoenix](https://github.com/rsktg)
+ [DragSama](https://github.com/DragSama)
+ [TsunayoshiSawada](https://github.com/TsunayoshiSawada)
+ [Athphane](https://github.com/athphane)
+ [Dank-del](https://github.com/Dank-del)

Any other authorship/credits can be seen through the commits.

Should any be missing kindly let us know at [Eagle Union](https://t.me/YorktownEagleUnion) or simply submit a pull request on the readme.
