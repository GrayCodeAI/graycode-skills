
List of CE specific functions and variables:

Global Variables:
TrainerOrigin : A variable that contains the path of the trainer that launched cheat engine (Only set when launched as a trainer)
process : A variable that contains the main modulename of the currently opened process
MainForm: The main ce gui
AddressList: The address list of the main ce gui


Global Functions:
getCEVersion(): Returns a floating point value specifying the version of cheat engine
getCheatEngineFileVersion(): Returns the full version data of the cheat engine version. A raw integer, and a table containing major, minor, release and build

getOperatingSystem(): Returns 0 if CE is running in Windows, 1 for Mac

darkMode(): Returns true if CE is running in windows Dark Mode. Has no effect on mac

activateProtection(): Prevents basic memory scanners from opening the cheat engine process (Not that useful)
enableDRM(altitude OPTIONAL, secondaryprocessid OPTIONAL ) : Prevents normal memory scanners from reading the Cheat Engine process (kernelmode)  The secondaryprocessid lets you protect another process. E.g the game itself, so they can't easily see what you change 

fullAccess(address,size): Changes the protection of a block of memory to writable and executable
setMemoryProtection(address, size, {R:boolean; W: Boolean; X: Boolean}): Sets the given protection on the address range. Note, some systems do not support X and W to be true at the same time

loadTable(filename, merge OPTIONAL): Loads a .ct or .cetrainer. If merge is provided and set to true it will not clear the old table
loadTable(stream ,merge OPTIONAL, ignoreluascriptdialog BOOLEAN): Loads a table from a stream object
saveTable(filename, protect OPTIONAL, dontDeactivateDesignerForms OPTIONAL): Saves the current table. If protect is provided and set to true and the filename has the .CETRAINER extension, it will protect it from reading normally
saveTable(stream, dontDeactivateDesignerForms OPTIONAL): Saves the current table to a stream object

signTable(filename) : If the current CE install has a valid cheta engine signature, this will sign the specific table with that signature (will pop up the password request)

note: addresses can be strings, they will get interpreted by ce's symbolhandler

copyMemory(sourceAddress: integer, size: integer, destinationAddress:integer SEMIOPTIONAL, Method:integer OPTIONAL): 
  Copies memory from the given address to the destination address
  If no destinationAddress is given(or nil), CE will allocate a random address for you

  Method can be:
    nil/0: Copy from target process to target process
    1: Copy from target process to CE Memory
    2: Copy from CE Memory to target process
    3: Copy from CE Memory to CE Memory

  Returns the address of the copy on success, nil on failure
  
compareMemory(address1: integer; address2: integer; size: integer;  method: integer)
  Compares the memory and returns true if the same or false and and index where the first disparity is

  Method can be:
  0: Target to Target
  1: Address1=Target Address2=CE
  2: Address1=CE Address2=CE

readBytes(address,bytecount, ReturnAsTable ) : returns the bytes at the given address. If ReturnAsTable is true it will return a table instead of multiple bytes
  Reads the bytes at the given address and returns a table containing the read out bytes

writeBytes(address, x,x,x,x,...) : Write the given bytes to the given address from a table
writeBytes(address, table) : Write the given bytes to the given address from a table

readShortInteger(address) / readByte(address) : Reads a 8-bit integer from the specified address
readSmallInteger(address) : Reads a 16-bit integer from the specified address
readInteger(address) : Reads a 32-bit integer from the specified address
readQword(address): Reads a 64-bit integer from the specified address
readPointer(address): In a 64-bit target this equals readQword, in a 32-bit target readInteger()
readFloat(address) : Reads a single precision floating point value from the specified address
readDouble(address) : Reads a double precision floating point value from the specified address
readString(address, maxlength, widechar OPTIONAL) : Reads a string till it encounters a 0-terminator. Maxlength is just so you won't freeze for too long, set to 6000 if you don't care too much. Set WideChar to true if it is encoded using a widechar formatting
writeShortInteger(address,value) / writeByte(address,value) : Writes a 8-bit integer to the specified address. Returns true on success
writeSmallInteger(address,value) : Writes a 16-bit integer to the specified address. Returns true on success
writeInteger(address,value) : Writes a 32-bit integer to the specified address. Returns true on success
writeQword(address, value): Write a 64-bit integer to the specified address. Returns true on success
writePointer(address,value)
writeFloat(address,value) : Writes a single precision floating point to the specified address. Returns true on success
writeDouble(address,value) : Writes a double precision floating point to the specified address. Returns true on success
writeString(address,text, widechar OPTIONAL) : Write a string to the specified address. Returns true on success

readBytesLocal(address,bytecount, ReturnAsTable) : See readBytes but then it's for Cheat engine's memory
readSmallIntegerLocal(address) : Reads a 16-bit integer from the specified address in CE's memory
readIntegerLocal(address) : Reads a 32-bit integer from the specified address in CE's memory
readQwordLocal(address) : Reads a 64-bit integer from the specified address in CE's memory
readPointerLocal(address) : ReadQwordLocal/ReadIntegerLocal depending on the cheat engine build
readFloatLocal(address) : Reads a single precision floating point value from the specified address in CE's memory
readDoubleLocal(address) : Reads a double precision floating point value from the specified address in CE's memory
readStringLocal(address, maxlength, widechar OPTIONAL)
writeSmallIntegerLocal(address,value) : Writes a 16-bit integer to the specified address in CE's memory. Returns true on success
writeIntegerLocal(address,value) : Writes a 32-bit integer to the specified address in CE's memory. Returns true on success
writeQwordLocal(address,value) : Writes a 64-bit integer to the specified address in CE's memory. Returns true on success
writePointerLocal(address,value)
writeFloatLocal(address,value) : Writes a single precision floating point to the specified address in CE's memory. Returns true on success
writeDoubleLocal(address,value) : Writes a double precision floating point to the specified address in CE's memory. Returns true on success
writeStringLocal(address,string, widechar OPTIONAL)
writeBytesLocal(address, x,x,x,x,...) : See writeBytes but then it's for Cheat Engine's memory
writeBytesLocal(address, table, , count) : See writeBytes but then it's for Cheat Engine's memory

readSmallInteger, readInteger, readSmallIntegerLocal, readIntegerLocal
can also have second boolean parameter. If true, value will be signed.

signExtend(value,mostSignificantBit): integer - Extends the bits so that if it's MSB bit is set, it will be negative

wordToByteTable(number): {}          - Converts a word to a bytetable
dwordToByteTable(number): {}         - Converts a dword to a bytetable
qwordToByteTable(number): {}         - Converts a qword to a bytetable
floatToByteTable(number): {}         - Converts a float to a bytetable
doubleToByteTable(number): {}        - Converts a double to a bytetable
extendedToByteTable(number): {}      - Converts an extended to a bytetable
stringToByteTable(string): {}        - Converts a string to a bytetable
wideStringToByteTable(string): {}    - Converts a string to a widestring and converts that to a bytetable

byteTableToWord(table, OPTIONAL signed:boolean): number       - Converts a bytetable to a word
byteTableToDword(table, OPTIONAL signed:boolean): number      - Converts a bytetable to a dword
byteTableToQword(table): number      - Converts a bytetable to a qword
byteTableToFloat(table): number      - Converts a bytetable to a float
byteTableToDouble(table): number     - Converts a bytetable to a double
byteTableToExtended(table): number   - Converts a bytetable to an extended and converts that to a double
byteTableToString(table): string     - Converts a bytetable to a string
byteTableToWideString(table): string - Converts a bytetable to a widestring and converts that to a string

bOr(int1, int2)   : Binary Or
bXor(int1, int2)  : Binary Xor
bAnd(int1, int2)  : Binary And
bShl(int, int2)   : Binary shift left
bShr(int, int2)   : Binary shift right
bNot(int)         : Binary not

enumMemoryRegions() : Returns an indexed table containing the memorylayout. Each entry consists out of: BaseAddress, AllocationBase, AllocationProtect, RegionSize, State, Protect, Type

writeRegionToFile(filename, sourceaddress,size) : Writes the given region to a file. Returns the number of bytes written
readRegionFromFile(filename, destinationaddress)

resetLuaState(): This will create a new lua state that will be used. (Does not destroy the old one, so memory leak)
getGlobalVariable(string): Returns the given variable from the main lua state. Only basic types are supported.  (Handy for new lua state threads)
setGlobalVariable(string, something): Sets the global variable names string in the main lua state.  Only basic types are supported

createRef(...): integer - Returns an integer reference that you can use with getRef. Useful for objects that can only store integers and need to reference lua objects.  (Component.Tag...)
getRef(integer): ... - Returns whatever the reference points out
destroyRef(integer) - Removes the reference

encodeFunction(function): string - Converts a given function into an encoded string that you can pass on to decodeFunction
decodeFunction(string): function - Converts an encoded string back into a function.  Note that the string must be made on the same architecture as it is currently running. 32-bit can only load 32-bit, 64-bit can only load 64-bit.  So either have two scripts ready, or limit to only one architecture. (Like .EXE trainers)

encodeFunctionEx(string,pathtodll OPTIONAL) - See encodeFunction but uses a script instead of a function, and lets you specify which lua dll to use (Note: Still can't use 32-bit dll's in 64-bit and vice versa)


getTranslationFolder(): Returns the path of the current translation files. Empty if there is no translation going on
loadPOFile(path): Loads a .PO file used for translation
translate(string): Returns a translation of the string. Returns the same string if it can't be found
translateID(translationid: string, originalstring: string OPTIONAL): Returns a translation of the string id

ansiToUtf8(string): Converts a string in Ansi encoding to UTF8
utf8ToAnsi(string): Converts a string in UTF8 encoding to Ansi
Note: GUI components mainly show in UTF8, some other functions use Ansi, try to find out which ones...


enumModules(processid OPTIONAL):
  Returns a table containing information about each module in the current process, or the specified processid
  Each entry is a table with fields
    Name : String containing the modulename    
    Address: Integer representing the address the module is loaded
    Is64Bit: Boolean set to true if it's a 64-bit module
    PathToFile: String to the location this module is loaded


md5memory(address, size): Returns a md5 sum calculated from the provided memory. 
md5file(pathtofile): Returns a md5 sum calculated from the file. 
getFileVersion(pathtofile): returns the 64-bit file version, and a table that has split up the file version into major, minor, release and build

getFileList(Path:string, searchMask:string OPTIONAL, SearchSubDirs: boolean OPTIONAL, DirAttrib: integer OPTIONAL): Returns an indexed table with filenames
getDirectoryList(Path:string, SearchSubDirs: boolean OPTIONAL): Returns an indexed table with directory names
extractFileName(filepath): returns the filename of the path
extractFileExt(filepath): returns the file extension of the path
extractFileNameWithoutExt(filepath): Returns the filename of the path, without the extension
extractFilePath(filepath): removes the filename from the path

getTempFolder() : Returns the path to the temp folder
fileExists(pathtofile): Returns true if a file exists at that path
deleteFile(pathtofile): Returns true if a file existed at that path, and now not anymore

enableWindowsSymbols(): Will download the PDB files of Windows and load them (Takes a long time the first time)
getAddress(string, local OPTIONAL): returns the address of a symbol. Can be a modulename or an export. set Local to true if you wish to querry the symboltable of the ce process
enableKernelSymbols(): Will check the option for kernelmode symbols in memory view (Gets only the exports unless enableWindowsSymbols() is used)
getAddressSafe(string, local OPTIONAL, shallow OPTIONAL): returns the address of a symbol, or nil if not found. Similar to getAddress when errorOnLookup is false, but returns nil instead
getSymbolInfo(symbolname): Returns a table as defined by the SymbolList class object (modulename, searchkey, address, size)
getModuleSize(modulename): Returns the size of a given module (Use getAddress to get the base address)
getRTTIClassName(address): Returns the classname of a given structure based on RTTI information (assuming it can be found, returns nil if not or unknown)

reinitializeSymbolhandler(waittilldone: BOOLEAN OPTIONAL, default=TRUE): reinitializes the symbolhandler. E.g when new modules have been loaded
reinitializeDotNetSymbolhandler(modulename OPTIONAL): Reinitializes only the DotNet part of the symbol list. (E.g After an ILCode has been JITed) (6.4+)
reinitializeSelfSymbolhandler(waittilldone: BOOLEAN OPTIONAL, default=TRUE): reinitializes the selfsymbolhandler. E.g when new modules have been loaded to CE process
waitForSections(): Waits till the sections have been enumerated
waitForExports(): Waits till all DLL Exports are loaded 
waitForDotNet(): Waits till all .NET symbols are loaded (this includes DLL Exports)
waitForPDB(): Waits till all PDB symbols are loaded (this includes DLL Exports, and .NET)
searchPDBWhileLoading(state: boolean): Will interrupt symbol enum to query the debughelp symbol handler about a specific symbol. This can take a while. Default is false

releaseDebugFiles() : Stops the symbolloader from processing any debug files and releases what it had open

errorOnLookupFailure(state): If set to true (default) address lookups in stringform will raise an error if it can not be looked up. This includes symbolnames that are not defined and pointers that are bad. If set to false it will return 0 in those cases
  (Useful for pointers that don't work 100% of the time)
6.4+:Returns the original state

waitforsymbols(state): If set to true looking up a symbol will wait for the symbol to be loaded(default true)

generateAPIHookScript(address:string, addresstojumpto:string, addresstogetnewcalladdress:string OPT, ext:string OPT, targetself:boolean OPT) : Generates an auto assembler script which will hook the given address when executed
assemble(line, address OPTIONAL, assemblePreference OPTIONAL, skipRangeCheck OPTIONAL): assembles a single line of code and returns a byte array of the generated code.  
  address is the address to assemble this code at
  assemblePreference: apNone=0, apShort=1, apLong=2, apFar=3
  skipRangeCheck is a boolean.  Which will skip range checks if true and just assembles it, no matter of how wrong the result will be   
autoAssemble(text, targetself OPTIONAL, disableInfo OPTIONAL) : runs the auto assembler with the given text. Returns true on success, with as secondary a table you can use when disabling (if targetself is set it will assemble into Cheat Engine itself). If disableInfo is provided the [Disable] section will be handled
autoAssemble(text, disableInfo OPTIONAL)

autoAssembleCheck(text, enable, targetself) : Checks the script for syntax errors. Returns true on succes, false with an error message on failure

compile(text, address OPTIONAL, targetself OPTIONAL) : Compiles C code and returns a table with the addresses of the symbols on success, or nil with a secondary result containing the errormessage
compile({indexedtable containing scripts}, address OPTIONAL, targetself OPTIONAL) ) : ^ but allows multiple scripts to be compiled into one
compileFiles({filelist}, address OPTIONAL, targetself OPTIONAL) ): ^ but takes an indexed list of files
compileTCCLib() - Compiles the TCC library functions some C code may need to function internally

addCIncludePath(path) : Adds an extra default include path for the compile() function
removeCIncludePath(path) : Removes a specific path previously added with addCIncludePath

compileCS(text, {references}, coreAssembly OPTIONAL) - Compiles c# code and returns the autogenerated filename. references is a list of c# assemblies this code may reference. This file will be deleted when CE closes (or next time another CE closes and it's not in use anymore).  Note: This requires .NET 4 to be installed, even if the target is mono.  Tip: Handy with injectDotNetDLL
dotNetExecuteClassMethod(pathtodll, namespace, classname, methodname, parameters: string): integer - Inside CE, call a method in a .NET class declared as : public static int methodname(string parameters)  For the target process version, look into injectDotNetDLL



registerEXETrainerFeature(FeatureName:String, function():table): adds a new feature to the exe trainer generator window, and calls your function when the user builds an .exe trainer.  The function should return a table with table entries: PathToFile and RelativePath.
  example output:
    [1]: 
      PathToFile=c:\cefolder\autorun\mycode.lua
      RelativePath="autorun\"

    [2]: 
      PathToFile=c:\cefolder\autorun\dlls\mycode.lua
      RelativePath="autorun\mylib.dll"

Note: This runs AFTER the table has been packaged already

                  
unregisterEXETrainerFeature(id)


registerAutoAssemblerCommand(command, function(parameters, syntaxcheckonly)): Registers an auto assembler command to call the specified function. The command will be replaced by the string this function returns when executed. The function can be called twice. Once for syntax check and symbol lookup(1), and the second time for actual execution by the assembler(2) if it has not been removed in phase1.
  Note: The callback function can return multiple values
  Nil, <String>: Will raise an error with the given string
  MultilineString: Replaces the line in the script with the given strings.


 If the function returns nil, and as secondary parameter a string, this will make the auto assembler fail with that error

unregisterAutoAssemblerCommand(command)


registerLuaFunctionHighlight(functionname): Makes the lua highlighter show the functionname as a functionkeyword
unregisterLuaFunctionHighlight(functionname): Removes the given name from showing up as a functionkeyword


registerSymbolLookupCallback(function(string):integer, location): ID  6.4+
  Registers a function to be called when a a symbol is parsed
  Location determines at what part of the symbol lookup the function is called
    slStart: The very start of a symbol lookup. Before tokenization
    slNotInt: Called when it has been determined it's not a hexadecimal only string. Before tokenization
    --The following locations can be called multiple times for one string as they are called for each token and appended token
    slNotModule: Called when it has been determined the current token is not a modulename
    slNotUserdefinedSymbol: Called when it has been determined it's not a userdefined symbol
    slNotSymbol: Called when it has been determined it's not a symbol in the symbollist
    slFailure: Called when it has no clue what the given string is

    Note: slNotSymbol and slFailure are similar, but failure comes only if there's no token after the current token that can be concatenated. Else slNotSymbol will loop several times till all tokens make up the full string


  Return an Integer with the corresponding address if you found it. Nil or 0 if you didn't.

unregisterSymbolLookupCallback(ID): Removes the callback


registerAddressLookupCallback(function(integer):string): ID
  Registers a function to be called when the name of an address is requested

unregisterAddressLookupCallback(ID): Removes the callback

registerGlobalStructureListUpdateNotification(function(sender)): ID -  Calls the given function each time the list is updated
unregisterGlobalStructureListUpdateNotification(id) - removes the callback with the given ID


registerStructureAndElementListCallback(function StructureListCallback(), function elementlistcallback(id1,id2) ) : Registers a function to be called when a structure needs to be dissected 
  function StructureListCallback() will be a function that returns an array of list of structures in table format
  the entries are build up as:
    name: string - name of the structure
    id1: integer - id you can use for whatever(e.g moduleid). It will be passed on to elementlistcallback when this structure is picked
    id2: integer - id you can use for whatever(e.g structureid inside the module). It will be passed on to elementlistcallback when this structure is picked

  
  function elementlistcallback(id1,id2) will be a function that returns an array of structure elements in table format
  the entries are build up as:
    name: string
    offset: integer
    vartype: variabletype (look up vtByte, vtWord, etc..)

  tip: If you return an empty table the structure will not be created. You can use this to create the structure layout yourself and register that instead

unregisterStructureAndElementListCallback(ID)


registerStructureDissectOverride(function(structure, baseaddress): table):
  same as onAutoGuess, but is called by the structure dissect window when the user chooses to let cheat engine guess the structure for him.
  Use the structure object to fill it in
  Return true if you have filled it in, or false or nil if you did not

  Tip: Use inputQuery to ask the user the size if your function doesn't do that automatically


unregisterStructureDissectOverride(ID)

registerStructureNameLookup(function(address): name, address OPTIONAL):
  Registers a function to be called when dissect data asks the user for the name of a new structure define. If you have code that can look up the name of a structure, and perhaps also the real starting point, you can use this to improve the data dissection.

unregisterStructureNameLookup(ID)

registerAssembler(function(address, instruction):bytetable)
  Registers a function to be called when the single line assembler is invoked to convert an instruction to a list of bytes
  Return a bytetable with the specific bytes, or nil if you wish to let another function, or the original x86 assembler to assemble it

unregisterAssembler(ID): Unregisters the registered assembler

registerAutoAssemblerPrologue(function(script, syntaxcheck), postAOB:boolean=false)
  Registers a function to be called when the auto assembler is about to parse an auto assembler script. The script you get is after the [ENABLE] and [DISABLE] tags have been used to strip the script to the according one, but before comment stripping and trimming has occured

  script is a Strings object which when changed has direct effect to the script

unregisterAutoAssemblerPrologue(ID)

registerAutoAssemblerTemplate(name, function(script: TStrings; sender: TFrmAutoInject), shortcut OPTIONAL ): id - Registers an template for the auto assembler. The script parameter is a TStrings object that has a direct connection to the current script. (All script parsing is up to you...).  Returns an ID
unregisterAutoAssemblerTemplate(ID)


generateCodeInjectionScript(script: Tstrings, address: string, farjmp: boolean) - Adds a default codeinjection script to the given script
generateAOBInjectionScript(script: Tstrings, symbolname: string, address: string, commentradius(default 10), farjmp: boolean) - Adds an AOB injection script to the given script
generateFullInjectionScript(script: Tstrings, address: string, commentradius(default 10), farjmp: boolean) - Adds a Full Injection script to the given script

getNextAllocNumber(script: TStrings): integer - scans the given script for alloc(newmem## and returns the next unused newmem number)
addSnapshotAsComment(script: TStrings, address: integer, radius(Default 10)) - creates a comment section for AA scripts that contains a snapshot of the original code
getUniqueAOB(address): AOBString,Offset - Scans for a unique AOB for the given address and returns the AOB as a string, and an offset applied in case the aob returned doesn't start at the given address



showMessage(text) : shows a messagebox with the given text
inputQuery(caption, prompt, initialstring): Shows a dialog where the user can input a string. This function returns the given string, or nil on cancel
showSelectionList(title, caption, stringlist, allowCustomInput OPTIONAL, formname OPTIONAL): integer,string - Shows a menu with the given list. It returns the linenumber (starting at 0) and the selected string.  Linenumber is -1 if the user was allowed to enter custom input

messageDialog(text, type, buttons...) : pops up a messagebox with a specific icon/sound with the specified buttons (mbok, mbyes, ....)
messageDialog(title, text, type, buttons...): ^ but adds a custom title
messageDialog(text) : shows an information dialog with the text

sleep(milliseconds): pauses for the number of specified milliseconds (1000= 1 sec...)

getProcesslist(Strings): Fills a Strings inherited object with the processlist of the system. Format: %x-pidname
getProcesslist(): Returns a table with the processlist  (pid - name )
getWindowlist(Strings): Fills a Strings inherited object with the top-window list of the system. Format: %x-windowcaption
getWindowlist(): Returns a table with the windowlist (pid - window caption ).  The table is formatted as : {pid,{id,caption}}


getThreadlist(List): fills a List object with the threadlist of the currently opened process. Format: %x
getHandleList(filter OPTIONAL): returns a table with all the handles in the system(Filter 0=everything, 1=target process handles only, 2 handles to target process, 3 handles to ce process).  Each handle entry has fields: ProcessID, ObjectTypeIndex, HandleAttributes, HandleValue, Object and GrantedAccess.  Note: Object will be invalid if you use the 32-bit CE on a 64-bit windows

closeRemoteHandle(handle, processid OPTIONAL): Closes the handle of a process.

duplicateHandle(handle): Duplicates the provided CE based handle into the target process (You still need tell the target about this handle, like an injected dll data block)
duplicateHandle(handle, Mode (0/1) ): If mode is 0 then it's the same as just duplicateHandle(handle), but if it's 1 it duplicates the target process handle into CE's process
duplicateHandle(handle, fromPID, toPID): Copies the handle from the given process to the target process. 


function onOpenProcess(processid):
  If this function is defined it will be called whenever cheat engine opens a process.
  Note: The the same process might be opened multiple times in a row internally
  Note 2: This function is called before attachment is fully done. You can call reinitializeSymbolhandler() to force the open to complete, but it will slow down process opens. Alternatively, you could launch a timer which will run when the opening has finished


MainForm.OnProcessOpened: function(processid, processhandle, caption) - Define this if you want to be notified when a new process has been opened. Called only once from the main thread. It is recommended to use this instead of onOpenProcess

function onTableLoad(before): If defined this function will be called twice when a table gets loaded. Once before the loading, and once after.


getOpenedProcessID() : Returns the currently opened process. If none is open, returns 0
getOpenedProcessHandle(): Returns the handle of the currently opened process
getProcessIDFromProcessName(name) : returns a processid
openProcess(processid) : causes cheat engine to open the given processid
openProcess(processname): causes cheat engine to find and open the given process
openFileAsProcess(filename,is64bit OPTIONAL,startaddress OPTIONAL): causes cheat engine to open the file with memory access as if it's a process
getOpenedFileSize(): Returns the file of the opened file
saveOpenedFile(filename OPTIONAL): Saves the changes of the opened file, set filename if you want a different file
setPointerSize(size): Sets the size cheat engine will deal with pointers in bytes. (Some 64-bit processes can only use 32-bit addresses)
getPointerSize() : Gets the current pointersize
setAssemblerMode(int): 0=32-bit, 1=64-bit
pause() : pauses the current opened process
unpause(): resumes the current opened process


getCPUCount(): Returns the number of CPU's
cpuid(EAX,ECX): returns a table with CPUID info (EAX, EBX, ECX, EDX)

gc_setPassive(state: boolean): enables/disables the passive garbage collector
gc_setActive(state: boolean, interval: integer, minsize: integer): enables/disables the active garbage collector and lets you configure the interval and minimim size


getSystemMetrics(index): Retrieves the specified system metric or system configuration setting
(https://msdn.microsoft.com/en-us/library/windows/desktop/ms724385.aspx)

getScreenDPI(): Returns the Dots/Pixels Per Inch of the screen
getScreenHeight(): Returns the screen height
getScreenWidth(): Returns the screen  width

getWorkAreaHeight(): Returns the work area height
getWorkAreaWidth(): Returns the work area width

invertColor(color): Returns the inverted color
getScreenCanvas(): Returns a Canvas object you can use to write to the screen (Note: Not as useful as you may think)

getPixel(x,y) : returns the rgb value of the pixel at the specific screen coordinate
getMousePos: returns the x,y coordinates of the mouse
setMousePos(x,y): sets the mouse position

isKeyPressed(key) : returns true if the specified key is currently pressed
keyDown(key) : causes the key to go into down state
keyUp(key) :causes the key to go up
doKeyPress(key) : simulates a key press

mouse_event(flags, x OPTIONAL, y OPTIONAL, data OPTIONAL, extra OPTIONAL) - The mouse_event windows API.  Check MSDN for information on how to use

shortCutToText(shortcut): Returns the textual representation of the given shortut value (integer) (6.4+)
textToShortCut(shortcutstring): Returns an shortcut integer that the given string represents.  (6.4+)

convertKeyComboToString(key1,...): Returns a string representation of the given keys like the hotkey handler does
convertKeyComboToString({key1,...}): ^


outputDebugString(text): Outputs a message using the windows OutputDebugString message. You can use tools like dbgview to read this. Useful for testing situations where the GUI freezes

shellExecute(command, parameters OPTIONAL, folder OPTIONAL, showcommand OPTIONAL): Executes a given command
runCommand(exepath, parameters or {parameter1, parameter2}, pathtoexecutein OPTIONAL): Executes the given command and returns the output of the command as a string and the exitcode as an integer (Should not open a console window) If pathtoexecutein is not provided the path will be the current working directory of CE


getTickCount() :  Returns the current tickcount since windows was started. Each tick is one millisecond
processMessages() :  Lets the main eventhandler process the new messages (allows for new button clicks)
inMainThread(): Returns true if the current code is running inside the main thread (6.4+)
integerToUserData(int):  Converts a given integer to a userdata variable
userDataToInteger(UserDataVar):  Converts a given userdata variable to an integer

synchronize(function(...), ...): Calls the given function from the main thread. Returns the return value of the given function
queue(function(...),...): calls the given function from the main thread. Does not wait for the result. Note: Be sure to synchronize and call checkSynchronize() before freeing the calling thread.  Note2: The queue will be emptied and NOT executed if the thread is freed. So it's not recommended without setting freeOnTerminate to false
checkSynchronize(timeout OPTIONAL): Call this from an infinite loop in the main thread when using threading and synchronize calls. This will execute any queued synchronize calls

writeToClipboard(text):  Writes the given text to the clipboard
readFromClipboard():  Reads the text from the clipboard



speedhack_setSpeed(speed) : Enables the speedhack if needed and sets the specific speed
speedhack_getSpeed(): Returns the last set speed

injectDLL(filename, skipsymbolreloadwait OPTIONAL): Injects a dll or dylib, and returns true on success
injectLibrary(filepath, skipsymbolreloadwait OPTIONAL): Same as injectDLL, just sounds better

injectDotNetDLL(dllpath, FullClassName, MethodName,parameterstring, timeout optional)

executeCode(address, parameter OPTIONAL, timeout OPTIONAL) : address - Executes a stdcall function with 1 parameter at the given address in the target process  and wait for it to return. The return value is the result of the function that was called
executeCodeLocal(addres, parameter OPTIONAL): address -  Executes a stdcall function with 1 parameter at the given address in the target process. The return value is the result of the function that was called

executeCodeEx(callmethod, timeout, address, {type=x,value=param1} or param1,{type=x,value=param2} or param2,...)
callmethod: 0=stdcall, 1=cdecl
  timeout: Number of milliseconds to wait for a result. nil or -1, infitely. 0 is no wait (will not free the call memory, so beware of it's memory leak)
  address: Address to execute
  {type,value} : Table containing the value type, and the value
    {
    type: 0=integer (32/64bit) can also be a pointer
          1=float (32-bit float)
          2=double (64-bit float)
          3=ascii string (will get converted to a pointer to that string)
          4=wide string (will get converted to a pointer to that string)
     
    value: anything base type that lua can interpret
    }
  if just param is provided CE will guess the type based on the provided type

executeMethod(callmethod, timeout, address, {regnr=0..15,classinstance=xxxxxxxx} or classinstance, {type=x,value=param1} or param1, {type=x,value=param2} or param2,...) - Executes a method.
  regnr can be:
    0: R/EAX
    1: R/ECX
    2: R/EDX
    3: R/EBX
    4: R/ESP
    5: R/EBP
    6: R/ESI
    7: R/EDI
    8: R8
    9: R9
    10: R10
    11: R11
    12: R12
    13: R13
    14: R14
    15: R15
  

  If no register number is provided then ECX(1) is picked
  If instance is nil it is the same as executeCodeEx

executeCodeLocalEx(address, {type=x,value=param1} or param1,{type=x,value=param2} or param2,...)
  Calls a function using the given callmethod and parameters
  
  
  If a direct parameter is given instead of a table entry describing the type, CE will 'guess' the type it is

  Returns the E/RAX value returned by the called function (if no timeout or other interruption)





loadPlugin(dllnameorpath): Loads the given plugin. Returns nil on failure. On success returns a value of 0 or greater

loadFontFromStream(memorystream) : Loads a font from a memory stream and returns an id (handle) to the font for use with unloadLoadedFont
unloadLoadedFont(id)




onAutoGuess(function) :
  Registers a function to be called whenever autoguess is used to predict a variable type
  function override (address, ceguess): Return the variable type you want it to be. If no change, just return ceguess




closeCE() : just closes ce
hideAllCEWindows() : makes all normal ce windows invisible (e.g trainer table)
unhideMainCEwindow() : shows the main cheat engine window

getAutoAttachList(): returns the AutoAttach StringList object. It can be controlled with the stringlist_ routines (it's not recommended to destroy this list object)


AOBScan(x,x,x,x,...):
scans the currently opened process and returns a StringList object containing all the results. don't forget to free this list when done
Bytevalue of higher than 255 or anything not an integer will be seen as a wildcard
AOBScan(aobstring, OPTIONAL protectionflags, OPTIONAL alignmenttype, OPTIONAL alignmentparam): see above but here you just input one string
AOBScanUnique(aobstring, OPTIONAL protectionflags, OPTIONAL alignmenttype, OPTIONAL alignmentparam)- Integer: scans for the aobstring and returns the first result it finds and nil if nothing is found. Make sure it is unique as it will return the first result found as it will return any random match
AOBScanModuleUnique(modulename, aobstring, OPTIONAL protectionflags, OPTIONAL alignmenttype, OPTIONAL alignmentparam)- Integer : scans for the aobstring in the designated module




Regarding eventhandlers. You can initialize them using both a string of a functionname or the function itself.
If initialized using a function itself it won't be able to get saved in the table


allocateMemory(size, BaseAddress OPTIONAL, Protection OPTIONAL): Allocates some memory into the target process
deAlloc(address, size OPTIONAL): Frees allocated memory

allocateSharedMemory(name, size):
  Creates a shared memory object in the attached process of the given size if it doesn't exist yet. If size is not given and there is no shared region with this name then the default size of 4096 is used
  It then maps this shared memory block into the currently targeted process. It returns the address of this mapped region in the target process.  Keep in mind that a process can map the same block multiple times, so keep track of your assignments
allocateSharedMemoryLocal(name, size): Same as allocateSharedMemory but then for the Cheat Engine process itself


createSection(size) : Creates a 'section' in memory
mapViewOfSection(section, preferedBaseAddress OPTIONAL): Maps the section to memory
unMapViewOfSection(baseaddress): Unmaps a section from memory


getForegroundProcess() : Returns the processID of the process that is currently on top


findWindow(classname OPTIONAL, caption OPTIONAL): windowhandle - Finds a window with the given classname and/or windowname
getWindow(windowhandle, command) : windowhandle - Gets a specific window based on the given window (Check MSDN getWindow for the command description)
getWindowCaption(windowhandle) : string - Returns the caption of the window
getWindowClassName(windowhandle): string - Returns the classname of the window
getWindowProcessID(windowhandle): processid - Returns the processid of the process this window belongs to
getForegroundWindow() - windowhandle : Returns the windowhandle of the topmost window

sendMessage(hwnd, msg, wparam, lparam): result - Sends a message to a window. Those that wish to use it, should know how to use it (and fill in the msg id's yourself)
hookWndProc(hwnd, function(hwnd, msg, wparam, lparam), ASYNC: BOOL) - Hooks a window's wndproc procedure. The given function will receive all functions.  Return 0 to say you handled it. 1 to let the default windows handler deal with it. Or anything else, to let the original handler deal with it.  Besides the return value, you can also return hWnd, Msg, lParam and wParam, modified, or nil for the original value.  Set ASYNC to true if you don't want to run this in the CE GUI. (faster, but you can't touch gui objects)
unhookWndProc(hwnd) - call this when done with the hook.  Not calling this will result in the process window behaving badly when you exit CE


cheatEngineIs64Bit(): Returns true if CE is 64-bit, false if 32-bit
targetIs64Bit(): Returns true if the target process is 64-bit, false if 32-bit
targetIsX86(): Returns true if the target process is x86 based
targetIsArm(): Returns true if the target process is arm based 
targetIsAndroid(): Returns true if the target process is running on the Android OS

getCheatEngineDir(): Returns the folder Cheat Engine is located at
getCheatEngineProcessID(): Returns the processid of cheat engine

getAutorunPath() : Returns the autorun path


disassemble(address): Disassembles the given address and returns a string in the format of "address - bytes - opcode : extra"
splitDisassembledString(disassembledstring): Returns 4 strings. The address, bytes, opcode and extra field

getInstructionSize(address): Returns the size of an instruction (basically it disassembles the instruction and returns the number of bytes for you)
getPreviousOpcode(address): Returns the address of the previous opcode (this is just an estimated guess)

disassembleBytes(hexadecimalbytestring or {bytetable},address OPTIONAL) : Disassembles the given bytes and returns the result. 

beep() : Plays the fabulous beep/ping sound!
playSound(stream, waittilldone OPTIONAL): Plays the given memorystream containing a .WAV formatted memory object. If waittilldone is true the script will stop executing till the sound has stopped
playSound(tablefile, waittilldone OPTIONAL) : Takes the memorystream from the tablefile and plays it.
  There are two tablefiles predeclared inside cheat engine "Activate" and "Deactivate" . You are free to use or override them

speak(text, waittilldone OPTIONAL): Speaks a given text.  If waitTillDone is true the thread it's in will be frozen till it is done
speak(text, flags): Speaks a given text using the given flags. https://msdn.microsoft.com/en-us/library/speechplatform_speakflags.aspx
speakEnglish(text, waittilldone OPTIONAL) - will try the English voice by wrapping the given text into an XML statement specifying the english voice. Will not say anything if no Egnlish language is present. Do not use SPF_IS_NOT_XML flag and SPF_PARSE_SSML won't work in this situation



printf(...) : Same as print(string.format(...))
setProgressState(state): Sets the state of the cheatengine task in the taskbar (windows only) values: tbpsNone, tbpsIndeterminate, tbpsNormal, tbpsError, tbpsPaused
setProgressValue(current, max): Sets the state of the cheatengine task progress status


getUserRegistryEnvironmentVariable(name): string - Returns the environment variable stored in the user registry environment
setUserRegistryEnvironmentVariable(name, string) - Sets the environment variable stored in the user registry environment
is when you've changed the environment variables in the registry. This will cause at least the shell to update so you don't have to reboot. (It's always recommended to reboot though)

stringToMD5String(string): Returns an md5 hash string from the provided string


getFormCount() : Returns the total number of forms assigned to the main CE application
getForm(index): Returns the form at the specific index

registerFormAddNotification(function(form)): Registers a function to be called when a form is attached to ce's form list. This is useful for extentions that add new functionality to certain existing forms. It returns an object you can use with unregisterFormAddNotification
unregisterFormAddNotification(Object)


getSettingsForm(): Returns the main settings form
getMemoryViewForm() : Returns the main memoryview form class object which can be accessed using the Form_ class methods and the methods of the classes it inherits from. There can be multiple memory views, but this will only find the original/base
getMainForm() : Returns the main form class object which can be accessed using the Form class methods and the methods of the classes it inherits from

getApplication() : Returns the application object. (the titlebar)
getAddressList() : Returns the cheat table addresslist object
getFreezeTimer() : Returns the freeze timer object
getUpdateTimer() : Returns the update timer object



setGlobalKeyPollInterval(integer): Sets the global keypoll interval. The interval determines the speed of how often CE checks if a key has been pressed or not. Lower is more accurate, but eats more cpu power
setGlobalDelayBetweenHotkeyActivation(integer): Sets the minimum delay between the activation of the same hotey in milliseconds. Affects all hotkeys that do not set their own minimum delay

getXBox360ControllerState(ControllerID OPTIONAL) : table - Fetches the state of the connected xbox controller. Returns a table containing the following fields on success:
    ControllerID : The id of the controller (between 0 and 3)
    PacketNumber : The packet id of the state you see. (use to detect changes)
    GAMEPAD_DPAD_UP : D-PAD Up (boolean)
    GAMEPAD_DPAD_DOWN: D-PAD Down (boolean)
    GAMEPAD_DPAD_LEFT: D-PAD Left (boolean)
    GAMEPAD_DPAD_RIGHT: D-PAD Right (boolean)
    GAMEPAD_START: Start button (boolean)
    GAMEPAD_BACK: Back button (boolean)
    GAMEPAD_LEFT_THUMB: Left thumb stick down (boolean)
    GAMEPAD_RIGHT_THUMB: Right thumb stick down (boolean)

    GAMEPAD_LEFT_SHOULDER: Left shoulder button (boolean)
    GAMEPAD_RIGHT_SHOULDER: Right shoulder button (boolean)

    GAMEPAD_A: A button (boolean)
    GAMEPAD_B: B button (boolean)
    GAMEPAD_X: X button (boolean)
    GAMEPAD_Y: Y button (boolean)

    LeftTrigger: Left trigger (integer ranging from 0 to 255)
    RightTrigger: Right trigger (integer ranging from 0 to 255)

    ThumbLeftX: Horizontal position of the left thumbstick (-32768 to 32767)
    ThumbLeftY: Verital position of the left thumbstick (-32768 to 32767)
    ThumbRightX: Horizontal position of the right thumbstick (-32768 to 32767)
    ThumbRightY: Vertical position of the right thumbstick (-32768 to 32767)  


setXBox360ControllerVibration(ControllerID, leftMotor, rightMotor) - Sets the speed of the left and right vibrating motor inside the controller. Range (0 to 65535 where 0 is off)



undefined property functions. Not all properties of all classes have been explicitly exposed to lua, but if you know the name of a property of a specific class you can still access them (assuming they are declared as published in the pascal class declaration)
getPropertyList(class) : Returns a stringlist object containing all the published properties of the specified class (free the list when done) (Note, not all classed with properties have 'published' properties. E.g: stringlist)
setProperty(class, propertyname, propertyvalue) : Sets the value of a published property of a class (Won't work for method properties)
getProperty(class, propertyname) : Gets the value of a published property of a class (Won't work for method properties)
setMethodProperty(class, propertyname, function): Sets the method property to the specific function
getMethodProperty(Class, propertyname): Returns a function you can use to call the original function



registerSymbol(symbolname, address, OPTIONAL donotsave): Registers a userdefined symbol. If donotsave is true this symbol will not get saved when the table is saved
unregisterSymbol(symbolname)

enumRegisteredSymbols(): Returns a table with elements containing {symbolname, address, OPTIONAL {allocsize, processid, donotsave}}

deleteAllRegisteredSymbols() : Deletes all symbols registered with registerSymbols, both in AA and Lua scripts (Does not remove registered symbolLists)


getNameFromAddress(address,ModuleNames OPTIONAL=true, Symbols OPTIONAL=true, Sections OPTIONAL=false): Returns the given address as a string. Registered symbolname, modulename+offset, or just a hexadecimal string depending on what address
inModule(address) : returns true if the given address is inside a module
inSystemModule(address) : returns true if the given address is inside a system module
getCommonModuleList: Returns the commonModuleList stringlist. (Do not free this one)



AOBScan("aobstring", protectionflags OPTIONAL, alignmenttype OPTIONAL, alignmentparam HALFOPTIONAL):
protectionflags is a string.
  X=Executable W=Writable memory C=Copy On Write. Add a + to indicate that flag MUST be set and a - to indicate that that flag MUST NOT be set. (* sets it to don't care)
  Examples:
    +W-C = Writable memory exluding copy on write and doesn't care about the Executable flag
    +X-C-W = Find readonly executable memory
    +W = Finds all writable memory and don't care about copy on write or execute
    "" = Find everything (is the same as "*X*C*W" )


alignmenttype is an integer:
  0=No alignment check
  1=Address must be dividable by alignmentparam
  2=Address must end with alignmentparam
alignmentparam is a string which either holds the value the addresses must be dividable by or what the last digits of the address must be




-debugging

debug variables
EFLAGS
32/64-bit: EAX, EBX, ECX, EDX, EDI, ESI, EBP, ESP, EIP
64-bit only: RAX, RBX, RCX, RDX, RDI, RSI, RBP, RSP, RIP, R8, R9, R10, R11, R12, R13, R14, R15 : The value of the register


Debug related routines:
function debugger_onBreakpoint():
When a breaking breakpoint hits (that includes single stepping) and the lua function debugger_onBreakpoint() is defined it will be called and the global variables EAX, EBX, .... will be filled in
Return 0 if you want the userinterface to be updated and anything else if not (e.g: You continued from the breakpoint in your script)



createProcess(path, parameters OPTIONAL, debug OPTIONAL, breakonentrypoint OPTIONAL) : Creates a process. If debug is true it will be created using the windows debugger and if breakonentry is true it will cause a breakpoint to occur on entrypoint

debugProcess(interface OPT): starts the debugger for the currently opened process (won't ask the user) Optional interface: 0=default, 1=windows debug, 2=VEHDebug, 3=Kerneldebug

debug_isDebugging(): Returns true if the debugger has been started
debug_getCurrentDebuggerInterface() : Returns the current debuggerinterface used (1=windows, 2=VEH 3=Kernel, nil=no debugging active)
debug_canBreak(): Returns true if there is a possibility the target can stop on a breakpoint. 6.4+
debug_isBroken(): Returns true if the debugger is currently halted on a thread
debug_isStepping(): Returns true if the debugger was single stepping an instruction earlier
debug_getBreakpointList(): Returns a lua table containing all the breakpoint addresses
debug_breakThread(threadid): Breaks the thread with the specific threadID (Note: The thread may not break instantly and may have to be awakened first)

debug_addThreadToNoBreakList(threadid): This will cause breakpoints on the provided thread to be ignored
debug_removeThreadFromNoBreakList(threadid): removed the threadid from the list

debug_setBreakpointForThread(threadid, address, size OPTIONAL, trigger OPTIONAL, breakpointmethod OPTIONAL, functiontocall() OPTIONAL) : sets a breakpoint of a specific size at the given address for the specified thread. if trigger is bptExecute then size is ignored. If trigger is ignored then it will be of type bptExecute, which obviously also ignores the size then as well.  (Other triggers are bptAccess and bptWrite)
debug_setBreakpoint(address, size OPTIONAL, trigger OPTIONAL, breakpointmethod OPTIONAL, functiontocall() OPTIONAL) 
debug_setBreakpoint(address, size OPTIONAL, trigger OPTIONAL, functiontocall() OPTIONAL) 
debug_setBreakpoint(address, functiontocall() OPTIONAL)
debug_removeBreakpoint(address) : if the given address is a part of a breakpoint it will be removed
debug_continueFromBreakpoint(continueMethod) : if the debugger is currently waiting to continue you can continue with this. Valid parameters are :co_run (just continue), co_stepinto(when on top of a call, follow it), co_stepover (when on top of a call run till after the call)
debug_getXMMPointer(xmmregnr) :
  Returns the address of the specified xmm register of the thread that is currently broken
  This is a LOCAL Cheat Engine address. Use Local memory access functions to read and modify
  xmmregnr can be 0 to 15 (0 to 7 on 32-bit)


The following routines describe last branch recording. These functions only work when kernelmode debugging is used and using windows XP (vista and later work less effective or not at all because the operating system interferes.  Might also be intel specific. A dbvm upgrade in the future might make this work for windows vista and later)
debug_setLastBranchRecording(boolean): When set the Kernel debugger will try to record the last branch(es) taken before a breakpoint happens
debug_getMaxLastBranchRecord() : Returns the maximum branch record your cpu can store (-1 if none)
debug_getLastBranchRecord(index): Returns the value of the Last Branch Record at the given index (when handling a breakpoint)


function debugger_onModuleLoad(modulename, baseaddress) :
this routine is called when a module is loaded. Only works for the windows debugger
return 1 if you want to cause the debugger to break


Changing registers:
When the debugger is waiting to continue you can change the register variables. When you continue those register values will be set in the thread's context


If the target is currently stopped on a breakpoint, but not done through an onBreakpoint function. The context won't be set.
You can get and set the context back with these functions before execution continues"
debug_getContext(BOOL extraregs) - Fills the global variables for the regular registers. If extraregs is true, it will also set FP0 to FP7 and XMM0 to XMM15
debug_setContext(BOOL extraregs)
debug_updateGUI() - Will refresh the userinterface to reflect the new context if the debugger was broken



detachIfPossible() : Detaches the debugger from the target process (if it was attached)

getComment(address) : Gets the userdefined comment at the specified address
setComment(address, text) : Sets a userdefined comment at the specifried address. %s is used to display the autoguess value if there is one
getHeader(address) : Gets the userdefined header at the specified address
setHeader(address) : Sets the userdefined header at the specified address

registerBinUtil(config) Registers a binutils toolset with CE (for assembling and disassembling in other cpu instruction sets)
config is a table containing several fields that describe the tools, and lets you specify extra parameters

Name : The displayed name in the binutils menu in memview
Description: The description for this toolset
Architecture: used by the objdump -m<architecture>  (required)
ASParam : extra parameters to pass on to AS (optional)
LDParam : extra parameters to pass on to LD
OBJDUMPParam: extra parameters to pass on to OBJDUMP
OnDisassemble: a lua function that gets called each time an address is disassembled. The return value will be passed on to OBJDUMP
Path: filepath to the binutils set
Prefix: prefix  (e.g: "arm-linux-androideabi-")
DisassemblerCommentChar: Depending on which target you're disassembling, the comment character  can be different. (ARM=";"  x86='#' )





class helper functions
inheritsFromObject(object): Returns true if given any class
inheritsFromComponent(object): Returns true if the given object inherits from the Component class
inheritsFromControl(object): Returns true if the given object inherits from the Control class
inheritsFromWinControl(object): Returns true if the given object inherits from the WinControl class

createClass(classname): Creates an object of the specified class (Assuming it's a registered class and has a default constructor)
createComponentClass(classname, owner): Creates an object of the specified component inherited class 


Class definitions
Object class: (Inheritance: )
Properties:
  ClassName: String - The name of class (Read only)
Methods:
  getClassName(): Returns the classname
  fieldAddress(fieldname: string): Returns the address of the specific field
  methodAddress(methodname: string)
  methodName(address: integer)
  destroy(): Destroys the object



Component Class: (Inheritance: Object)
properties
  ComponentCount: Integer - Number of child components . Readonly
  Component[int]: Component - Array containing the child components. Starts at 0. Readonly
  ComponentByName[string]: Component - Returns a component based on the name. Readonly
  Name: string - The name of the component
  Tag: integer - Free to use storage space. (Useful for id's)
  Owner: Component - Returns the owner of this object. Nil if it has none

methods
  getComponentCount() : Returns the number of components attached to his component
  getComponent(index) : Returns the specific component
  findComponentByName(name) : Returns the component with this name
  getName() : Return the name
  setName(newname) : Changes the name
  getTag() : Sets an integer value. You can use this for ID's
  setTag(tagvalue) : Get the tag value
  getOwner() : Returns the owner of this component



Control Class: (Inheritance: Component->Object)
properties:
  Caption: string - The text of a control
  Top : integer - The x position
  Left : integer - The y position
  Width : integer - The width of the control
  Height : integer - The height of the control
  ClientWidth: integer - The usable width inside the control (minus the borders)
  ClientHeight: integer - The usable height the control (minus the borders)
  Align: AlignmentOption - Alignment of the control
  Enabled: boolean - Determines if the object is usable or greyed out
  Visible: boolean - Determines if the object is visible or not
  Color: ColorDefinition/RGBInteger - The color of the object. Does not affect the caption
  RGBColor: RGBInteger - The color of the object in RGB formatting
  Parent: WinControl - The owner of this control
  PopupMenu: PopupMenu - The popup menu that shows when rightclicking the control
  Font: Font - The font class associated with the control
  OnClick: function(sender) - The function to call when a button is pressed
  OnChangeBounds:function(sender) - Called when the size or position of the control changes

methods:
  getLeft()
  setLeft(integer)
  getTop()
  setTop(integer)
  getWidth()
  setWidth(integer)
  getHeight()
  setHeight()
  setCaption(caption) : sets the text on a control. All the GUI objects fall in this category
  getCaption() : Returns the text of the control
  setPosition(x,y): sets the x and y position of the object base don the top left position (relative to the client array of the owner object)
  getPosition(): returns the x and y position of the object (relative to the client array of the owner object)
  setSize(width,height) : Sets the width and height of the control
  getSize() : Gets the size of the control
  setAlign(alignmentoption): sets the alignment of the control
  getAlign(alignmentoption): gets the alignment of the control
  getEnabled() : gets the enabled state of the control
  setEnabled(boolean) : Sets the enabled state of the control
  getVisible() : gets the visible state of the control
  setVisible(boolean) : sets the visible state of the control
  getColor() : gets the color
  setColor(rgb) : Sets the color
  getParent() : Returns nil or an object that inherits from the Wincontrol class
  setParent(wincontrol) : Sets the parent for this control
  getPopupMenu()
  setPopupMenu()
  getFont():  Returns the Font object of this object
  setFont():  Assigns a new font object. (Not recommended to use. Change the font object that's already there if you wish to change fonts)
  repaint(): Invalidates the graphical area of the control and forces and update
  refresh() : updates the control (usually a repaint)
  update() : Only updates the invalidated areas
  setOnClick(functionnameorstring) : Sets the onclick routine
  getOnClick(): Gets the onclick function
  doClick():  Executes the current function under onClick
  bringToFront(): Changes the z-order of the control so it'd at the top
  sendToBack(): Changes the z-order of the control so it'd at the back
  screenToClient(x,y): Converts screen x,y coordinates to x,y coordinates on the control
  clientToScreen(x,y): Converts control x,y coordinates to screen coordinates


GraphicsObject : (GraphicsObject->Object)



Region Class : (Region->GraphicsObject->Object)
createRegion(): Created an empty region

properties
-
methods
  addRectangle(x1, y1, x2, y2): Adds a rectangle to the region
  addPolygon(tablewithcoordinates): Adds an array of 2D locations. (example : {{0,0},{100,100}, {0,100}} for a triangle )



WinControl Class: (Inheritance: Control->Component->Object)
properties
  Handle: Integer - The internal windows handle
  DoubleBuffered: boolean - Graphical updates will go to a offscreen bitmap which will then be shown on the screen instead of directly to the screen. May reduce flickering
  ControlCount : integer - The number of child controls of this wincontrol
  Control[] : Control - Array to access a child control
  OnEnter : function - Function to be called when the WinControl gains focus
  OnExit : function - Function to be called when the WinControl loses focus

methods
  getControlCount()  Returns the number of Controls attached to this class
  getControl(index) : Returns a WinControl class object
  getControlAtPos(x,y):  Gets the control at the given x,y position relative to the wincontrol's position
  canFocus(): returns true if the object can be focused
  focused(): returns boolean true when focused
  setFocus(): tries to set keyboard focus the object
  setShape(Region): Sets the region object as the new shape for this wincontrol
  setShape(Bitmap):
  setOnEnter(function) : Sets an onEnter event. (Triggered on focus enter)
  getOnEnter()
  setOnExit(function) : Sets an onExit event. (Triggered on lost focus)
  getOnExit()
  setLayeredAttributes(Key, Alpha, Flags) : Sets the layered state for the control if possible (Only Forms are supported in in windows 7 and earlier)
      flags can be a combination of LWA_ALPHA and/or LWA_COLORKEY
      See msdn SetLayeredWindowAttributes for more information




MenuItem class(Inheritance: Component->Object)
createMenuItem(ownermenu) : Creates a menu item that gets added to the owner menu

properties
  Caption : String - Text of the menu item
  Shortcut : string - Shortcut in textform to trigger the menuitem
  Count : integer - Number of children attached to this menuitem
  Menu: Menu - The menu this item resides in
  Parent: MenuItem - The menuitem this item hangs under
  MenuIndex: integer - The position this menu item is in it's parent
  ImageList: ImageList
  ImageIndex: integer - Which image of the attached ImageList to show
  Item[] : Array to access each child menuitem
  [] : Item[]
  OnClick: Function to call when the menu item is activated
  FontColor: Color of the font. (Only works when in dark mode)

methods
  getCaption() : Gets the caption of the menu item
  setCaption(caption) : Sets the caption of the menu item
  getShortcut(): Returns the shortcut for this menu item
  setShortcut(shortcut): Sets the shortcut for this menuitem. A shortcut is a string in the form of ("ctrl+x")
  getCount()
  getItem(index) : Returns the menuitem object at the given index
  add(menuitem) : Adds a menuItem as a submenu item
  insert(index, menuitem): Adds a menuItem as a submenu item at the given index
  delete(index)
  clear() - Deletes all children under this menuitem (frees the menu item, so it's gone)
  setOnClick(function) : Sets an onClick event
  getOnClick()
  doClick(): Executes the onClick method if one is assigned



Menu Class: (Inheritance: Component->Object)
properties
  Items : MenuItem - The base MenuItem class of this menu (readonly)
methods
  getItems() : Returns the main MenuItem of this Menu

MainMenu Class: (Inheritance: Menu->Component->Object)
createMainMenu(form)
  The mainmenu is the menu at the top of a window

PopupMenu Class: (Inheritance: Menu->Component->Object)
createPopupMenu(owner)
  The popup menu is the menu that pops up when showing the (rightclick) context of an control


Strings Class: (Inheritance : Object) (Mostly an abstract class)
properties
  LineBreak: String - the character(s) to count as a linebreak
  Text : String - All the strings in one string
  Count: Integer - The number of strings in this list
  String[]: String - Array to access one specific string in the list
  Data[]: Integer - Array to access the data of a specific string in the list
  [] = String[]

methods
  clear() : Deletes all strings in the list
  add(string, data:integer OPTIONAL) : adds a string to the list. Returns the index
  addText([[strings]]) : adds multiple strings at once
  delete(index) : Deletes a string from the list
  getText() : Returns all the strings as one big string
  setText(string) : Sets the strings of the given strings object to the given text (can be multiline)
  indexOf(string): Returns the index of the specified string. Returns -1 if not found
  insert(index, string): Inserts a string at a specific spot moving the items after it

  getCount(): Returns the number is strings in the list
  remove(string); Removes the given string from the list
  loadFromFile(filename, ignoreencoding OPTIONAL default true) : Load the strings from a textfile. If ignoreEncoding is false then the file will be loaded with the best encoding the loader can guess
  saveToFile(filename) : Save the strings to a textfile

  getString(index) : gets the string at the given index
  setString(index, string) : Replaces the string at the given index
  getData(index) : Returns the integer value stored in the string
  setData(index, integer): Sets the integer value stored in the string

  beginUpdate() : Stops updates from triggering other events (prevents flashing)
  endUpdate(): call after beginUpdate

ImageList Class: (Inheritance: )
List containing images.  Used by several components for images

createImageList(owner OPTIONAL): creates an imagelist object

properties
  Count: integer - Number of images in the list
  DrawingStyle: 'dsFocus', 'dsSelected', 'dsNormal', 'dsTransparent'
  Height: integer
  Width: integer
  Masked: boolean
  Scaled: boolean
  OnChange: function(sender)

methods
  add(bitmap, bitmapmask OPTIONAL):integer - Adds a new bitmap the list and returns the index of the newly added entry
  draw(canvas, x,y, index) - Draws the image at the index to the specific x,y coordinates on the canvas
  getBitmap(index, bitmap, OPTIONAL effect) - Draw the specified image to the provided bitmap. Effect can be :  0=gdeNormal, 1=gdeDisabled, 2=gdeHighlighted, 3=gdeShadowed, 4=gde1Bit


Stringlist Class: (Inheritance : Strings->Object)
createStringlist() : Creates a stringlist class object (for whatever reason, lua strings are probably easier to use)

properties
  Sorted : boolean - Determines if the list should be sorted
  Duplicates : DuplicatesType - Determines how duplicates should be handled when the list is sorted
  CaseSensitive: boolean - Determines if the list is case sensitive or not.

methods
  getDuplicates() : returns the duplicates property
  setDuplicates(Duplicates) : Sets the duplicates property (dupIgnore, dupAccept, dupError)
  getSorted() : returns true if the list has the sorted property
  setSorted(boolean) : Sets the sorted property
  getCaseSensitive() : Returns true if the case sensitive property is set
  setCaseSensitive(boolean): Sets the case sensitive property

Application Class: (Inheritance: CustomApplication->Component->Object)
properties
  Title: The title of cheat engine in the bar
  Icon: The icon of Cheat Engine inn the bar

methods
  bringToFront(): Shows the cheat engine app
  processMessages()
  terminate()
  minimize()


ControlScrollBar Class (Inheritance: Object)
  Increment: Word - The amount the position moves when using the scrollbar arrows
  Page: Word - slider size in pixels
  Smooth: Boolean
  Position: Integer - (limited to 0 to range-page)
  Range: Integer 
  Tracking: Boolean - Gives feedback when the slider is moved
  Visible: Boolean

ScrollingWinControl Class (Inheritance: CustomControl->WinControl->Control->Component->Object)
properties 
  HorzScrollBar: ControlScrollBar
  VertScrollBar: ControlScrollBar

Form Class: (Inheritance: ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)
properties
  DesignTimePPI: integer - the PPI/DPI at the time the form was designed
  AllowDropFiles: boolean - Allows files to be dragged into the form
  ModalResult: integer - The current ModalResult value of the form. Note: When this value gets set the modal form will close
  Menu: MainMenu - The main menu of the form

  OnClose: function(sender) - The function to call when the form gets closed
  OnDropFiles: function(sender, {filenames}) - Called when files are dragged on top of the form. Filenames is an arraytable with the files
  FormState: FormState string ReadOnly - The current state of the form. Possible values: fsCreating, fsVisible, fsShowing, fsModal, fsCreatedMDIChild, fsBorderStyleChanged, fsFormStyleChanged, fsFirstShow, fsDisableAutoSize 


methods
  fixDPI() : Resizes controls and fonts based on the current DPI and the DPI used to create the form. Only use this on forms that are not designed with variable DPI in mind
  centerScreen(); : Places the form at the center of the screen
  hide() : Hide the form
  show() : show the form
  close():  Closes the form. Without an onClose this will be the same as hide
  bringToFront(): Brings the form to the foreground
  showModal() : show the form and wait for it to close and get the close result
  isForegroundWindow(): returns true if the specified form has focus
  setOnClose(function)  : function (sender) : Return a CloseAction to determine how to close the window
  getOnClose() : Returns the function
  getMenu() : Returns the mainmenu object of this form
  setMenu(mainmenu)

  setBorderStyle( borderstyle):  Sets the borderstyle of the window
  getBorderStyle()

  printToRasterImage(rasterimage): Draws the contents of the form to a rasterimage class object

  registerCreateCallback(function(f)): userdata - Registers a function to be called when the form has finished being created
  unregisterCreateCallback(userdata) - removes the specific callback
  registerFirstShowCallback(function(f)): userdata - Registers a function to be called when the form is show the first time
  unregisterFirstShowCallback(userdata) - removes the specific callback
  registerCloseCallback(function(f)): userdata - Registers a function to be called when the form has been closed
  unregisterCloseCallback(userdata) - removes the specific callback

  dragNow() -  Call this on mousedown on any object if you wish that the mousemove will drag the whole form arround. Useful for borderless windows (Dragging will stop when the mouse button is released)
  saveFormPosition({IntegerTable OPTIONAL}) - Saves the current form position and dimensions and an optional list of integer. The name of the form must have been set to a unique name
  loadFormPosition(): boolean, {IntegerTable OPTIONAL, can be nil} - Restores the form position and dimensions. On success returns true and a integer table if that was provided with the save.  The name of the form must have been set to a unique name


CEForm Class: (Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)
createForm(visible OPT): creates a CEForm class object(window) and returns the pointer for it. Visible is default true but can be changed
createFormFromFile(filename): Returns the generated CEform
createFormFromStream(stream): Returns the generated CEform

properties
  DoNotSaveInTable: boolean - Set this if you do not wish to save the forms in the table
methods
  saveToFile(filename): Saves a userdefined form
  saveToStream(s): Saves the userdefined form to the given stream
  getDoNotSaveInTable(): Returns the DoNotSaveInTable property
  setDoNotSaveInTable(boolean): Sets the DoNotSaveInTable property
  saveCurrentStateAsDesign() : Sets the current state of the form as the state that will be saved when the table is saved


TfrmLuaEngine class: (Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)
getLuaEngine() : Returns the main lua engine form object (Creates it if needed)
createLuaEngine() : Creates a new lua engine form object. If there is no main luaengine window, this will become it. 

properties
  mOutput: Memo - Output of the luaengine window
  mScript: SynEdit - Editor for the script

methods


TfrmAutoInject class: (Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)
createAutoAssemblerForm(script: string OPTIONAL): TFrmAutoInject - Spawns an autoassembler window with the optionally provided script

properties
  Assemblescreen: SynEdit - Editor for the script
  TabCount: integer
  TabScript[index]: string

methods
  addTab(): integer
  deleteTab(index)

GraphicControl Class: (Inheritance: Control->Component->Object)
properties
  Canvas: Canvas - The canvas for rendering this control

methods
  getCanvas() : Returns the Canvas object for the given object that has inherited from customControl


PaintBox class: (Inheritance: GraphicControl->Control->Component->Object)
createPaintBox(owner): Creates a Paintbox class object


Label Class: (Inheritance: GraphicControl->Control->Component->Object)
createLabel(owner): Creates a Label class object which belongs to the given owner. Owner can be any object inherited from WinControl


Splitter Class: (Inheritance: CustomControl->WinControl->Control->Component->Object)
createSplitter(owner): Creates a Splitter class object which belongs to the given owner. Owner can be any object inherited from WinControl


Panel Class: (Inheritance: CustomControl->WinControl->Control->Component->Object)
createPanel(owner): Creates a Panel class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Alignment: alignment
  BevelInner: panelBevel
  BevelOuter: panelBevel
  BevelWidth: Integer
  FullRepaint: boolean
methods
  getAlignment() : gets the alignment property
  setAlignment(alignment) : sets the alignment property
  getBevelInner()
  setBevelInner(PanelBevel)
  getBevelOuter()
  setBevelOuter(PanelBevel)
  getBevelWidth()
  setBevelWidth(BevelWidth)
  getFullRepaint()
  setFullRepaint(boolean)



Image Class: (Inheritance: GraphicControl->Control->Component->Object)
createImage(owner): Creates an Image class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Canvas: Canvas - The canvas object to access the picture of the image
  Transparent: boolean - Determines if some parts of the picture are see through (usually based on the bottomleft corner)
  Stretch: boolean - Determines if the picture gets stretched when rendered in the image component
  Picture: Picture - The picture to render

methods
  loadImageFromFile(filename)
  getStretch()
  setStretch(boolean)
  getTransparent()
  setTransparent(boolean)
  getCanvas()
  setPicture(picture)
  getPicture() : Returns the Picture object of this image


Edit Class: (Inheritance: WinControl->Control->Component->Object)
createEdit(owner): Creates an Edit class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Text: string - The current contents of the editfield
  CaretPos: Point - The posaition of the caret
  PasswordChar: string[1] - When not set to char0 this will make the edit field show the character instead of the given text
  SelText: string - The current selected contents of the edit field 
  SelStart: number - The starting index of the current selection (zero-indexed)
  SelLength: number - The length of the current selection. 
  OnChange: function - The function to call when the editfield is changed
  OnKeyPress: function - The function to call for the KeyPress event.
  OnKeyUp: function - The function to call for the KeyUp event.
  OnKeyDown: function - The function to call for the KeyDown event.

methods
  clear()
  copyToClipboard()
  cutToClipboard()
  pasteFromClipboard()
  selectAll()
  select(start, length OPTIONAL)
  selectText(start, length OPTIONAL) : Set the control's current selection. If no length is specified, selects everything after start.
  clearSelection()
  getSelText()
  getSelStart()
  getSelLength()
  getOnChange()
  setOnChange(function)
  getOnKeyPress()
  setOnKeyPress(function)
  getOnKeyUp()
  setOnKeyUp(function)
  getOnKeyDown()
  setOnKeyDown(function)


Memo Class: (Inheritance: Edit->WinControl->Control->Component->Object)
createMemo(owner): Creates a Memo class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Lines: Strings - Strings object for this memo
  WordWrap: boolean - Set if words at the end of the control should go to the next line
  WantTabs: Boolean - Set if tabs will add a tab to the memo. False if tab will go to the next control
  WantReturns: Boolean - Set if returns will send a event or not
  Scrollbars: Scrollstyle - Set the type of ascrollbars to show (ssNone, ssHorizontal, ssVertical, ssBoth,
    ssAutoHorizontal, ssAutoVertical, ssAutoBoth)


methods
  append(string)
  getLines() : returns a Strings class
  getWordWrap()
  setWordWrap(boolean)
  getWantTabs()
  setWantTabs(boolean)
  getWantReturns()
  setWantReturns(boolean)
  getScrollbars()
  setScrollbars(scrollbarenumtype) :
  Sets the scrollbars. Horizontal only takes affect when wordwrap is disabled
  valid enum types:
    ssNone : No scrollbars
    ssHorizontal: Has a horizontal scrollbar
    ssVertical: Has a vertical scrollbar
    ssBoth: Has both scrollbars
    ssAutoHorizontal: Same as above but only shows when there actually is something to scroll for
    ssAutoVertical: " " " " ...
    ssAutoBoth: " " " " ...


SynEdit class: 
createSynEdit(owner,mode OPTIONAL): Creates a synedit object. mode: 0=Lua highlighting, 1=Auto Assembler highlighting
properties
  Lines: Stringlist - Contains the text
  Gutter: Gutter - Gutter object
  ReadOnly: Boolean - Set to true for read only
  SelStart: integer
  SelEnd: integer
  SelText: string
  CanPaste: boolean
  CanRedo: boolean
  CanUndo: boolean
  CharWidth: integer READONLY
  LineHeight: integer READONLY

methods
  CopyToClipboard()
  CutToClipboard()
  PasteFromClipboard()
  ClearUndo()
  Redo()
  Undo()
  MarkTextAsSaved()
  ClearSelection();
  SelectAll();     

ButtonControl Class: (Inheritance: WinControl->Control->Component->Object)


Button Class: (Inheritance: ButtonControl->WinControl->Control->Component->Object)
createButton(owner): Creates a Button class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  ModalResult: ModalResult - The result this button will give the modalform when clicked

methods
  getModalResult(button)
  setModalResult(button, mr)

CheckBox Class: (Inheritance: ButtonControl->WinControl->Control->Component->Object)
createCheckBox(owner): Creates a CheckBox class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Checked: boolean - True if checked
  AllowGrayed: boolean - True if it can have 3 states. True/False/None
  State: checkboxstate - The state. (cbUnchecked=0, cbChecked=1, cbGrayed=2)
  OnChange: function - Function to call when the state it changed

methods
  getAllowGrayed()
  setAllowGrayed(boolean)
  getState(): Returns a state for the checkbox. (cbUnchecked, cbChecked, cbGrayed)
  setState(boolean): Sets the state of the checkbox
  onChange(function)

ToggleBox Class: (Inheritance: CheckBox->ButtonControl->WinControl->Control->Component->Object)
createToggleBox(owner): Creates a ToggleBox class object which belongs to the given owner. Owner can be any object inherited from WinControl

GroupBox Class: (Inheritance: WinControl->Control->Component->Object)
createGroupBox(owner): Creates a GroupBox class object which belongs to the given owner. Owner can be any object inherited from WinControl


RadioGroup class: (Inheritance: GroupBox->WinControl->Control->Component->Object)
createRadioGroup(owner): Creates a RadioGroup class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Items: Strings - Strings derived object containings all the items in the list
  Columns: Integer - The number of columns to split the items into
  ItemIndex: Integer - The currently selected item
  OnClick: Called when the control is clicked

methods
  getRows(): Returns the number of rows
  getItems(): Returns a Strings object
  getColumns(): Returns the nuber of columns
  setColumns(integer)
  getItemIndex()
  setItemIndex(integer)
  setOnClick(function)
  getOnClick()


ListBox Class: (Inheritance: WinControl->Control->Component->Object)
createListBox(owner): Creates a ListBox class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  MultiSelect: boolean - When set to true you can select multiple items
  Items: Strings - Strings derived object containings all the items in the list
  Selected[] - Returns true if the given line is selected. Use Items.Count-1 to find out the max index
  ItemIndex: integer - Get selected index. -1 is nothing selected
  Canvas: Canvas - The canvas object used to render on the object

methods
  clear()
  clearSelection() : Deselects all items in the list
  selectAll(): Selects all items in the list
  getItems(): Returns a strings object
  setItems(Strings): sets a strings object to the listbox
  getItemIndex()
  setItemIndex(integer)
  getCanvas()


Calendar Class: (Inheritance: WinControl->Control->Component->Object)
createCalendar(owner): Creates a Calendar class object which belongs to the given owner. Owner can be any object inherited from WinControl. Valid date is between "September 14, 1752" and "December 31, 9999"

properties
  Date: string - current date of the Calendar, format: yyyy-mm-dd
  DateTime: number - days since December 30, 1899

methods
  getDateLocalFormat - returns current date of the Calendar, format: ShortDateFormat from OS local settings


ComboBox Class: (Inheritance: WinControl->Control->Component->Object)
createComboBox(owner): Creates a ComboBox class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Items: Strings - Strings derived object containings all the items in the list
  ItemIndex: integer - Get selected index. -1 is nothing selected
  Canvas: Canvas - The canvas object used to render on the object

methods
  clear()
  getItems()
  setItems()
  getItemIndex()
  setItemIndex(integer)
  getCanvas()
  getExtraWidth() : Returns the number of pixels not part of the text of the combobox (think about borders, thumb button, etc...)




ProgressBar Class: (Inheritance: WinControl->Control->Component->Object)
createProgressBar(owner): Creates a ProgressBar class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Min: integer - The minimum positionvalue the progressbar can have (default 0)
  Max: integer - The maximum positionvalue the progressbar can have (default 100
  Position: integer - The position of the progressbar
  Step: integer- The stepsize to step by when stepIt() is called

methods
  stepIt() - Increase position with "Step" size
  stepBy(integer) - increase the position by the given integer value
  getMax() - returns the Max property
  setMax(integer) - sets the max property
  getMin() - returns the min property
  setMin(integer)- sets the min property
  getPosition() - returns the current position
  setPosition(integer) - sets the current position
  setPosition2(integer) - sets the current position; without slow progress animation on Win7 and later




TrackBar Class : (Inheritance: WinControl->Control->Component->Object)
createTrackBar(owner): Creates a TrackBar class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Min: integer - Minimal value for the trackbar
  Max: integer - Maximum value for the trackbar
  Position: integer - The current position
  OnChange: function - Function to call when

methods
  getMax()
  setMax(integer)
  getMin(trackbar)
  setMin(trackbar, integer)
  getPosition(progressbar)
  setPosition(progressbar, integer)
  getOnChange()
  setOnChange(function)


CollectionItem Class: (Inheritance: Object)
Base class for some higher level classes. Often used for columns

properties
  ID: integer
  Index: integer - The index in the array this item belong to
  DisplayName: string

methods
  getID()
  getIndex()
  setIndex()
  getDisplayName()
  setDisplayName()





ListColumn class: (Inheritance: CollectionItem->Object)
properties
  AutoSize: boolean
  Caption: string
  MaxWidth: integer
  MinWidth: integer
  Width: integer
  Visible: boolean
methods
  getAutosize()
  setAutosize(boolean)
  getCaption()
  setCaption(caption)
  getMaxWidth()
  setMaxWidth(width)
  getMinWidth()
  setMinWidth(width)
  getWidth()
  setWidth(width)


Collection Class: (Inheritance: Object)

properties
  Count: integer
  Items[index]: CollectionItem
  []=Items[index]

methods
  clear(collection)
  getCount(collection)
  delete(collection, index)


ListColumns class : (Inheritance: Collection->Object)
properties
  Columns[]: Array to access a column
  [] = Columns[]

methods
  add(): Returns a new ListColumn object
  getColumn(index): Returns a ListColum object;
  setColumn(index, listcolumns): Sets a ListColum object (not recommended, use add instead)

ListItem Class : (Inheritance: TObject)
properties
  Caption: boolean - The text of this listitem
  Checked: boolean - Determines if the checkbox is checked (if it has a checkbox)
  SubItems: Strings - The Strings object that hold the subitems
  Selected: boolean - Returns true if selected
  Index: integer - The index in the Items object of the owner of this listitem (readonly)
  ImageIndex: integer - The index in the attached imagelist (LargeImages/SmallImages)
  StateIndex: integer - The index in the attached imagelist (StateImages)
  Owner: ListItems - The ListItems object that owns this ListItem (readonly)
  Data: integer - Read/Write value up to the user to implement

methods
  delete()
  getCaption() : Returns the first columns string of the listitem
  setCaption(string) : Sets the first column string of the listitem
  getChecked() : Returns true if the listitem is checked
  setChecked(boolean): Sets the checkbox of the listbox to the given state
  getSubItems(): Returns a Strings object
  makeVisible(partial): Scrolls the listview so this item becomes visible (Cheat Engine 6.4 and later)
  displayRect(code): returns the displayed rectangle of the listitem. code can be: drBounds(0), drIcon(1), drLabel(2), drSelectBounds(3)
  displayRectSubItem(code): returns the displayed rectangle of the listitem. code can be: drBounds(0), drIcon(1), drLabel(2), drSelectBounds(3)


ListItems class : (Inheritance: TObject)
properties
  Count : Integer - The number of ListItems this object holds (Normally read only, but writable if OwnerData is true in the listview)
  Item[]: ListItem[] - Array to access each ListItem object
  [] = Item[]
methods
  clear()
  getCount()
  getItem(integer) : Return the listitem object at the given index
  add(): Returns a new ListItem object



Listview Class : (Inheritance: WinControl->Control->Component->Object)
createListView(owner): Creates a ListView class object which belongs to the given owner. Owner can be any object inherited from WinControl

properties
  Columns: ListColumns - The Listcolumns object of the listview (Readonly)
  Items: ListItems - The ListItems objects of the listview
  ItemIndex: integer - The currently selected index in the Items object  (-1 if nothing is selected)
  Selected: ListItem - The currently selected listitem (nil if nothing is selected)
  TopItem: ListItem - The first visible item in the listview
  VisibleRowCount: integer - The number of lines currently visible
  Canvas: Canvas - The canvas object used to render the listview  (Readonly)
  AutoWidthLastColumn: Boolean - When set to true the last column will resize when the control resizes
  HideSelection: Boolean - When set to true the selection will not hide when the focus leaves the control
  RowSelect: Boolean - When set to true the whole row will be selected instead of just the first column
  OwnerData: Boolean - When set to true the listview will call the onData function for every line being displayed. Use Items.Count to set the number of virtual lines
  LargeImages: ImageList
  SmallImages: ImageList
  StateImages: ImageList

  OnData: function(sender, ListItem) - Called when a listview with OwnerData true renders a line

  OnCustomDraw: function(Sender, {Top, Left, Bottom, Right}, DefaultDraw Optional): NewDefaultDraw
  OnCustomDrawItem: function(Sender, ListItem, {cdsSelected=true/false(nil), cdsGrayed=true/false(nil), cdsDisabled, cdsChecked, cdsFocused, cdsDefault, cdsHot, cdsMarked, cdsIndeterminate}, DefaultDraw Optional): NewDefaultDraw
  OnCustomDrawSubItem: function(Sender, ListItem, SubItemIndex, {cdsSelected=true/false(nil), cdsGrayed=true/false(nil), cdsDisabled, cdsChecked, cdsFocused, cdsDefault, cdsHot, cdsMarked, cdsIndeterminate}, DefaultDraw Optional): NewDefaultDraw


methods
  clear()
  getColumns() : ListColumns - Returns a ListColumns object
  getItemAt(x,y):ListItem - Returns the ListItem at the given index. nil if nothing
  getItems(): ListItems - Returns a ListItems object
  getItemIndex(): integer -  Returns the currently selected index in the Items object
  setItemIndex(index: integer)- Sets the current itemindex
  getCanvas() : Canvas - Returns the canvas object used to render the listview
  beginUpdate() - Tells the listview to stop updating while you're busy
  endUpdate() - Applies all updates between beginUpdate and endUpdate


HeaderSection class : (Inheritance: CollectionItem)
properties
  Alignment: string - 'taLeftJustify', 'taRightJustify', 'taCenter'
  ImageIndex: imageindex
  MaxWidth: integer
  MinWidth: integer
  Text: String - The text of the headersection
  Width: integer - The width of the headersection
  Visible: boolean - Determines if the headersection is visible
  OriginalIndex: integer - The original index ignoring user reorganization (READONLY)
methods


HeaderSections class : (Inheritance: Collection->TObject)
properties
methods
  add(): THeaderSection - Adds a new header and returns it
  insert(index): THeaderSection - inserts a new header at the index and returns it
  delete(index) - deletes(and frees) the headersection at the given index


TreeNode class : (Inheritance: TObject)
properties
  Text: string - The text of the treenode
  Parent: Treenode - The treenode this object is a child of. (can be nil) (ReadOnly)
  Level: Integer - The level this node is at
  HasChildren: boolean - Set to true if it has children, or you wish it to have an expand sign
  Expanded: boolean - Set to true if it has been expanded
  Count : Integer - The number of children this node has
  Items[]: Treenode - Array to access the child nodes of this node
  [] = Items[]
  Index: Integer - The index based on the parent
  AbsoluteIndex: Integer - The index based on the TreeView's Treenodes object (Items)
  ImageIndex: integer - The image to show from the attached ImageList
  Selected: Boolean - Set to true if currently selected
  MultiSelected: Boolean - Set to true if selected as well, but not the main selected object
  Data: Pointer - Space to store 4 or 8 bytes depending on which version of CE is used
methods
  delete()
  deleteChildren()
  makeVisible()
  expand(recursive:boolean=TRUE OPTIONAL) : Expands the given node
  collapse(recursive:boolean=TRUE OPTIONAL)  : collapses the given node
  getNextSibling(): Returns the treenode object that's behind this treenode on the same level
  getDisplayRect(TextOnly: Boolean=FALSE OPTIONAL): Returns a rect {Left,Top,Right,Bottom} describing the node
  add(text:string): Returns a Treenode object that is a child of the treenode used to create it




TreeNodes class : (Inheritance: TObject)
properties
  Count : Integer - The total number of Treenodes this object has
  Item[]: TreeNode - Array to access each node
  [] = Item[]
methods
  clear()
  getCount()
  getItem(integer) : Return the TreeNode object at the given index (based on the TreeView's Treenodes)
  add(text:string): Returns a new root Treenode object
  insert(treenode, string): Returns a new treenode object that has been inserted before the given treenode
  insertBehind(treenode, string): Returns a new treenode object that has been inserted after the given treenode



Treeview Class : (Inheritance: CustomControl->WinControl->Control->Component->Object)
createTreeView(owner)

properties
  Items: TreeNodes - The Treenodes object of the treeview (ReadOnly)
  Selected: TreeNode - The currently selected treenode

methods
  beginUpdate()
  endUpdate()
  getItems()
  getSelected()
  setSelected()
  fullCollapse()  : Collapses all the nodes, including the children's nodes
  fullExpand() : Expands all the nodes and all their children
  saveToFile(filename): Saves the contents of the treeview to disk
  loadFromFile(filename)



Timer Class : (Inheritance: Component->object)
createTimer(delay, function(...),...):
  Creates a timer object that waits the given delay, executes the given function, and then selfdestructs.  Tip: Don't use the timer after it has ran

createTimer(owner OPT, enabled OPT):
  Creates a timer object. If enabled is not given it will be enabled by default (will start as soon as an onTimer event has been assigned)
  Owner may be nil, but you will be responsible for destroying it instead of being the responsibility of the owner object)

properties
  Interval: integer - The number of milliseconds (1000=1 second) between executions
  Enabled: boolean
  OnTimer: function(timer) - The function to call when the timer triggers

methods
  getInterval()
  setInterval(interval) : Sets the speed on how often the timer should trigger. In milliseconds (1000=1 second)
  getOnTimer()
  setOnTimer(function(timer))
  getEnabled()
  setEnabled(boolean)

CustomControl class (CustomControl->WinControl->Control->Component->Object)
properties
  Canvas : The canvas object for drawing on the control/. Readonly
  OnPaint: an OnPaint event you can assign to do some extra painting
methods
  getCanvas() : Returns the Canvas object for the given object that has inherited from customControl


Canvas Class : (Inheritance: CustomCanvas->Object)
properties
  Brush: Brush - The brush object
  Pen: Pen - The pen object
  Font: Font - The font object
  Width: integer - Width of the canvas
  Height: integer - Height of the canvas
  Handle: integer - DC handle of the canvas



methods
  getBrush(): Returns the brush object of this canvas
  getPen(): Returns the pen object of this canvas
  getFont(): Returns the font object of this canvas
  getWidth()
  getHeight()
  getPenPosition()
  setPenPosition(x,y)
  clear() - Clears the canvas

  line(sourcex, sourcey, destinationx, destinationy)
  lineTo(destinationx, destinationy)
  moveTo(destinationx, destinationy)
  rect(x1,y1,x2,y2) - Draws a rectangle
  fillRect(x1,y1,x2,y2) - Draws a filled rectangle
  roundRect(x1,y1,x2,y2,rx,ry) - Draws a rectangle with rounded corners
  drawFocusRect(x1,y1,x2,y2) - Draws the focus rectangle shape
  textOut(x,y, text)
  textRect(rect,x,y,text): write the text within the given rectangle. The text supports some ansi escape characters
  getTextWidth(text)
  getTextHeight(text)
  getPixel(x,y)
  setPixel(x,y,color)
  floodFill(x,y, color OPTIONAL default=brush.Color, filltype OPTIONAL default=fsSurface): Fills the picture till/with a color.  
    filltype can be 
      fsSurface: fill till the color (it fills all except this color)        
      fsBorder:  fill this color (it fills only connected pixels of this color)      


  ellipse(x1,y1,x2,y2)
  gradientFill(x1,y1,x2,y2, startcolor, stopcolor, direction) : Gradient fills a rectangle. Direction can be 0 or 1. 0=Vertical 1=Horizontal
  copyRect(dest_x1,dest_y1,dest_x2,dest_y2, sourceCanvas, source_x1,source_y1,source_x2,source_y2) : Draws an image from one source to another. Useful in cases of doublebuffering
  draw(x,y, graphic) : Draw the image of a specific Graphic class
  stretchDraw(rect, graphic): Draw the image of a specific Graphic class and stretch it so it fits in the given rectangle
  getClipRect() : Returns a table containing the fields Left, Top, Right and Bottom, which define the invalidated region of the graphical object. Use this to only render what needs to be rendered in the onPaint event of objects

Pen Class : (Inheritance: CustomPen->CanvasHelper->Object)
properties
  Color: Integer - The color of the pen
  Width: integer - Thickness of the pen
methods
  getColor()
  setColor(color)
  getWidth()
  setWidth(width)


Brush Class : (Inheritance: CustomBrush->CanvasHelper->Object)
properties
  Color : Integer
methods
  getColor()
  setColor()

Font Class : (Inheritance: CustomFont->CanvasHelper->Object)
createFont(): Returns a font object (default initialized based on the main ce window)

properties
  Name: string
  Size: integer
  Height: integer
  Orientation: integer
  Pitch: string - 'fpDefault', 'fpVariable', 'fpFixed'
  Color: integer
  CharSet: integer
  Quality: string - 'fqDefault', 'fqDraft', 'fqProof', 'fqNonAntialiased', 'fqAntialiased', 'fqCleartype', 'fqCleartypeNatural' 
