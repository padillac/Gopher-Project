Chris Padilla
Gopher Project
Changes between first draft and final draft:

My first draft of code worked well in terms of conforming with the Gopher protocol.
The only changes I needed to make involved the organization/comments on the code,
and changing the names of the .links files to be ".links.txt" instead of "links.txt"
(The only reason left off the '.' initially was because on the lab computers, it didn't work to save a file with a name that started with a period.)
I also had to add a way for the user to quit the server without just force-quitting Terminal.

The first two changes were very simple to make: I added periods to the beginning of all the .links filenames,
and I added comments explaining my thinking and the functionality of my code, as well as
headers explaining what the programs do.

To add a 'quit' ability to the server, I added an additional thread that would wait for the user to enter 'q'
into the command line. If this key were entered, the socket would be forcibly closed and the program would exit.
