from datetime import datetime #Importing date time library for the file names
setup = 0  #Global setup variable - to track if a polling booth file has been created
currentFile = "" #Globel variable that tracks the name of the current file name in use
def main():
    global setup
    option = 0
    while option != 5: #Checking if the user wants to exit or not
        if setup == 1: #Confirming that a file has been setup for the votes to be written to
            option = menu() #Calling the menu funcition
            if option == 1:
                pollingFile()
            elif option == 2:
                pollingEnter()
            elif option == 3:
                pollingData()
            elif option == 4:
                pollingStats()
            elif option == 5:
                print("\nThank you for using the system")
            else:
                print("\nInvalid Data Entry\n")
        else:
            option = menu()
            if option == 1:
                pollingFile()
            elif option == 2: #Exit option for menu before a file has been set
                print("\nThank you for using the system")
                option = 5
            else:
                print("\nInvalid Data Entry\n")


def menu():
    global setup
    print("Electoral System \n****************\n") #Prints the menu
    print("1. Setup polling station votes file\n")
    if setup == 1:
        print("2. Enter polling booth\n")
        print("3. Collate data from other polling stations\n")
        print("4. Review statistics\n")
        print("5. Exit\n")
    else:
        print("2. Exit\n")
    try:
        option = int(input("Enter Choice:"))
        return option  # Returns the users choice
    except:
        option = 0


def pollingFile(): #Function to set up the polling file
    global setup
    global currentFile
    now = datetime.now() #Gets the current date
    fileName = input("What is the name of the polling booth?") #Allows user to name the file
    try:
        fileObj = open("Belfast_"+fileName+"_"+str(now.date())+".txt", "w") #Creats and opens the file with the chosen name by the user plus the current date to be written to
        setup = 1 #Sets the setup value to be accessible by the whole program
        currentFile = "Belfast_"+fileName+"_"+str(now.date())+".txt" #Sets the current file name to be accessible by the whole program
        for count in range(0, 7): #Writes 7 0s to the file
            fileObj.write("0")
            fileObj.write("\n")
        fileObj.close()
        names = []
        try: #Will attempt to open a previously created pollingBooth.txt file
            fileObj = open("pollingBooths.txt", "r") #Opens the pollingBooths.txt containing the names of all polling booths
            for booth in fileObj.readlines():
                if booth != "\n":
                    names.append(booth) #Writes the names of all polling booths to the names list for later use
        except:
            fileObj.close()
        fileObj.close()
        names.append(currentFile) #adds the current file name to the names list
        fileObj = open("pollingBooths.txt", "w")
        for name in range(0, len(names)): #Writes all file names back into the pollingBooths.txt file
            fileObj.write(names[name])
            fileObj.write("\n")
        fileObj.close()
        print('''File "Belfast_''' + fileName + "_" + str(now.date()) + '''.txt" has been created!''') #Confirms file creation including name
    except: #Incase of any issue throughout it will stop a crash and print an error message
        print("There was an issue creating your file.")


def pollingEnter(): #Function to enter voting choices
    global currentFile
    while True: #Continues repeating indefinitely until a break occurs
        male = 0
        female = 0
        addToFile = True
        choices = []
        print("\nElectoral Polling Booth \n***********************\n")
        gender = input("What gender are you?(M/F):").lower()
        if gender == "secret password": #Allows for user to return to the main menu
            break #Exits the while loop
        elif gender != "m" and gender != "male" and gender != "f" and gender != "female": #checks to confirm a valid gender input
            print("Invalid input")
        else:
            if gender == "m" or gender == "male":
                male = 1 #Adding to the male tally count
            else:
                female = 1 #Adding to the female tally count
            while True:  #This tests for valid voting inputs from the user
                    if len(choices) < 1: #Checks the length of the list to confirm a valid input was entered, if not it will repeat until a valid input is entered
                        track = input("Black Party - Joan Jet:")
                        choices = testVotes(choices, track) #Calls the testVotes function to validate the vote
                    elif len(choices) == 1:
                        track = input("Blue Party - Bert Navy:")
                        choices = testVotes(choices, track)
                    elif len(choices) == 2:
                        track = input("Green Party - Luke Lime:")
                        choices = testVotes(choices, track)
                    elif len(choices) == 3:
                        track = input("Red Party - Rose Burgundy:")
                        choices = testVotes(choices, track)
                    elif len(choices) == 4:
                        track = input("Yellow Party - Egbert Yoke:")
                        choices = testVotes(choices, track)
                    else: #When all inputs have been registered it will move onto checking for duplicates
                        for item in range(0, 5): #Grabs the first item in the votes list
                            for check in range(0, 5): #Checks the first item against all other values
                                if choices[item] == choices[check] and item != check and choices[check] != 0: #Confirms that the registered repeated value is not itself or a zero
                                    print("Cannot have multiple of the same vote") #Prints error message
                                    choices.clear() #Clears list to allow user to re-enter votes
                                    addToFile = False #Stops the program from continuing
                                    break
                            if addToFile == False:
                                break #Will cause the program to jump back to the enter votes portion
                        if addToFile == True: #Converts the votes to their values
                            for number in range(0, 5):
                                if int(choices[number]) == 1:
                                    choices[number] = 1
                                elif int(choices[number]) == 2:
                                    choices[number] = 0.5
                                elif int(choices[number]) == 3:
                                    choices[number] = 0.33
                                elif int(choices[number]) == 4:
                                    choices[number] = 0.25
                                elif int(choices[number]) == 5:
                                    choices[number] = 0.2
                                elif int(choices[number]) == 0:
                                    choices[number] = 0
                                else:
                                    print("Error") #Incase of error
                                    break
                            fileObj = open(currentFile, "r") #Opens the current file to be read from
                            choice = 0
                            for vote in fileObj.readlines(): #Reads the stored votes value from current file to list
                                if choice == 5: #Checking if the value is the male count
                                    choices.append(float(vote))
                                    choices[choice] += float(male)
                                elif choice == 6: #Checking if the value is the female count
                                    choices.append(float(vote))
                                    choices[choice] += float(female)
                                else:
                                    choices[choice] += float(vote)
                                choice += 1
                            fileObj.close()
                            fileObj = open(currentFile, "w") #Reopens the current file to be written to
                            for element in range(0, 7):
                                fileObj.write(str(round(choices[element], 2)) + "\n") #Writes the vote values to the file
                            fileObj.close()
                            break
                        else:
                            break
                        break
def pollingData(): #Function to collate data from other polling files into one
    check = "y"
    while check == "yes" or check == "y": #While loop to allow user to collate multiple files if they choose
        totals = []
        votes = []
        track = 0
        files = []
        fileChoice = 0
        fileObj = open("pollingBooths.txt", "r") #opens the pollingBooth.txt file to allow the names of all polling files to be accessed
        for file in fileObj.readlines():
            if file != "\n":
                files.append(str(file)) #Writes the polling booth names to the files list
                track += 1
                print(track, ". ", file) #Prints a list of file options for the user to choose from
        fileObj.close()
        while True: #Will repeat input option in case of invalid entry
            try:
                fileChoice = int(input("Which polling file would you like to add to a total votes file?"))
                if fileChoice <= len(files) and fileChoice > 0: #Checks if input is in range
                    break
                else:
                    print("Invalid option") #Error Message
            except:
                print("Invalid option")#Error Message
        fileChoice = str(files[fileChoice-1]) #Gets the name of the chosen file
        fileChoice = fileChoice[:-1] #Gets just the name of the file removing any extra string values such as "\n"
        fileObj = open(fileChoice, "r") #Opens the chosen file to be read from
        for vote in fileObj.readlines():#Reads the vote values from the file and writes them to the votes list
            votes.append(vote)
        fileObj.close()
        try: #Attempts to open the totalVotes.txt file to read from
            fileObj = open("totalVotes.txt", "r")
            for total in fileObj.readlines():
                if total != "\n":
                    totals.append(total)
            for vote in range(0, 7):
                votes[vote] = float(votes[vote]) + float(totals[vote]) #Adds the votes from the totalsVotes.txt file to the current votes
            fileObj.close()
        except: #If the totalVotes.txt file does not already exist then this will run to create the file
            fileObj.close()
        fileObj = open("totalVotes.txt", "w") #Will continue to write the new total back to the totalVotes.txt file
        for vote in range(0, 7):
            fileObj.write(str(votes[vote]))
            fileObj.write("\n") #Prints the collated votes
        print('''\t Total Votes: 
                     Black Party – Joan Jet:''', votes[0], '''
                     Blue Party – Bert Navy:''', votes[1], '''
                     Green Party – Luke Lime:''', votes[2], '''
                     Red Party – Rose Burgundy:''', votes[3], '''
                     Yellow Party – Egbert Yoke:''', votes[4], '''
                     Male:''', votes[5], '''
                     Female:''', votes[6])
        fileObj.close()
        check = input("Do you want to add another file? (Y/N)").lower() #Checks if the user wants to add another file
        while check != "y" and check != "yes" and check != "n" and check != "no":
            print("Invalid input")
            check = input("Do you want to add another file? (Y/N):").lower()


def pollingStats(): #Function to turn the collated data into percentages
    total = 0
    tally = -1
    totalVotes = [0, 0, 0, 0, 0, 0, 0]
    try:
        fileObj = open("totalVotes.txt", "r") #Attempts to open the totalVotes.txt file to read from
    except:
        fileObj = open("totalVotes.txt", "w") #Creates the totalVotes.txt file if it does not already exist
        for element in range(0, 7):
            fileObj.write("0")
        fileObj.close()
        fileObj = open("totalVotes.txt", "r")
    for vote in fileObj.readlines(): #Writes the vote values to the totalVotes list
        if vote != "\n":
            tally += 1
            totalVotes[tally] += float(vote)
            total += float(vote)
    tally = -1
    maleFemaleTotal = (float(totalVotes[5]) + float(totalVotes[6])) #Calculates the total voters
    total -= maleFemaleTotal #Calculate the total value of the votes without the number of voters interfering
    for vote in range(0, 7): #Calculates percentage of total the value accounts for
        try:
            tally += 1
            if tally == 5:
                totalVotes[5] = round((float(totalVotes[5]) / maleFemaleTotal) * 100, 2) #Male percentage
            elif tally == 6:
                totalVotes[6] = round((float(totalVotes[6]) / maleFemaleTotal) * 100, 2) #Female percentage
            else:
                totalVotes[tally] = round((float(totalVotes[tally]) / total) * 100, 2) #Vote percentage
        except:
            totalVotes[tally] = 0 #If a calculation returns an error then the value will be set as 0
    fileObj.close() #Prints the percentages for the user to view
    print('''\t Total Votes:
                Black Party – Joan Jet:''', totalVotes[0], "%", '''
                Blue Party – Bert Navy:''', totalVotes[1], "%" '''
                Green Party – Luke Lime:''', totalVotes[2], "%", '''
                Red Party – Rose Burgundy:''', totalVotes[3], "%", '''
                Yellow Party – Egbert Yoke''', totalVotes[4], "%", '''
                Male:''', totalVotes[5], "%", '''
                Female:''', totalVotes[6], "%")
    input("Press any button to return to menu") #An input to allow the user to view the data and continue when they please

def testVotes(choices, track):
    try: #Try specifically used to detect the entry of a letter in a vote input
        track = int(track) #Allows for the prevention of letter inputs
        if track > 5 or track < 0: #Keeps the votes within the given range of 1-5
            print("Outside range")
        else:
            choices.append(track) #If it is a valid vote it will be added to the choices list
    except:
        if track == "": #Blank values are valid and as such they have to be accounted for as a '0' value
            choices.append(0)
        else:
            print("Not a number") #Prints error message
    return choices #retunrs the choices list

main() #Calls the main function to begin the program