# Amazon-Cart-Total

## Description
A Command Line Interface (CLI) App for getting the total of the cost of items in an Amazon.com wishlist webpage.

<hr>

## Getting Started
### Prerequisites
- **Python 3.10+**
- **git**
- Saved **Amazon Wishlist** webpage (HTML text document).

<hr>

## Installing
- Open a working directory to download and use the program in your favourite Command Terminal.
- Download the program using the following command:
    > git clone https://github.com/Racerin/Amazon-Cart-Total.git
- Change to the directory **'Amazon-Cart-Total'**
- Run the following commands in a command terminal to acivate the virtual environment. 

*NB: execute appropriate command according to the Operating System in use.*

> python -m venv venv \
> <span style="color:grey">...wait for dependencies to complete...</span> \
> python -m pip install -r requirements.txt 

> <span style="color:grey">Linux/Bash-Based OS:</span> \
> source venv/Scripts/activate \
> <span style="color:grey">Linux/Bash-Based OS:</span> \
> .\venv\Scripts\activate

<hr>

## Executing program
Save the webpage of the Amazon wishlist onto your computer within the **'Amazon-Cart-Total'** directory.

In the command terminal, run the command
> python main.py main

You should see the total of the wishlist apear in the terminal.
<hr>

For other commands, type:
> python main.py --help

You will also see the instruction on how to run the commands.
<hr>


## Help
Any advise for common problems or issues.
For CLI App commands, type command in Amazon-Cart-Total directory
. python main.py --help
<hr>

## Authors
[Darnell Baird](https://github.com/Racerin) (Main Developer)
<hr>

## Version History
- 0.1
    - Initial Release
    - See [commit change](https://github.com/Racerin/Amazon-Cart-Total/commits/master) or See [release history](https://github.com/Racerin/Amazon-Cart-Total/releases)
<hr>

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Racerin/Amazon-Cart-Total/blob/master/LICENSE) file for details
<hr>

## Acknowledgements
The following repositories inspired me to do this cli app.

- LenAnderson/[Amazon-Wishlist-Total](https://github.com/LenAnderson/Amazon-Wishlist-Total)