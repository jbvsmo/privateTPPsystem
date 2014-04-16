Private Twitch Plays Pokémon System
-----------------------------------

The idea for this code is to be able to have a private session of "Twitch Plays Pokémon" gameplay.

Installing the server might require a little bit of effort. Right now the code was tested on Windows,
but may work on other platforms.

**Status:** It works quite well, but some bug fix might be needed.


What you will need:

1. Server:
    - This code!
    - [Python 3.3 or later](https://www.python.org/downloads/)
    - [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download)
    - [Max Remote Server](http://www.bitunitsstudio.com/max-remote-server.html)
    - Java Runtime (optional -- depends on how Max Remote Server is running)
    - An Emulator (For GBA games, VisualBoyAdvance-M is very good)

2. Players:
    - Android device
    - [Max Remote](https://play.google.com/store/apps/details?id=com.bitunits.maxremote)


Please contribute with changes/bug reports if you want!



How to install the server:
--------------------------

The installation of Python 3 and PyQt4 are pretty much straightforward.

"Max Remote Server" is a tool to be used with the "Max Remote" android app. This application is
not mine and I cannot control what changes they might do on it. I only chose it because the server
was quite simple to reverse engineer so I could create my own server to talk with the smartphones
and pass commands to the original server.

I only tried the "Portable Version 2.3 - Multiplatform" of Max Remote Server, but others may also
work. The trick was to assign a different network port for it (originally on 8585 both TCP and UDP)
and open my own server on this port. The Multiplatform version will require a Java Runtime installed.
I don't know the minimal version or if it only works with Oracle JVM.

The first time running Max Remote Server it will create a simple configuration file with 3 lines:

    8585
    n
    i

The first line tells which port it will connect. Change that to `8589` (If you want another port,
you will have to change on the `TwitchController.config` file).

Now you're good to go!



How to play
-----------

On the server:

1. Start "Max Remote Server" after changing the port
2. Run the `main.py` file (Double clicking on Windows should work)
3. Start the emulator
4. You will need to map the keys in the emulator.
    The keys are `A: A`, `B: B`, `START: C`, `SELECT: D`, `LEFT: E`, `UP: F`, `RIGHT: G`, `DOWN: H`.
    It is easier to set the key mapping with a smartphone, by clicking it.
5. IMPORTANT: The emulator window must be selected (click on it with the mouse) for the inputs to work.

On your android devices:

1. Connect the device **to the same network** the server is running
2. Open "Max Remote" and click to add server automatically.
3. It should appear "Private Twitch! By JB". So click it.
4. Choose the joypad icon and select a joypad with a design compatible to what you are playing.
(DO NOT CHANGE THE DEFAULT KEY MAP or the server will not recognize the inputs).
5. MASH BUTTONS!



Customize the Gameplay
----------------------

- When changing between the features, it is a great idea to disable the users input, so uncheck the "Enabled" box.

- There are three gameplay modes: Anarchy, Democracy and Raffle.
    - On "Anarchy", every input will be sent to the emulator
    - On "Democracy", the inputs will be counted for a certain period of time (Democracy Time) and, after this
    period, the most voted input will be executed.
    - On "Raffle", the inputs will be counted for a certain period of time (Raffle Time) and, after this
    period, one of the inputs will be *chosen at random*.

- If one wants to have a gameplay more like the original Twitch Plays Pokémon, the inputs may be delayed (Delay).

- Once players connect to the server, their IP address will appear on the Player list. You can select them and click
the "E" button to edit their names. Try adding one user at a time to be able to tell know which one they are.

- The "+" button will add new users. Only use it for bots (The PC tab below). You can delete bots with "-" button.

- Bots will play a random command in the selected interval (the interval may be a little bit bigger o smaller than
the selected one to avoid clustering -- adds more entropy).


TO DO
-----

Some options in the interface do not work yet and some others may be added

- Create personalities for bots
    1. Only press a single button/a set of buttons
    2. Play against/with the majority of commands of last seconds
    3. Always play after some other player (to help/harm them)
- Install Democracy (or Raffle) each X minutes.
- Vote for democracy/anarchy/raffle
- Add timer to show how much time of democracy until the command is executed (like a bar)
- Log the data (IMPORTANT!). Possibly show some stats later.
- Fix some bugs on the interface. Make the commands window prettier.



Screenshot
----------

![](http://i.imgur.com/AmVOcFz.png)