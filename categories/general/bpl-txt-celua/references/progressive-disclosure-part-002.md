  Style: string set - ['fsBold', 'fsItalic', 'fsStrikeOut', 'fsUnderline']

methods
  getName(): Gets the fontname of the font
  setName(string): Sets the fontname of the font
  getSize(): Gets the size of the font
  setSize(integer): Sets the size of the font
  getColor(): Gets the color of the font
  setColor(integer): Sets the color of the font
  assign(font): Copies the contents of the font given as parameter to this font


Graphic Class : (Inheritance: Object) : Abstract class
properties
  Width: integer
  Height: integer
  Transparent: boolean

methods
  getWidth(graphic): Gets the current width in pixels of this graphics object
  setWidth(graphic, width): Sets thw width in pixels
  getHeight(graphic)
  setHeight(graphic, height)
  loadFromFile(filename)
  saveToFile(filename)

RasterImage class: (Inheritance: Graphic->Object) : Base class for some graphical controls
properties
  Canvas: Canvas
  PixelFormat: PixelFormat - the pixelformat for this image. Will clear the current image if it had one. Supported pixelformats: pf1bit, pf4bit, pf8bit, pf15bit, pf16bit, pf24bit, pf32bit (recommended)
  TransparentColor: integer

methods
  getCanvas(): Returns the Canvas object for this image
  getPixelFormat():  Returns the current pixelformat
  getPixelFormat(pixelformat):  Sets the pixelformat for this image. Will clear the current image if it had one. Supported pixelformats: pf1bit, pf4bit, pf8bit, pf15bit, pf16bit, pf24bit, pf32bit (recommended)
  setTransparentColor(integer): Sets the color that will be rendered as transparent when drawn
  getTransparentColor():  Returns the color set to be transparent
  saveToStream(stream) : Saves the image to a stream object
  loadFromStream(stream): Loads the image from a stream object



Bitmap class: (Inheritance: CustomBitmap->RasterImage->Graphic->Object) : Bitmap based Graphic object
createBitmap(width, height) - Returns a Bitmap object

PortableNetworkGraphic Class: (Inheritence: CustomBitmap->RasterImage->Graphic->Object)
createPNG(width, height) - Returns a PortableNetworkGraphic object

JpegImage Class: (Inheritence: CustomBitmap->RasterImage->Graphic->Object)
createJpeg(width, height) - Returns a Jpeg object

Icon Class: (Inheritence: CustomBitmap->RasterImage->Graphic->Object)
createIcon(width, height) - Returns an Icon object


Picture Class : (Inheritance: Object) : Container for the Graphic class
createPicture() : Returns a empty picture object

properties
  Graphic
  PNG
  Bitmap
  Jpeg
  Icon

methods
  loadFromFile(filename)
  saveToFile(filename)
  loadFromStream(stream, originalextension OPTIONAL) : Loads a picture from a stream. Note that the stream position must be set to the start of the picture
  assign(sourcepicture)


GenericHotkey Class : (Inheritance:  Object)
createHotkey(function, keys, ...) : returns an initialized GenericHotkey class object. Maximum of 5 keys
createHotkey(function, {keys, ...}) : ^

properties
  DelayBetweenActivate: integer - Interval in milliseconds that determines the minimum time between hotkey activations. If 0, the global delay is used
  onHotkey: The function to call when the hotkey is pressed

methods
  getKeys()
  setKeys(key, ....)
  setOnHotkey(table)
  getOnHotkey


CommonDialog class: (Inheritance: CommonDialog->Component->Object)
  properties
    OnShow: function(sender)
    OnClose: function(sender)
    Title: string - The caption at top of the dialog
  methods
    Execute() : Shows the dialog and return true/false depending on the dialog

ColorDialog class: 
createColorDialog(owner OPTIONAL) - Creates a new colordialog
properties
  property Color: integer - The currently selected color
  property CustomColors: TStrings - List of custom colors ( entry looks like ColorA = FFFF00 ... ColorX = C0C0C0 ) 

methods

ColorBox class:
  Combobox like component where you can pick a color

createColorBox(owner) - Creates a new colorbox



FindDialog Class: (Inheritance: CommonDialog->Component->Object)
createFindDialog(owner)

properties
  Top
  Left
  Width
  Height
  FindText: String - The text the user wishes to find
  Options: Enum - Find Options
                   { frDown, frFindNext, frHideMatchCase, frHideWholeWord,
                     frHideUpDown, frMatchCase, frDisableMatchCase, frDisableUpDown,
                     frDisableWholeWord, frReplace, frReplaceAll, frWholeWord, frShowHelp,
                     frEntireScope, frHideEntireScope, frPromptOnReplace, frHidePromptOnReplace }
  OnFind: function (sender) - Called when the find button has been clicked
  OnHelp: function (sender) - Called when the help button is visible (see Options) and clicked
methods


FileDialog Class: (Inheritance: CommonDialog->Component->Object)

properties

  DefaultExt: string - When not using filters this will be the default extention used if no extension is given
  Files: Strings - Stringlist containing all selected files if multiple files are selected
  FileName: string - The filename that was selected
  Filter: string - A filter formatted string
  FilterIndex: integer - The index of which filter to use

  InitialDir: string - Sets the folder the filedialog will show first
methods



OpenDialog Class: (Inheritance: FileDialog->CommonDialog->Component->Object)
createOpenDialog(owner) : Creates an opendialog object

properties
  Options: String
    A string formatted as "[param1, param2, param3]" to set OpenDialogs options
    Valid parameters are:
      ofReadOnly,
      ofOverwritePrompt  : if selected file exists shows a message, that file will be overwritten
      ofHideReadOnly     : hide read only file
      ofNoChangeDir      : do not change current directory
      ofShowHelp         : show a help button
      ofNoValidate
      ofAllowMultiSelect : allow multiselection
      ofExtensionDifferent
      ofPathMustExist    : shows an error message if selected path does not exist
      ofFileMustExist    : shows an error message if selected file does not exist
      ofCreatePrompt
      ofShareAware
      ofNoReadOnlyReturn : do not return filenames that are readonly
      ofNoTestFileCreate
      ofNoNetworkButton
      ofNoLongNames
      ofOldStyleDialog
      ofNoDereferenceLinks : do not expand filenames
      ofEnableIncludeNotify
      ofEnableSizing     : dialog can be resized, e.g. via the mouse
      ofDontAddToRecent  : do not add the path to the history list
      ofForceShowHidden  : show hidden files
      ofViewDetail       : details are OS and interface dependent
      ofAutoPreview      : details are OS and interface dependent


methods
-


SaveDialog Class: (Inheritance: OpenDialog->FileDialog->CommonDialog->Component->Object)
createSaveDialog(owner)

SelectDirectoryDialog Class: (Inheritance: OpenDialog->FileDialog->CommonDialog->Component->Object)
createSelectDirectoryDialog(owner)


Stream Class

properties
  Size: integer
  Position: integer

methods
  copyFrom(stream, count) - Copies count bytes from the given stream to this stream
  read(count): bytetable - Returns a bytetable containing the bytes of the stream. This increases the position
  write(bytetable, count OPTIONAL)- Writes the given bytetable to the stream
  readByte(): integer
  writeByte(integer)
  readWord(): integer
  writeWord(integer)
  readDword(): integer
  writeDword(integer)
  readQword(): integer
  writeQword(integer)
  readAnsiString(): string
  writeAnsiString(string)


MemoryStream Class (Inheritance: Stream->Object)
createMemoryStream()

properties
  Memory: Integer - The address in Cheat Engine's memory this stream is loaded (READONLY, tends to change on size change)

methods
  loadFromFile(filename) : Replaces the contents in the memory stream with the contents of a file on disk
  saveToFile(filename) : Writes the contents of the memory stream to the specified file
  loadFromFileNoError(filename):boolean,string - Replaces the contents in the memory stream with the contents of a file on disk. On success returns true, else false with a secondary return the error message
  saveToFileNoError(filename):boolean,string - Writes the contents of the memory stream to the specified file. On success returns true, else false with a secondary return the error message



FileStream Class (Inheritance: HandleStream->Stream->Object)
createFileStream(filename, mode)  - 
  Creates a filestream object.  mode can be fmCreate(0xff00), fmOpenRead, fmOpenWrite or fmOpenReadWrite and can be or-ed with
  fmShareCompat(0x0000), fmShareExclusive(0x0010), fmShareDenyWrite(0x0020), fmShareDenyRead(0x0030) or fmShareDenyNone(0x0040)


StringStream Class (Inheritance: Stream->Object)
createStringStream(string)

properties
DataString: The internal string


TableFile class (Inheritance: Object)
findTableFile(filename): Returns the TableFile class object for the saved file
createTableFile(filename, filepath OPTIONAL): TableFile - Add a new file to your table. If no filepath is specified, it will create a blank file. Otherwise, it will read the contents from disk.

properties
  Name: string
  Stream: MemoryStream

methods
  delete() : Deletes this file from your table.
  saveToFile(filename)
  getData() : Gets a MemoryStream object


xmplayer class
The xmplayer class has already been defined as xmplayer, no need to create it manually

properties
  IsPlaying : boolean - Indicator that the xmplayer is currently playing a xm file
  Initialized: boolean - Indicator that the xmplayer is actually actively loaded in memory

methods
  setVolume(int)
  playXM(filename, OPTIONAL noloop)
  playXM(tablefile, OPTIONAL noloop)
  playXM(Stream, OPTIONAL noloop)
  pause()
  resume()
  stop()


CheatComponent Class: (Inheritance: WinControl->Control->Component->Object)
The cheatcomponent class is the component used in Cheat Engine 5.x trainers
Most people will probably want to design their own components but for those that don't know much coding and use the autogenerated trainer this will be used

properties
  Color: Integer - background color
  Textcolor: integer - text color
  Activationcolor: integer - The textcolor to show when activated is true
  Activated: boolean - Toggles between the ActivationColor and the TextColor
  Editleft:integer - The x position of the optional edit field
  Editwidth: integer - the width of the optional edit field
  Editvalue:string - The string of the optional edit field
  Hotkey:string read - The hotkeypart of the cheat line
  Description:string - Description part of the cheat line
  Hotkeyleft: integer - The x position of the hotkey line
  Descriptionleft:integer - The x position of the Description line


  ShowHotkey: boolean - Decides if the hotkey label should be shown
  HasEditBox: boolean - Decides if the editbox should be shown
  HasCheckbox: boolean - Decides if the checkbox should be shown
  Font: Font - The font to use to render the text

methods
 -



MemoryRecordHotkey Class: (Inheritance: object)
The memoryrecord hotkey class is mainly readonly with the exception of the event properties to be used to automatically create trainers
Use the generic hotkey class if you wish to create your own hotkeys

properties
  Owner: MemoryRecord - The memoryrecord this hotkey belongs to (ReadOnly)
  Keys: Table - Table containing the keys(combination) for this hotkey
  action: integer - The action that should happen when this hotkey triggers
      mrhToggleActivation(0): Toggles between active/deactive
      mrhToggleActivationAllowIncrease(1): Toggles between active/deactive. Allows increase when active
      mrhToggleActivationAllowDecrease(2): Toggles between active/deactive. Allows decrease when active
      mrhActivate(3): Sets the state to active
      mrhDeactivate(4):  Sets the state to deactive
      mrhSetValue(5):  Sets a specific value to the value properyy (see value)
      mrhIncreaseValue(6):  Increases the current value with the value property (see value)
      mrhDecreaseValue(7):  Decreases the current value with the value property (see value)
  value: string - Value used depending on what kind of hotkey is used
  ID: integer - Unique id of this hotkey (ReadOnly)
  Description: string - The description of this hotkey  
  HotkeyString: string - The hotkey formatted as a string (ReadOnly)
  ActivateSound: string - Tablefile name of a WAV file inside the table which will get played on activate events
  DeactivateSound: string - Tablefile name of a .WAV file inside the table which will get played on deactivate events
  OnHotkey: function(sender) - Function to be called when a hotkey has just been pressed
  OnPostHotkey: function(sender) - Function to be called when a hotkey has been pressed and the action has been performed


methods
  doHotkey: Executes the hotkey as if it got triggered by the keyboard


MemoryRecord Class:
The memoryrecord objects are the entries you see in the addresslist

properties
  ID: Integer - Unique ID
  Index: Integer - The index ID for this record. 0 is top. (ReadOnly)
  Description: string- The description of the memory record
  Address: string - Get/set the interpretable address string. Useful for simple address settings.
  AddressString: string - Get the address string shown in CE (ReadOnly)
  OffsetCount: integer - The number of offsets. Set to 0 for a normal address
  Offset[] : integer - Array to access each offset
  OffsetText[] : string - Array to access each offset using the interpretable text style

  CurrentAddress: integer - The address the memoryrecord points to
  VarType: ValueType (string) - The variable type of this record. See vtByte to vtCustom
  Type: ValueType (number) - The variable type of this record. See vtByte to vtCustom
    If the type is vtString then the following properties are available:
     String.Size: Number of characters in the string
     String.Unicode: boolean
     String.Codepage: boolean

    If the type is vtBinary then the following properties are available
      Binary.Startbit: First bit to start reading from
      Binary.Size : Number of bits

    If the type is vtByteArray then the following properties are available
      Aob.Size : Number of bytes

  CustomTypeName: String - If the type is vtCustom this will contain the name of the CustomType
  Script: String - If the type is vtAutoAssembler this will contain the auto assembler script
  Value: string - The value in stringform.
  NumericalValue: number - The value in numerical form.  nil if it can not be parsed to a number
  Selected: boolean - Set to true if selected (ReadOnly)
  Active: boolean - Set to true to activate/freeze, false to deactivate/unfreeze
  Color: integer
  ShowAsHex: boolean - Self explanatory
  ShowAsSigned: boolean - Self explanatory
  AllowIncrease: boolean - Allow value increasing, unfreeze will reset it to false
  AllowDecrease: boolean - Allow value decreasing, unfreeze will reset it to false
  Collapsed: boolean - Set to true to collapse this record or false to expand it. Use expand/collapse methods for recursive operations. 
  IsGroupHeader: boolean - Set to true if the record was created as a Group Header with no address or value info. 
  IsAddressGroupHeader: boolean - Set to true if the record was created as a Group Header with address.
  IsReadable: boolean - Set to false if record contains an unreadable address. NOTE: This property will not be set until the value property is accessed at least once. (ReadOnly)

  Options: String set - a string enclosed by square brackets filled with the options seperated by a comma. Valid options are: moHideChildren, moActivateChildrenAsWell, moDeactivateChildrenAsWell, moRecursiveSetValue, moAllowManualCollapseAndExpand, moManualExpandCollapse, moAlwaysHideChildren
  
  DropDownLinked: boolean - if dropdown list refers to list of another memory record eg. (memrec name)
  DropDownLinkedMemrec: string - Description of linked memrec or emptystring if not linked
  DropDownList : StringList - list of "value:description" lines, lists are still separate objects when linked, read-write
  DropDownReadOnly: boolean - true if 'Disallow manual user input' is set
  DropDownDescriptionOnly: boolean - self explanatory
  DisplayAsDropDownListItem: boolean - self explanatory
  DropDownCount: integer - equivalent to .DropDownList.Count
  DropDownValue[index] : Array to access values in DropDownList (ReadOnly)
  DropDownDescription[index] : Array to access Descriptions in DropDownList (ReadOnly)



  Count: Number of children
  Child[index] : Array to access the child records
  [index] = Child[index]
  Parent: MemoryRecord - The parent of the memory record

  HotkeyCount: integer - Number of hotkeys attached to this memory record
  Hotkey[] : Array to index the hotkeys

  Async: Boolean - Set to true if activating this entry will be asynchronious. (only for AA/Lua scripts)
  AsyncProcessing: Boolean - True when async is true and it's being processed
  AsyncProcessingTime: qword - The time that it has been processing in milliseconds

  HasMouseOver: boolean - True if the mouse is currently over it

  OnActivate: function(memoryrecord,before,currentstate):boolean - The function to call when the memoryrecord will change (or changed) Active to true. If before is true, not returning true will cause the activation to stop.
  OnDeactivate: function(memoryrecord,before,currentstate):boolean - The function to call when the memoryrecord will change (or changed) Active to false. If before is true, not returning true will cause the deactivation to stop.
  OnDestroy: function() - Called when the memoryrecord is destroyed.
  OnGetDisplayValue: function(memoryrecord,valuestring):boolean,string - This function gets called when rendering the value of a memory record. Return true and a new string to override the value shown
  OnValueChanged: function(memoryrecord, oldvalue, newvalue): This function gets called whenever the value of a memory record has changed
  OnValueChangedByUser: function(memoryrecord, oldvalue, newvalue):This function gets called whenever the value of a memory record has changed by the user
  DontSave: boolean - Don't save this memoryrecord and it's children

methods
  getDescription()
  setDescription()
  getAddress() : Returns the interpretable addressstring of this record. If it is a pointer, it returns a second result as a table filled with the offsets
  setAddress(string) : Sets the interpretable address string, and if offsets are provided make it a pointer

  getOffsetCount(): Returns the number of offsets for this memoryrecord
  setOffsetCount(integer): Lets you set the number of offsets

  getOffset(index) : Gets the offset at the given index
  setOffset(index, value) : Sets the offset at the given index

  getCurrentAddress(): Returns the current address as an integer (the final result of the interpretable address and pointer offsets)

  appendToEntry(memrec): Appends the current memory record to the given memory record

  getHotkey(index): Returns the hotkey from the hotkey array
  getHotkeyByID(integer): Returns the hotkey with the given id

  reinterpret()
  createHotkey({keys}, action, value OPTIONAL, description OPTIONAL): Returns a hotkey object 

  disableWithoutExecute(): Sets the entry to disabled without executing the disable section
  beginEdit() : Call when you wish to take a long time to edit a record. (e.g external editor) It prevents the record from getting deleted
  endEdit() : to mark the end of your long edit sequence

global events
  function onMemRecPreExecute(memoryrecord, newstate BOOLEAN):
    If above function is defined it will be called before action* has been performed.
    Active property is about to change to newState.
  
  function onMemRecPostExecute(memoryrecord, newState BOOLEAN, succeeded BOOLEAN):
    If above function is defined it will be called after action*.
    Active property was supposed to change to newState.
    If 'succeeded' is true it means that Active state has changed and is newState.
    
    newState and succeeded are read only.
  
    *action can be: running auto assembler script (ENABLE or DISABLE section), freezing and unfreezing.
  


Addresslist Class: (Inheritance: Panel->WinControl->Control->Component->Object)
properties
  LoadedTableVersion: integer - Returns the tableVersion of the last loaded table
  Count: Integer - The number of records in the table
  SelCount: integer- The number of records that are selected
  SelectedRecord: MemoryRecord - The main selected record
  MemoryRecord[]: MemoryRecord - Array to access the individial memory records
  [] = MemoryRecord - Default accessor

  CheckboxActiveSelectedColor: color
  CheckboxActiveColor: color
  CheckboxSelectedColor: color
  CheckboxColor: color
  SelectedBackgroundColor: color
  SelectedSecondaryBackgroundColor: color
  ExpandSignColor: color
  IncreaseArrowColor: color
  DecreaseArrowColor: color

  MouseHighlightedRecord() : Returns the memoryrecord that the mouse points at. nil if nothing


  OnDescriptionChange: function(addresslist,memrec):boolean - called when the user initiates a description column change on a record. Return true if you handle it, false for normal behaviour
  OnAddressChange: function(addresslist,memrec):boolean - called when the user initiates an address column change on a record. Return true if you handle it, false for normal behaviour
  OnTypeChange: function(addresslist,memrec):boolean - called when the user initiates a type column change on a record. Return true if you handle it, false for normal behaviour
  OnValueChange: function(addresslist,memrec):boolean - called when the user initiates a value column change on a record. Return true if you handle it, false for normal behaviour
  OnAutoAssemblerEdit: function(addresslist,memrec) - Called when the user initiates a memoryrecord AA script edit.  This function will be responsible for changing the memory record


methods
  getCount()
  getMemoryRecord(index)
  getMemoryRecordByDescription(description): returns a MemoryRecord object
  getMemoryRecordByID(ID)
  createMemoryRecord() : creates an generic cheat table entry and add it to the list

  getSelectedRecords():  Returns a table containing all the selected records

  doDescriptionChange() : Will show the GUI window to change the description of the selected entry
  doAddressChange() : Will show the GUI window to change the address of the selected entry
  doTypeChange() : Will show the GUI window to change the type of the selected entries
  doValueChange() : Will show the GUI window to change the value of the selected entries

  getSelectedRecord() : Gets the main selected memoryrecord
  setSelectedRecord(memrec) : Sets the currently selected memoryrecord. This will unselect all other entries

  disableAllWithoutExecute(): Disables all memory records without executing their [Disable] section
  rebuildDescriptionCache(): Rebuilds the description to record lookup table


MemScan Class (Inheritance: Object)
getCurrentMemscan() : Returns the current memory scan object. If tabs are used the current tab's memscan object
createMemScan(progressbar OPTIONAL) : Returns a new MemScan class object

properties
  LastScanWasRegionScan: boolean - returns true is the previous scan was an unknown initial value
  LastScanValue: string
  LastScanType: ScanType/string - 'stNewScan', 'st v   ', 'stNextScan'
  ScanresultFolder: string - Path where the results are stored  
  OnScanDone: function(memscan) - Set a function to be called when the scan has finished
  OnGuiUpdate: function(memscan, TotalAddressesToScan, CurrentlyScanned, ResultsFound) - Called during the scan so you can update the interface if needed
  FoundList: FoundList - The foundlist currently attached to this memscan object
  OnlyOneResult: boolean - If this is set to true memscan will stop scanning after having found the first result, and written the address to "Result"
  IsUnique: boolean - Same as OnlyOneResult but will use multiple threads, so if the value is not unique you will be given a random address
  Result: Integer - If OnlyOneResult is used this will contain the address after a scan has finished

  CodePage: boolean;
  ScanOption: TScanoption 
  VariableType: TVariableType
  VarType: TVariableType : ^
  Roundingtype: TRoundingType
  Scanvalue: string : Value to scan
  Scanvalue1: string : ^
  Scanvalue2: string : Secondary value to scan (e.g value between scan)
  Startaddress: integer
  Stopaddress: integer
  Hexadecimal: boolean 
  BinaryStringAsDecimal: boolean
  UTF16: boolean 
  Casesensitive: boolean 
  Fastscanmethod: TFastScanMethod 
  Fastscanparameter: string
  Customtype: TCustomType

  ScanWritable:    TScanregionpreference ('scanDontCare', 'scanExclude', 'scanInclude')
  ScanExecutable:  TScanregionpreference ('scanDontCare', 'scanExclude', 'scanInclude') 
  ScanCopyOnWrite: TScanregionpreference ('scanDontCare', 'scanExclude', 'scanInclude')
  
  Percentage: boolean
  CompareToSavedScan: boolean 
  SavedScanName: string

methods
  scan(): Does either a first scan or next scan based on the given property values
  firstScan() : Does a first scan based on the given property values
  nextScan() : Does a next scan based on the given property values
  newScan() : Clears the current results

  firstScan(scanoption, vartype, roundingtype, input1, input2 ,startAddress ,stopAddress ,protectionflags ,alignmenttype ,"alignmentparam" ,isHexadecimalInput ,isNotABinaryString, isunicodescan, iscasesensitive);
    Does an initial scan.
    memscan: The MemScan object created with createMemScan
    scanOption: Defines what type of scan is done. Valid values for firstscan are:
      soUnknownValue: Unknown initial value scan
      soExactValue: Exact Value scan
      soValueBetween: Value between scan
      soBiggerThan: Bigger than ... scan
      soSmallerThan: smaller than ... scan

    vartype: Defines the variable type. Valid variable types are:
      vtByte
      vtWord  2 bytes
      vtDword 4 bytes
      vtQword 8 bytes
      vtSingle float
      vtDouble
      vtString
      vtByteArray
      vtGrouped
      vtBinary
      vtAll

    roundingtype: Defined the way scans for exact value floating points are handled
      rtRounded : Normal rounded scans. If exact value = "3" then it includes 3.0 to 3.49999999. If exact value is "3.0" it includes 3.00 to 3.0499999999
      rtTruncated: Truncated algorithm. If exact value = "3" then it includes 3.0 to 3.99999999. If exact value is "3.0" it includes 3.00 to 3.099999999
      rtExtremerounded: Rounded Extreme. If exact value = "3" then it includes 2.0000001 to 3.99999999. If exact value is "3.0" it includes 2.900000001 to 3.099999999

    input1: If required by the scanoption this is a string of the given variable type
    input2: If requires by the scanoption this is the secondary input

    startAddress : The start address to scan from. You want to set this to 0
    stopAddress  : The address the scan should stop at. (You want to set this to 0xffffffffffffffff)

    protectionflags : See aobscan about protectionflags
    alignmenttype : Scan alignment type. Valid options are:
      fsmNotAligned : No alignment check
      fsmAligned    : The address must be dividable by the value in alignmentparam
      fsmLastDigits : The last digits of the address must end with the digits provided by alignmentparam

    alignmentparam : String that holds the alignment parameter.

    isHexadecimalInput: When true this will handle the input field as a hexadecimal string else decimal
    isNotABinaryString: When true and the varType is vtBinary this will handle the input field as a decimal instead of a binary string
    isunicodescan: When true and the vartype is vtString this will do a unicode (utf16) string scan else normal utf8 string
    iscasesensitive : When true and the vartype is vtString this check if the case matches




  nextScan(scanoption, roundingtype, input1,input2, isHexadecimalInput, isNotABinaryString, isunicodescan, iscasesensitive, ispercentagescan, savedresultname OPTIONAL);
    Does a next scan based on the current addresslist and values of the previous scan or values of a saved scan
    memscan: The MemScan object that has previously done a first scan
    scanoption:
      soExactValue: Exact Value scan
      soValueBetween: Value between scan
      soBiggerThan: Bigger than ... scan
      soSmallerThan: smaller than ... scan
      soIncreasedValue: Increased value scan
      soIncreasedValueBy: Increased value by scan
      soDecreasedValue: Decreased value scan
      soDecreasedValueBy: Decreased value by scan
      soChanged: Changed value scan
      soUnchanged: Unchanged value scan

    roundingtype: Defined the way scans for exact value floating points are handled
      rtRounded : Normal rounded scans. If exact value = "3" then it includes 3.0 to 3.49999999. If exact value is "3.0" it includes 3.00 to 3.0499999999
      rtTruncated: Truncated algoritm. If exact value = "3" then it includes 3.0 to 3.99999999. If exact value is "3.0" it includes 3.00 to 3.099999999
      rtExtremerounded: Rounded Extreme. If exact value = "3" then it includes 2.0000001 to 3.99999999. If exact value is "3.0" it includes 2.900000001 to 3.099999999

    input1: If required by the scanoption this is a string of the given variable type
    input2: If requires by the scanoption this is the secondary input

    isHexadecimalInput: When true this will handle the input field as a hexadecimal string else decimal
    isNotABinaryString: When true and the varType is vtBinary this will handle the input field as a decimal instead of a binary string
    isunicodescan: When true and the vartype is vtString this will do a unicode (utf16) string scan else normal utf8 string
    iscasesensitive : When true and the vartype is vtString this check if the case matches
    ispercentage: When true and the scanoption is of type soValueBetween, soIncreasedValueBy or soDecreasedValueBy will cause CE to do a precentage scan instead of a normal value scan
    savedResultName: String that holds the name of a saved result list that should be compared against. First scan is called "FIRST"


  waitTillDone() : Waits for the memscan thread(s) to finish scanning. Always use this
  saveCurrentResults(name) : Save the current scanresults to a unique name for this memscan. This save can be used to compare against in a subsequent next scan
  getSavedResultList(): Returns an indexed table of all the saved results (strings)
  getSavedResultHandler(name): Gets the 'SavedResultHandler' object with this name (nil on failure)
  getAttachedFoundlist() : Returns a FoundList object if one is attached to this scanresults. Returns nil otherwise


  setOnlyOneResult(state): If set to true before you start a scan, this will cause the scanner to only return one result. Note that it does not work with a foundlist
  getOnlyResult(): Only works if returnOnlyOneResult is true. Returns nil if not found, else returns the address that was found (integer)
  getProgress(): returns a table with fields: TotalAddressesToScan, CurrentlyScanned, ResultsFound


FoundList Class
The foundlist is an object that opens the current memscan's result file and provides an interface for reading out the addresses

createFoundList(memscan)

properties
  Count: integer - Number of results found
  Address[index] : string - Returns the address as a string at the given index
  Value[index]: string - Returns the value as a string at the given index
  [index]: string - Same as Address

methods
  initialize() : Call this when a memscan has finished scanning. This will open the results for reading
  deinitialize() : Release the results
  getCount()
  getAddress(index) : Returns the address as a string
  getValue(index) : Returns the value as a string


SavedResultHandler:
  properties
  methods
    getStringFromAddress(address, hexadecimal:boolean OPTIONAL, signed: boolean OPTIONAL) : Returns the value in string format at the given address


Memoryview class: (Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)
createMemoryView() - Creates a new memoryview window. This window will not receive debug events. Use getMemoryViewForm() function to get the main memoryview window
properties
  DisassemblerView: The disassemblerview class of this memoryview object
  HexadecimalView: The hexadecimalview class of this memoryview object
methods
  -

DisassemblerviewLine class: (Inheritance: Object)
properties
  Address: The current address of this line
  Owner: The Disassemblerview that owns this line
  OnDisassemblerViewOverride: Called when a line is about to be rendered
    funtion(address, addressstring, bytestring, opcodestring, parameterstring, specialstring)
      return addressstring, bytestring, opcodestring, parameterstring, specialstring
    end    

methods
  -

Disassemblerview class: (Inheritance: Panel->CustomControl->WinControl->Control->Component->Object)
  The visual disassembler used on the memory view window
properties
  SelectedAddress: integer - The currently selected address in the disassemblerview
  SelectedAddress2: integer - The secondary selected address in the disassemblerview
  TopAddress: Integer - The first address to show
  ShowJumplines: boolean - Determines if the jumplines should be shown
  HideFocusRect: boolean - If set to true the focus rectangle won't be shown
  SpaceAboveLines: integer
  SpaceBelowLines: integer
  OnSelectionChange: function(sender, address, address2) - Function to call when the selection has changed
  OnExtraLineRender: function(sender, Address, AboveInstruction, Selected): RasterImage OPTIONAL, x OPTIONAL, y OPTIONAL
    Function to call when you wish to provide the disassembler view with an extra image containing data you wish to show.
    This function is called once to get an image to show above the instruction, and once to get an image to show under the instruction and optional comments.
    The image for both calls must be different objects as rendering will only be done when both calls have been completed

    Sender is a DisassemblerviewLine object
    If no coordinates are given the image will be centered above/below the instruction

  Osb: Bitmap : Background picture of the disasemblerview


methods
  -


Hexadecimal class: (Inheritance: Panel->CustomControl->WinControl->Control->Component->Object)
  The visual hexadecimal object used on the memory view window
properties
  Address: integer - The top address
  HasSelection: boolean - True if something is selected
  SelectionStart: integer
  SelectionStop: integer
  DisplayType: displaytype - The type being shown: dtByte, dtByteDec, dtWord, dtWordDec, dtDword, dtDwordDec, dtQword, dtQwordDec, dtSingle, dtDouble
  OnAddressChange(hexadecimalview, function): function(hexadecimalview, address)
  OnByteSelect(hexadecimalview, function): function(hexadecimalview, address, address2)
  OnCharacterRender: function(sender, address, text) return text end - Called when a character is being rendered. Use this to change it or change the canvas fonts (Warning: slow)
  OnValueRender: function(sender, address, text) return text end - Called when a value (depending on the displaytype) is being rendered. Use this to change it or change the canvas fonts (Warning: slow)

methods
  -


Thread Class: (Inheritance: Object)
createThread(function(Thread,...), ...) :
  Executes the given function in another thread using the systems thread mechanism
  The function returns the Thread class object
  function declaration: function (Thread, ...)

createThreadSuspended(function(Thread,...), ...) :
  Same as createNativeThread but it won't run until resume is called on it

createThreadNewState(scripttext): Creates a new thread in a new lua state. This is more efficient as no locking inside lua takes place, but has no access to userdefined lua functions and only limited base CE functions. called inside a function(t) where t is the thread.  Watch for t.Terminated to quit.  Notice: Unlike createThread, the created thread does not freeOnTerminate so you can read out the "Result" property which will be set on thread finish


properties
  Name: string - This name will be shown when the thread terminated abnormally
  Finished: boolean - Returns true if the thread has reached the end.  Do not rely on this if the thread is freeOnTerminate(true) (which is the default)
  Terminated: boolean - Returns true if the Terminate method has been called
  Result: string - The result of the thread function as a string

methods
  freeOnTerminate(state) :
    When set to true the thread object will free itself when the function ends (default=true)
    Note: Use this only from inside the thread function as the thread might have already terminated and freed itself when called

  synchronize(function(thread, ...), ...) :
    Called from inside the thread. This wil cause the tread to get the main thread to execute the given function and wait for it to finish.
    Usually for GUI access
    Returns the return value of the given function

  waitfor() :
    Waits for the given thread to finish (Not recommended to call this from inside the thread itself)

  suspend() :
    Suspend the thread's execution

  resume() :
    Resume the thread's execution

  terminate() :
    Tells the thread it should terminate. The Terminated property will become true


CriticalSection class: (Inheritance: Object)
createCriticalSection(): Returns a critical section object

properties
-

methods
  enter()
  leave()
  tryEnter(): Returns true if entered, false if not


Event class: (Inheritance: Object)
createEvent(ManualReset, InitialState): Returns an event object

properties
-

methods
  resetEvent()
  setEvent()
  waitFor(timeout): Waits for the event to be set. Returns wrSignaled(0), wrTimeout(1), wrAbandoned(2) or wrError(3);  


Semaphore class: (Inheritance: Object)
createSemaphore(count): Returns an semaphore object
properties
-

methods
  acquire()
  release()


MultiReadExclusiveWriteSynchronizer class: (Inheritance: Object)
createMultiReadExclusiveWriteSynchronizer(): Returns a createMultiReadExclusiveWriteSynchronizer

properties
-

methods
  beginWrite()
  endWrite()
  beginRead()
  endRead()




StructureFrm class:
createStructureForm(address, groupname OPTIONAL, structurename OPTIONAL)
enumStructureForms() : returns a table of StructureFrm objects (can be useful for finding a structure window with the wanted structure)


properties:
MainStruct: structure - The currently selected structure

ColumnCount: integer - the number of columns (columns=address)
Column[index]: structColumn - Fetches a structColumn object from the structure form

GroupCount: integer - The number of groups
Group[index]: structGroup - Fetches a structGroup object from the structure form
OnStatusbarUpdate(function(notificationbar)) - Called when the statusbar gets updated



methods:
structChange() : Forces a refresh
addColumn(): Adds a new column in the currently focuses group and returns it's structColumn object
addGroup(): Adds a new group and returns the structGroup object
getSelectedStructElement(): Returns the currently selected StructureElement , and as second result a table containing an indexed list continaing 'struct', and 'element' describing the path to the base


structColumn class:
properties:
Address: integer - The current address
AddressText: string - Gets/sets the visual address
Focused: boolean - Gets/sets the focused state 

methods:
focus(): focuses the current column


structGroup class:
properties:
name: string - gets the current name
box: Groupbox - Gets the groupbox object
columnCount: integer- Gets the number of columns in the group
columns[index]: structColumn - Returns the specific structColumn object


methods:
addColumns(): Adds a new columns to the specific group and returns it's structColumn objecy




Structure class related functions:
getStructureCount(): Returns the number of Global structures. (Global structures are the visible structures)
getStructure(index): Returns the Structure object at the given index
createStructure(name): Returns an empty structure object (Not yet added to the Global list. Call structure.addToGlobalStructureList manually)
createStructureFromName(string): If PDB files are loaded this will create a structure with that name if it can be found



structure class: (Inheritance: Object)
Properties:
  Name: String - The name of the structure
  Size: Integer - The number of bytes between the last element and the start. ReadOnly
  Count: Integer - Number of elements in the structure. ReadOnly
  Element[]: structureElement - Returns the structure element at the given index. Readonly
Methods:
  getName(): Returns the name
  setName(name): Sets the name
  getElement(index): Returns a structureElement object (Changing offsets can change the index)
  getElementByOffset(offset): Returns a structureElement object where the specified offset is at least the requested offset
  addElement(): Adds a new blank structureElement and returns it
  autoGuess(baseaddresstoguessfrom, offset, size)
  fillFromDotNetAddress(address, changeName): Fills the structure with the layout gathered from querying .NET.  If changeName is true, the structure will take the name of the .NET class.  (6.4+)

  beginUpdate(): Call this when you want to make multiple updates to a structure. It will speed up the update process
  endUpdate(): Call this when done
  addToGlobalStructureList(): Add this to the list of structures for the user to select from. (Global structures will get saved to the table)
  removeFromGlobalStructureList(): Remove from the list of structures.


StructureElement class: (Inheritance: Object)
Properties:
  Owner: structure - The structure this element belongs to. Readonly
  Offset: integer - The offset of this element
  Name: string - The name of this element
  Vartype: integer - The variable type of this element
  DisplayMethod: string - The displaymethod of the entry : 'dtUnsignedInteger', 'dtSignedInteger' or 'dtHexadecimal'
  ChildStruct: structure - If not nil this element is a pointer to the structure defined here
  ChildStructStart: integer - The number of bytes inside the provided childstruct. (E.g: It might point to offset 10 of a certain structure)
  Bytesize: integer - The number of bytes of this element. Readonly for basic types, writable for types that require a defined length like strings and array of bytes

Methods:
  getOwnerStructure(): Returns the structure this element belongs to
  getOffset(): Returns the offset of this element
  setOffset(offset): Sets the offset of this element
  getName(): Returns the name of this element
  setName(name): Sets the name of this element (tip: Leave blank if you only want to set the name of the variable)
  getVartype(): Returns the variable type of this element (check Variable types in defines.lua)
  setVartype(vartype)
  getValue(address) : Gets the memory from the specified address and interprets it according to the element type
  setValue(address,value): Sets the memory at the specified address to the interpreted value according to the element type
  getValueFromBase(baseaddress): same as getValue but uses the offset to calculate the final address
  setValueFromBase(baseaddress,value): same as setValue but uses the offset to calculate the final address
  getChildStruct()
  setChildStruct(structure)
  getChildStructStart()
  setChildStructStart(offset)
  getBytesize(): Gets the bytesize of the element. Usually returns the size of the type, except for string and aob
  setBytesize(size): sets the bytesize for types that are affected (string, aob)





supportCheatEngine(attachwindow, hasclosebutton, width, height, position ,yoururl OPTIONAL, extraparameters OPTIONAL, percentageshown OPTIONAL):
  Will show an advertising window which will help keep the development of Cheat Engine going.
  If you provide your own url it will be shown Up to 75% of the time.

  attachwindow: Type=Form : The form that the ad is attached to
  hasclosebutton: Type=boolean : If true the window will have a border an a close button at top
  width, height: Type=integer :
    The client width and height of the window.
    Prefered formats are : 120x600 , 160x600, 300x250, 468x60, 728x90  ,But you are free to use different formats

  Position: Type=integer/enum: The place of the window
    0=Top, 1=Right, 2=Bottom, 3=left

  Yoururl: Type=string: The url you want to show. When given instead of showing CE's ads 100% it will show your url up to 75%.
    You can use it for your own income, or for updating users about new versions of your trainer or whatever you feel like

  Extraparameters: Type=String :  are url request parameters you can add to the default parameters (e.g trainername=mytrainer for tracking purposes)

  PercentageShown: You can change the default of 75% to a smaller value like 50%


fuckCheatEngine() : Removes the ad window if it was showing


Following are some more internal functions for Cheat Engine

dbk_initialize() : Returns true if the dbk driver is loaded in memory. False if it failed for whatever reason (e.g 64-bit and not booted with unsigned driver support)
dbk_useKernelmodeOpenProcess() : Switches the internal pointer of the OpenProcess api to dbk_OpenProcess
dbk_useKernelmodeProcessMemoryAccess() : Switches the internal pointer to the ReadProcessMemory and WriteProcessMemory apis to dbk_ReadProcessMemory and dbk_WriteProcessMemory
dbk_useKernelmodeQueryMemoryRegions() : Switches the internal pointer to the QueryVirtualMemory api to dbk_QueryVirtualMemory
dbk_usePhysicalMemoryAccess() : Changes all memory access to physical memory
dbk_setSaferPhysicalMemoryScanning(state: BOOLEAN): When set to true CE's memory scanner will skip hardware device owned memory. Default state is true
dbk_readPhysicalMemory(address, size): bytetable
dbk_writePhysicalMemory(address, size): boolean
dbk_getPEProcess(processid) : Returns the pointer of the EProcess structure of the selected processid
dbk_getPEThread(threadid) : Gets the pointer to the EThread  structure

dbk_readMSR(msr): Reads the msr
dbk_writeMSR(msr, msrvalue): Writes the msr 
dbk_executeKernelMemory(address, parameter) :
  Executes a routine from kernelmode (e.g a routine written there with auto assembler)
  parameter can be a value or an address. It's up to your code how it's handled


dbvm_initialize(offloados:Boolean OPTIONAL, reason:String OPTIONAL) : Initializes the dbvm functions (dbk_initialize also calls this) offloados is a boolean that when set will offload the system onto dbvm if it's not yet running (and only IF the dbk driver is loaded)
dbvm_setKeys(key1,key2,key3) - Sets the keys to operate DBVM.  Key1 and Key3 are pointersize, key2 is 32-bit.  Note that if key1 or key3 are 64-bit wide, 32-bit CE can not use DBVM.  Returns true if DBVM is working, and automatically updates the current DBVM keys in CE and the driver if DBVM was already connected (e.g default keys)
dbvm_getMemory(): Returns the total memory free for DBVM, and the total number of full pages as secondary result
dbvm_addMemory(pagecount): Adds memory to DBVM (one page is 4096 bytes)
dbvm_readMSR(msr): See dbk_readMSR but then using dbvm
dbvm_writeMSR(msr, value): See dbk_writeMSR
dbvm_getCR4(): Returns the real Control Register 4 state

dbvm_readPhysicalMemory(address, size): bytetable
dbvm_writePhysicalMemory(address, bytetable)

dbvm_watch_writes(PhysicalAddress, bytesize OPTIONAL, OPTIONS OPTIONAL,  internalentrycount OPTIONAL, Optional1, Optional2) : 
  Starts watching writes to the given address range
  OPTIONS is a binary field.
    (1 << 0): Log the same RIP multiple times (if different registers)
    (1 << 1): Ignore the size field and log everything in the specified page
    (1 << 2): Logs record the floating point state
    (1 << 3): Logs contain a 4KB stack snapshot
    (1 << 4): does nothing
    (1 << 5): If the number of recorded entries gets bigger than internalentrycount, grow the list instead of discarding the entries
    (1 << 6): <reserved>
    (1 << 7): DBVMBP.  Not a watch! When triggered changes RIP to Optional1 if in UserMode and Optional2 if in Kernelmode.  These addresses need to contain an 0xcc (int3) . If 0 RIP will not be changed, and also not if the current state is not interuptable. Look at dbvm_bp_* functions for more information
  On success returns an ID to use with dbvm_watch_retrievelog and dbvm_watch_disable


dbvm_watch_reads(PhysicalAddress, bytesize OPTIONAL, OPTIONS OPTIONAL,  internalentrycount OPTIONAL, Optional1, Optional2) : see dbvm_watch_writes but then for reads and writes
dbvm_watch_executes(PhysicalAddress, bytesize OPTIONAL, OPTIONS OPTIONAL,  internalentrycount OPTIONAL, Optional1, Optional2) : see dbvm_watch_writes but then for executes
dbvm_watch_retrievelog(ID) : Returns an array of watch event data. (Context of the system at the time of the event, like registers)
dbvm_watch_disable(ID) : Disables the watch operation


dbvm_cloak_activate(physicalbase, virtualbase OPTIONAL): 
  Hides an executable memory range (4096 bytes) from snooping eyes
  Note: It is recommended to cause a copy-on-write on the target first, else this will affect all processes that have this memory block loaded
dbvm_cloak_deactivate(physicalbase): Disables the cloak and restores the executable memory to what the system thinks it is
dbvm_cloak_readOriginal(physicalbase): Reads the memory that will get executed.  On success returns a 4096 byte long bytetable starting from the base of the page (remember, lua indexes start at 1, so offset 0 is index 1)
dbvm_cloak_writeOriginal(physicalbase, bytetable[4096]): Writes the memory that will get executed. 

dbvm_changeregonbp(physicaladdress, changereginfo, virtualaddress OPTIONAL): boolean
  sets a breakpoint at the given position. When a breakpoint hits the registers will be changed according to the changereginfo table
    changereginfo table:  (set the field to nil, or don't define it, if you don't want to change it)
      newCF: integer/boolean (false=0, true=1) 
      newPF: integer/boolean (false=0, true=1) 
      newAF: integer/boolean (false=0, true=1) 
      newZF: integer/boolean (false=0, true=1) 
      newSF: integer/boolean (false=0, true=1) 
      newOF: integer/boolean (false=0, true=1)
      newRAX: integer
      newRBX: integer
      newRCX: integer 
      newRDX: integer
      newRSI: integer 
      newRDI: integer
      newRBP: integer 
      newRSP: integer
      newRIP: integer
      newR8:  integer
      newR9:  integer
      newR10: integer
      newR11: integer
      newR12: integer
      newR13: integer
      newR14: integer
      newR15: integer

dbvm_removechangeregonbp(physicaladdress) : Disables the changeregonbp breakpoint

dbvm_traceonbp(PhysicalAddress, stepcount, VirtualAddress, {secondaryoptions}) : Sets a int3 breakpoint at the given address after cloaking that page and when hit does a trace. 
secondaryoptions is a table:
  logFPU: boolean
  logStack: boolean         

dbvm_traceonbp_getstatus() : status, count, maxcount - Returns the status (0=no trace configured. 1=trace configured but not started yet, 2=trace configured and started, 3=trace done) and the number of steps the trace currently holds
dbvm_traceonbp_stoptrace() : requests the trace to stop
dbvm_traceonbp_remove(pa,force: boolean) - Disables the current trace and removes all results
dbvm_traceonbp_retrievelog() : Returns an array of traceentries. (Context of the system at the time of the event, like registers)

dbvm_bp_getBrokenThreadListSize() : Returns the number of breakpoint slots currently available
dbvm_bp_getBrokenThreadEventShort(id) : Returns a table with information about the specific breakpoint slow
dbvm_bp_getBrokenThreadEventFull(id) : Returns a bigger table (fpu and stack) 
dbvm_bp_setBrokenThreadEventFull(id,state) : Sets the state of the frozen thread
dbvm_bp_resumeBrokenThread(id, continueMethod) : Resumes the specific thread.  continueMethod can be 0=run, 1=step into
dbvm_bp_getProcessAndThreadIDFromEvent(ThreadEvent): processid,threadid - Returns the processid and threadid of the provided threadEvent. On failure processid will be nil, and threadid will contain text

dbvm_log_cr3_start() : Tells DBVM to record (up to 512) unique CR3 values it encounters
dbvm_log_cr3_stop() : Stops the logging and returns the results as a table

dbvm_speedhack_setSpeed(speed): Changes the speed the timestamp counter goes up (similar to speedhack in a process but affects the whole system including the clock)
dbvm_setTSCAdjust(enabled, timeout): If enabled (default true with timeout 2000) will return a small(20-30) timestamp between multiple rdtsc/rdtscp instructions.  The timeout is the number of actual TSC to watch else the actual time is given. A high timeout can make your system unstable

dbk_getCR0(): Returns Control Register 0
dbk_getCR3(): Returns Control Register 3 of the currently opened process.  (Note: This will also work without dbk when only dbvm is loaded)
dbk_getCR4(): Returns Control Register 4
dbk_getPhysicalAddress(address): Returns the physical address of the given address
dbk_writesIgnoreWriteProtection(state): Set to true if you do not wish to initiate copy-on-write behaviour


getPhysicalAddressCR3(CR3, address): Looks up the physical address for the given virtual address in the given pagetable base. Returns nil if not paged
readProcessMemoryCR3(CR3, address, size): Reads the virtual memory of the given process's CR3 value. Returns a bytetable on success, nil if fail to read (paged out)
writeProcessMemoryCR3(CR3, address, bytetable): Reads the virtual memory of the given process's CR3 value
 


allocateKernelMemory(size) : Allocates a block of nonpaged memory and returns the address
freeKernelMemory(address) : Frees the given memory region

mapMemory(address, size,  frompid OPTIONAL, topid OPTIONAL): maps a specific address to the usermode context from the given PID to the given PID. If the PID is 0 or not specified, the cheat engine process is selected. This functions returns 2 results. Address and MDL. The MDL you will need for unmapMemory()
unmapMemory(address, mdl)                                                         





onAPIPointerChange(function): Registers a callback when an api pointer is changed (can happen when the user clicks ok in settings, or when dbk_use*** is used. Does NOT happen when setAPIPointer is called)


setAPIPointer(functionid, address): Sets the pointer of the given api to the given address. The address can be a predefined address set at initialization by Cheat Engine, or an address you got from an autoassembler script or injected dll (When Cheat Engine itself was targeted)

functionid:
  0: OpenProcess
    Known compatible address defines:
      windows_OpenProcess
      dbk_OpenProcess

  1: ReadProcessMemory
    Known compatible address defines:
      windows_ReadProcessMemory
      dbk_ReadProcessMemory
      dbk_ReadPhysicalMemory
      dbvm_ReadPhysicalMemory

  2: WriteProcessMemory
    Known compatible address defines:
      windows_WriteProcessMemory
      dbk_WriteProcessMemory
      dbk_WritePhysicalMemory
      dbvm_WritePhysicalMemory


  3: VirtualQueryEx
    Known compatible address defines:
      windows_VirtualQueryEx
      dbk_VirtualQueryEx
      VirtualQueryExPhysical

Extra variables defined:
dbk_NtOpenProcess : Address of the NtOpenProcess implementation in DBK32


The dbvm_ addresses should only be used with auto assembler scripts injected into Cheat Engine
dbvm_block_interrupts  : Address of function dbvm_block_interrupts : DWORD; stdcall;
dbvm_raise_privilege   : Address of function dbvm_raise_privilege : DWORD; stdcall;
dbvm_restore_interrupts: Address of function dbvm_restore_interrupts : DWORD; stdcall;
dbvm_changeselectors   : Address of function dbvm_changeselectors(cs,ss,ds,es,fs,gs: dword): DWORD; stdcall;


D3DHOOK class:
The d3dhook functions provide a method to render graphics and text inside the game, as long as it is running in directx9, 10 or 11

createD3DHook(textureandcommandlistsize OPTIONAL, hookmessages OPTIONAL)
  Hooks direct3d and allocates a buffer with given size for storage of for the rendercommand list

  hookmessages defines if you want to hook the windows message handler for the direct3d window. The d3dhook_onClick function makes use of that


  If no size is provided 16MB is used and hookmessages is true

  Note: You can call this only once for a process

  It returns a d3dhook object

properties
  Width: Integer : The width of the screen (readonly)
  Height: integer: The height of the screen (readonly)
  DisabledZBuffer: boolean : Set this to true if you don't want previously rendered walls to overlap a newly rendered object (e.g map is rendered first, then the players are rendered)
  WireframeMode: boolean : Set this to true if you don't want the faces of 3d objects to be filled
  MouseClip: boolean : Set this if to true if you have one of those games where your mouse can go outside of the gamewindow and you don't want that.
  OnClick: function(d3dhook_sprite, x, y)
    A function to be called when clicked on an sprite (excluding the mouse)
    x and y are coordinates in the sprite object. If sprites overlap the highest zorder sprite will be given. It does NOT care if a transparent part is clicked or not

    Note: If you set this it can cause a slowdown in the game if there are a lot of sprites and you press the left button a lot

  OnKeyDown: function(virtualkey, char)
    function(vkey, char) : boolean
      A function to be called when a key is pressed in the game window (Not compatible with DirectInput8)
      Return false if you do not wish this key event to pass down to the game


methods
  beginUpdate() : Use this function when you intent to update multiple sprites,textcontainers or textures. Otherwise artifacts may occur (sprite 1 might be drawn at the new location while sprite 2 might still be at the old location when a frame is rendered)
  endUpdate() : When done updating, call this function to apply the changes
  enableConsole(virtualkey): Adds a (lua)console to the specific game. The given key will bring it up (0xc0=tilde(`~))
  createTexture(filename) : Returns a d3dhook_texture object
  createTexture(picture, transparentColor OPTIONAL): Returns a d3dhook_texture object
    if the picture is not a transparent image the transparentcolor parameter can be used to make one of it's colors transparent

  createFontmap(font) : Returns a d3dhook_fontmap object created from the given font
  createSprite(d3dhook_texture): returns a d3dhook_sprite object that uses the given texture for rendering
  createTextContainer(d3dhook_fontmap, x, y, text): Returns a d3dhook_textContainer object


D3DHook_Texture Class (Inheritance: Object)
This class controls the texture in memory. Without a sprite to use it, it won't show

properties
  Height: integer (ReadOnly)
  Width: integer (ReadOnly)
methods
  loadTextureByPicture(picture)



D3DHook_FontMap Class (Inheritance: D3DHook_Texture->Object)
A fontmap is a texture that contains extra data regarding the characters. This class is used by the textcontainer
Current implementation only supports 96 characters (character 32 to 127)

properties
  -
methods
  changeFont(font): Changes the fontmap to the selected font
  getTextWidth(string): Returns the width of the given string in pixels


D3DHook_RenderObject Class (Inheritance: Object)
The renderobject is the abstract class used to control in what manner objects are rendered.
The sprite and TextContainer classed inherit from this

properties
  X: Float - The x-coordinate of the object on the screen
  Y: Float - The y-coordinate of the object on the screen
  CenterX: Float - X coordinate inside the object. It defines the rotation spot and affects the X position
  CenterY: Float - Y " "
  Rotation: Float - Rotation value in degrees (0 and 360 are the same)
  Alphablend: Float - Alphablend value. 1.0 is fully visible, 0.0=invisible
  Visible: boolean - Set to false to hide the object
  ZOrder: integer - Determines if the object will be shown in front or behind another object
methods
  -



D3DHook_Sprite Class (Inheritance: D3DHook_RenderObject->Object)
A d3dhook_sprite class is a visible texture on the screen.


properties
  Width: Integer - The width of the sprite in pixels. Default is the initial texture width
  Height: Integer - The height of the sprite in pixels. Default is the initial texture height
  Texture: d3dhook_texture - The texture to show on the screen

methods
  -


D3Dhook_TextContainer Class (Inheritance: D3DHook_RenderObject->Object)
A d3dhook_sprite class draws a piece of text on the screen based on the used fontmap.
While you could use a texture with the text, updating a texture in memory is slow. So if you wish to do a lot of text updates, use a textcontainer

properties
  FontMap : The D3DHook_FontMap object to use for rendering text
  Text : The text to render
methods
  -




Disassembler Class (Inheritance: Object)



createDisassembler() - Creates a disassembler object that can be used to disassemble an instruction and at the same time get more data
getDefaultDisassembler() - Returns the default disassembler object used by a lot of ce's disassembler routines (Only use this from the main thread)
getVisibleDisassembler() - Deprectad. Returns a stub disassembler for backward compatability. It's function overrides are set the other visible disasemblers will use that if they themselves don't have an ovverride. Special codes are: {H}=Hex value {R}=Register {S}=Symbol {N}=Nothing special {C######}=RGB color , {B######}=Background RGB color were ###### is 0xBBGGRR 

registerGlobalDisassembleOverride(function(sender: Disassembler, address: integer, LastDisassembleData: Table): opcode, description): Same as Disassembler.OnDisassembleOverride, but does it for all disassemblers, including newly created ones.  Tip: Check the sender to see if you should use syntax highlighting codes or not
  This function returns an ID you can pass on to unregisterGlobalDisassembleOverride()  6.4+

unregisterGlobalDisassembleOverride(id)

properties
  LastDisassembleData : Table
  OnDisassembleOverride: function(sender: Disassembler, address: integer, LastDisassembleData: Table): opcode, description
  OnPostDisassemble: function(sender: Disassembler, address: integer, LastDisassembleData: Table, result: string, description: string): result, description
  syntaxhighlighting: boolean : This property is set if the syntax highlighting codes are accepted or not

Methods
  disassemble(address): Disassembles the given instruction and returns the opcode. It also fills in a LastDisassembleData record
  decodeLastParametersToString() : Returns the unedited "Comments" information. Does not display userdefined comments
  getLastDisassembleData() : Returns the LastDisassembleData table.
    The table is build-up as follow:
      address: integer - The address that was disassembled
      opcode: string - The opcode without parameters
      parameters: string - The parameters
      description: string - The description of this opcode
      commentsoverride: string - If set, this will be the comments/LastParamatersToString result
      bytes: table - A table containing the bytes this instruction consists of (1.. )

      modrmValueType: DisAssemblerValueType  - Defines the type of the modrmValue field (dvtNone=0, dvtAddress=1, dvtValue=2)
      modrmValue: Integer - The value that the modrm specified. modrmValueType defines what kind of value

      parameterValueType: DisAssemblerValueType
      parameterValue: Integer - The value that the parameter part specified

      isJump: boolean - Set to true if the disassembled instruction can change the EIP/RIP (not ret)
      isCall: boolean - Set to true if it's a Call
      isRet: boolean - Set to true if it's a Ret
      isRep: boolean - Set to true if it's preceded by a Rep
      isConditionalJump: boolean - Set to true if it's a conditional jump



DissectCode class: (Inheritance: Object)
getDissectCode() : Creates or returns the current code DissectCode object

properties:
methods:
  clear() : Clears all data
  dissect(modulename) : Dissects the memory of a module
  dissect(base,size) : Dissect the specified memory region

  addReference(fromAddress, ToAddress, type, OPTIONAL isstring):
    Adds a reference. Type can be jtCall, jtUnconditional, jtConditional, jtMemory
    In case of jtMemory setting isstring to true will add it to the referenced strings list

  deleteReference(fromAddress, ToAddress)


  getReferences(address) : Returns a table containing the addresses that reference this address and the type
  getReferencedStrings(): Returns a table of addresses and their strings that have been referenced. Use getReferences to find out which addresses that are
  getReferencedFunctions(): Returns a table of functions that have been referenced. Use getReferences to find out which callers that are

  saveToFile(filename)
  loadFromFile(filename)

RIPRelativeScanner class: (Inheritance: Object)
createRipRelativeScanner(startaddress, stopaddress, includejumpsandcalls OPTIONAL):
createRipRelativeScanner(modulename, includejumpsandcalls OPTIONAL): Creates a RIP relative scanner. This will scan the provided module for RIP relative instructions which you can use for whatever you like
properties:
  Count: integer - The number of instructions found that have a RIP relative address
  Address[]: integer - An array to access the results. The address is the address of the RIP relative offset in the instruction

methods:
-
 



LuaPipe class: (Inheritance: Object)
  Abstract class that LuaPipeServer and LuaPipeclient inherit from. It implements the data transmission methods

properties
  Connected: boolean: True if the pipe is connected

methods
  lock() : Acquire a lick on this pipe till unlock is called. If lock can not be acquired, wait. Recursive calls are allowed
  unlock()
  writeBytes(ByteTable, size OPTIONAL): Writes the provided byte table to the pipe. if size is not provided, the whole table is sent. Returns the number of bytes sent, or nil on failure
  readBytes(size: integer): returns a byte table from the pipe, or nil on failure

  readDouble(): Read a double from the pipe, nil on failure
  readFloat(): Read a float from the pipe, nil on failure
  readQword(): Read an 8 byte value from the pipe, nil on failure
  readDword(): Read a 4 byte value from the pipe, nil on failure
  readWord(): Read a 2 byte value from the pipe, nil on failure
  readByte(): Read a byte from the pipe, nil on failure

  readString(size: integer): Reads a string from the pipe, nil on failure.  (Can support 0-byte chars)
  readWideString(size: integer): Reads a widestring from the pipe, nil on failure

  writeDouble(v: double): Writes a double to the pipe. Returns the number of bytes sent, nil on failure
  writeFloat(v: single): writes a float to the pipe. Returns the number of bytes sent, nil on failure
  writeQword(v: qword): writes an 8 byte value to the pipe. Returns the number of bytes sent, nil on failure
  writeDword(v: dword): writes a 4 byte value to the pipe. Returns the number of bytes sent, nil on failure
  writeWord(v: word): writes a word to the pipe. Returns the number of bytes sent, nil on failure
  writeByte(v: byte): writes a byte to the pipe. Returns the number of bytes sent, nil on failure

  writeString(str: string; include0terminator: boolean OPTIONAL); Writes a string to the pipe. If include0terminator is false or not provided it will not write the 0 terminator byte.  Returns the number of bytes written, or nil on failure
  writeWideString(str: widestring; include0terminator: boolean OPTIONAL); Writes a widestring to the pipe. If include0terminator is false or not provided it will not write the 0 terminator bytes. Returns the number of bytes written, or nil on failure

LuaPipeClient class: (Inheritance: LuaPipe>Object)
Class implementing a client that connects to a pipe

connectToPipe(pipename,timeout OPTIONAL): Returns a LuaPipeClient connected to the given pipename. Nil if the connection fails. Timeout is number of milliseconds before it disconnects on read/write operations. 0 or nil means never

properties:
methods:
-

LuaPipeServer Class: (Inheritance: LuaPipe>Object)
  Class launching the server side of a pipe

createPipe(pipename, inputsize OPTIONAL, outputsize OPTIONAL) : Creates a LuaPipeServer which can be connected to by a pipe client. InputSize and Outputsize define buffers how much data can be in the specific buffer before the writer halts.  Default input and output size is 4096 for both

properties
  valid: boolean - Returns true if the pipe has been created properly. False on failure (e.g wrong pipename)
  handle: integer - The handle of the pipe serverside (this can be used with duplicateHandle to get a handle into the target process)


methods
  acceptConnection() - Waits for a client to connect to this pipe (Warning: Freezes the thread this is executed in)



openLuaServer(Name):
  Opens a pipe with the given name. The LuaClient dll needs this name to connect to ce


  LuaClient.dll functions:  (STDCALL calling machanic)
    BOOL CELUA_Initialize(char *name) : Initializes
    UINT_PTR CELUA_ExecuteFunction(char *luacode, UINT_PTR parameter)
      This function executes a lua function with parameters (parameter) and with the luacode as body Parameter will be treated as an integer
      In short:
        function(parameter)
          <luacode>
        end


    the return value of this function is the return value of the lua function (integer)

    UINT_PTR CELUA_ExecuteFunctionAsync(char *luacode, UINT_PTR parameter)
      See CELUA_ExecuteFunction but runs in the server thread instead of passing it to the main GUI and then wait for it's return

    integer CELUA_GetFunctionReferenceFromName(char *functionname): Returns a reference ID you can pass on to CELUA_ExecuteFunctionByReference
    UINT_PTR CELUA_ExecuteFunctionByReference(int refid, int paramcount, PVOID *parameters, BOOL async):
      This functions executes the function specified by reference id. If async is true, the code will run in a seperate thread instead of the main thread
      paramcount is the number of parameters to pass on to the function
      parameters is a pointer to a list of integers.  32-bit in 32-bit targets, 64-bit in 64-bit targets



Settings class
  This class can be used to read out and set settings of cheat engine and of plugins, and store your own data

global functions
  reloadSettingsFromRegistry(): This will cause cheat engine to reload the settings from the registry and apply them

  getSettings(path Optional): Settings - Returns a settings object. If path is nil it will point to the Cheat Engine main settings (Registry) . If name is provided the settings currently accessed will be the one at the subkey provided
  Note: Keep in mind that it returns a new object each call, even if he same name is used multiple times


properties
  Path: string - Gets/Sets the current subkey (nil if main)
  Value[]: A table access into the settings. e.g: Value["Count"]=12  .Setting vcalue to nil will delete it
  [] : Same as Value[]

methods
  getBinaryValue(name, stream) : Gets binary data from the registry value. Adds it after the current 'position'
  setBinaryValue(name, stream, size OPTIONAL) : Sets binary data in the registry value. If size is given, write from the current position. If not, or size=0, writes from position 0 to the end
  getBinaryValue(name): bytetable
  setBinaryValue(name, bytetable)




SymbolList class
  This class can be used to look up an address to a symbolname, and a symbolname to an address
  It can also be registered with the internal symbol handler of cheat engine

  This class makes use of a special "Symbol" table construction that contains size and optionally other data
    Symbol Table:
      modulename: string
      searchkey: string
      address: integer
      symbolsize: integer

Global functions
  createSymbolList() : Creates an empty symbollist
  getMainSymbolList(): Returns the symhandler internal symbol list (Note: This does not contain .net, modulelist, or other info)
  enumRegisteredSymbolLists() : Returns a table containing all the registered symbollists


Properties
  PID: integer - The processid it refers to
  Name: string - A name that can be set to make it easier to identify

Methods
  clear()
  getSymbolFromAddress(address) : Searches the list for the given address. The address does not have to match the exact address. As long as it falls withing the range
  getSymbolFromString(searchkey)
  addModule(modulename, modulepath, address, size, is64bit)
  deleteModule(modulename)
  deleteModule(address)  
  addSymbol(modulename, searchkey, address, symbolsize, skipAddressToSymbolLookup OPTIONAL, extradata OPTIONAL)
    Adds a symbol to the symbollist
    extradata is a table which can be used to fill in a return type and parameters for function calls. It has the following fields:
      returntype: string
      parameters: string

  deleteSymbol(searchkey)
  deleteSymbol(address)
  register() : Registers the current symbol list with the symbol handler
  unregister(): Unregisters the current symbol list from the symbol handler
  getModuleList(): Returns an indexed table with all the modules
  getSymbolList(): Returns an unindex table with each symbol being an element containing an address


Pagecontrol Class (WinControl->Control->Component->Object)
  This is an object that can hold multiple pages

global functions
  createPageControl(owner)
properties
  ShowTabs: boolean - Shows the tabs
  TabIndex: integer - Gets and sets the current tab
  ActivePage: TabSheet - Returns the current tabsheet.
  PageCount: integer - Gets the number of pages
  Page[]: TabSheet - Get a specific page (TabSheet)
methods
  addTab() : TabSheet - Creates a new TabSheet
  tabRect(index): Rect - returns a rect table describing the position of the specific tab

TabSheet class (WinControl->Control->Component->Object)
  Part of a page control. This object can contain other objects
properties
  TabIndex: integer - the current index in the pagelist of the owning pagecontrol
methods

Internet class (Object)
global functions
  getInternet(string) - Returns an internet class object.  The string provided will be the name of the client provided

properties
  Header : string - the additional header to be sent with the next getURL request
methods
  getURL(path) - returns a string containing the contents of the url. nil on failure
  postURL(path, urlencodeddata) - posts the given data to the path and returns the results


CustomType class (Object)
The custom type is an convertor of raw data, to a human readable interpretation.

global functions
  registerCustomTypeLua(typename, bytecount, bytestovaluefunction, valuetobytesfunction, isFloat)
    Registers a Custom type based on lua functions
    The bytes to value function should be defined as "function bytestovalue (b1,b2,b3,b4)" and return an integer as result
    The value to bytes function should be defined as "function valuetobytes (integer)" and return the bytes it should write

    returns the Custom Type object


  registerCustomTypeAutoAssembler(script)
    Registers a custom type based on an auto assembler script. The script must allocate an "ConvertRoutine" and "ConvertBackRoutine"

    returns the Custom Type object

  getCustomType(typename) : Returns the custom type object, or nil if not found

properties
  name: string
  functiontypename: string
  CustomTypeType: TCustomTypeType - The type of the script
  script: string - The custom type script
  scriptUsesFloat: boolean - True if this script interprets it's user side values as float

methods
  byteTableToValue({bytetable},Address Optional)
  valueToByteTable(value, Address Optional)

TFrmTracer class (Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object)

properties
  Count: integer - number of entries in the list
  SelectionCount: integer - The number of selected entries

  Entry[index]: table - Information about each entry. Read only. (Index starts at 0)
    table is formatted as:
    {
      address: integer - address of the instruction
      instruction: string - disassembled instruction
      instructionSize: integer - bytesize of the instruction
      referencedAddress: integer - address the code references
      referencedData: bytearray - The bytes of the referenced data at the time of tracing
      context: contexttable - the state of the cpu when this instruction got executed (contains registers(EAX/RAX, ...), floating points(FP) and XMM values
      hasStackSnapshot: boolean - set to true if there is a stack entry      
      selected: boolean - Set to true if the entry is selected

    }


  StackEntry[index]: bytearray - The stacksnapshot of that entry. Nil if not available

methods



TfrmUltimap2 class(Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object) 
getUltimap2(): TfrmUltimap2 - Returns the ultimap2 form, nil if not open

properties
  Count: integer - The number of entries in the list (READONLY)
methods
  isInList(address): boolean,count - returns true if the current address is in the list of addresses. In case of true, it also returns the count value (up to 255)

TfrmCodeFilter class(Inheritance: Form->ScrollingWinControl->CustomControl->WinControl->Control->Component->Object) 
getCodeFilter(): TfrmCodeFilter - Returns the codefilter form

properties
methods
  isInList(address): boolean - Returns true if this address is in the list


----SQL Classes----
CustomConnection class (Inheritance: Component->Object)
properties
  Connected: Boolean - Gets the current connection state, and lets you connect as well
  LoginPrompt: Boolean
  AfterConnect: function(sender)
  AfterDisconnect: function(sender)
  BeforeConnect: function(sender)
  BeforeDisconnect: function(sender)
  
methods
  close(forceClose:Boolean Optional)
  open()


Database Class (Inheritance: CustomConnection->Component->Object)
properties
  Connected: Boolean - Sewt this to true to activate the connection. (turns back to false on failure)
  DatabaseName: string
  KeepConnection: Boolean
  Params: Strings 
  TransactionCount: integer readonly

methods

SQLConnection Class (Inheritance: Database->CustomConnection->Component->Object)
properties
  Password: String
  UserName: string
  Transaction: SQLTransaction - SQLTransaction object. Needs to be set
  CharSet: string
  HostName: string
  Options: string set - [scoExplicitConnect, scoApplyUpdatesChecksRowsAffected]

methods
  startTransaction()
  endTransaction()
  executeDirect(sql)
  getTableNames() : Returns a counted table with all tablenames


SQLite3Connection class(Inheritance: SQLConnection->Database->CustomConnection->Component->Object) 
createSQLite3Connection(owner) - creates an SQLite3Connection object
setSQLiteLibraryName(pathwithdllname)- Lets you set the path to the sqlite3.dll in case it's not .\win*\sqlite3.dll

properties
methods
  createDB()
  dropDB()
  getInsertID(): integer

ODBCConnection class(Inheritance: SQLConnection->Database->CustomConnection->Component->Object) 
createODBCConnection(owner) - creates an ODBCConnection object
properties
  DatabaseName: string - Name of the odbc connection
  Driver: string
  FileDSN: string

methods



DBTransaction class (Inheritance: Component->Object)
properties
  Active: boolean
  DataBase: Database
methods
  closeDataSets()

SQLTransaction class (Inheritence: DBTransaction->Component->Object)
createSQLTransaction(owner): Creates an SQLTransaction object
properties
  SQLConnection: SQLConnection
  Params: StringList
  Options: string - set of [stoUseImplicit, stoExplicitStart]
  Action: string - options between caNone, caCommit, caCommitRetaining, caRollback,
    caRollbackRetaining

methods
  commit()  
  commitRetaining()
  rollback()
  rollbackRetaining()
  startTransaction()
  endTransaction()


Param class (Inheritence: CollectionItem->Object))
properties
  Name: string
  Value: something
  DataType: string
  AsBoolean
  AsByteTable
  AsInteger
  AsNumber
  AsString
  Text  
  Size
  Precision
  IsNull: boolean

   
methods



Params class (Inheritence: Collection->Object)
properties
  Items[index]: Param

methods
  AddParam(Param)


Field class (Inheritance: Component->Object)
properties
  FieldName: string
  Index: integer
  Value: something
  DataType: string
  AsBoolean
  AsByteTable
  AsInteger
  AsNumber
  AsString
  Text  
  Size
  IsNull: boolean
  
methods


Fields class (Inheritence: Object)
properties
  Count: integer
  Fields[index]: Field
methods
  add(Field)
  clear()
  fieldByName(name): Field
  fieldByNumber(integer): Field
  indexOf(field): integer



Dataset class (Inheritance: Component->Object)
properties
  BlockReadSize: integer
  BOF: boolean; READONLY
  CanModify: boolean READONLY
  DefaultFields: boolean READONLY
  EOF: boolean; READONLY
  FieldCount: integer; READONLY
  Fields: Fields READONLY
  Found: boolean READONLY
  Modified: boolean READONLY
  IsUniDirectional: boolean READONLY
  RecordCount: integer READONLY
  RecNo: integer
  
  FieldValues[fieldname]: something
  Filter: string
  Filtered: boolean
  FilterOptions: set of [foCaseInsensitive, foNoPartialCompare]
  Active: boolean
  AutoCalcFields: boolean


methods
  append()
  appendRecord({values})
  cancel()
  checkBrowseMode()
  clearFields()
  close();
  controlsDisabled(): boolean
  cursorPosChanged;
  delete;
  disableControls;
  edit;
  enableControls;
  fieldByName(fieldname): Field
  findField(fieldname): Field
  findFirst() boolean
  findLast()
  findNext()
  findPrior()
  first()
  insert()
  isEmpty()
  last()
  locate(KeyFields, KeyValues, options:"[loCaseInsensitive, loPartialKey]"): boolean
  lookup(keyfields, KeyValues, ResultFields): something
  moveBy(distance)
  next()
  open()
  post()
  prior()
  refresh()
  updateCursorPos()
  updateRecord() 



DBDataset class (Inheritance: Dataset->Component->Object)
properties
  DataBase: Database
  Transaction: DBTransaction

methods
-


CustomBufDataset class (Inheritance: DBDataset->Dataset->Component->Object)
properties
  FileName: string
  PacketRecords: integer
  UniDirectional: boolean
  IndexName: string
  MaxIndexesCount: integer
  ChangeCount: integer
  ReadOnly: boolean

methods
  applyUpdates(MaxErrors Optional)
  cancelUpdates()  
  loadFromStream(stream)
  saveToStream(stream)
  loadFromFile(filename)
  saveToFile(filename)
  createDataset()


CustomSQLQuery class (Inheritance: CustomBufDataset->DBDataset->Dataset->Component->Object) 
properties
  prepared: boolean READONLY
  SQLConnection: SQLConnection
  SQLTransaction: SQLTransaction


      
methods
  prepare()
  unprepare()
  execSQL()
  rowsAffected()
  paramByName(paramname): Param




SQLQuery class (Inheritance: CustomSQLQuery->CustomBufDataset->DBDataset->Dataset->Component->Object) 
createSQLQuery(owner)
properties
  Database: Database

  SchemaType: string READFONLY - can be: stNoSchema, stTables, stSysTables, stProcedures, stColumns, stProcedureParams, stIndexes, stPackages, stSchemata, stSequences
  StatementType: string READONLY - can be :stUnknown, stSelect, stInsert, stUpdate, stDelete,
      stDDL, stGetSegment, stPutSegment, stExecProcedure,
      stStartTrans, stCommit, stRollback, stSelectForUpd

  Params: Params object
  ParamCheck: Boolean
  ParseSQL: Boolean
  UpdateMode: string - can be :upWhereAll, upWhereChanged, upWhereKeyOnly
  UsePrimaryKeyAsKey: boolean
  ReadOnly: boolean


  SQL: string
  InsertSQL: stringlist
  UpdateSQL: stringlist
  DeleteSQL: stringlist
  RefreshSQL: stringlist
  Options: string - set of [sqoKeepOpenOnCommit, sqoAutoApplyUpdates, sqoAutoCommit, 
      sqoCancelUpdatesOnRefresh, sqoRefreshUsingSelect]


methods
  -

----------------------------------------------------------

HotkeyHandlerThread(Inheritence: Thread)
getHotkeyHandlerThread() : Returns the hotkey handler thread used internally by CE

properties
  state: 0 ('htsActive')=Active , 1('htsMemrecOnly')=Memory records only, 2('htsNoMemrec')=Everything except memoryrecords, 3('htsDisabled')=disabled

methods
  -

RemoteThread class(Inheritance: -)
createRemoteThread(address, parameter)

properties
  Result : The 32-bit value returned by the thread 

methods
  waitForThread(timeout OPTIONAL) : Waits for the thread to finish. Timeout is time in milliseconds. If nil, the timeout it infinite. If 0, it returns without wait

ModuleLoader(Inheritance: -)
loadModule(pathtodll, executeEntryPoint OPTIONAL default=true, timeout OPTIONAL default=nil=infinite)

properties:
  loaded: boolean - true if successfuly mapped
  exports: Table containing all exports
  entryPoint: integer - address of the entrypoint
  

WriteLog class(Inheritence: -)
The writelog is the log that keeps all writes (when enabled)

properties
  status: boolean
  logsize: integer 

methods
  getLog(): table - Returns an indexed table with the write logs. each entry has a table with the fields: address, original and new


DotNetDataCollector class
getDotNetDataCollector() - Returns the current dotnetdatacollector object

properties
Attached: boolean - Returns true if attached to a process


methods
enumDomains(): table - Returns an index table containing all domains. Each entry is build up as {DomainHandle, Name}
enumModuleList(DomainHandle) : table - Returns an indexed table containing information about all modules. Each module entry is build up as {ModuleHandle, BaseAddress, Name}
enumTypeDefs(ModuleHandle) : table - Returns an indexed table containing information about all TypeDefs (classes) . Each entry is build up as {TypeDefToken, Name, Flags, Extends}
getTypeDefMethods(ModuleHandle, TypedefToken) : table - Returns a table containing all the methods in the specified typedef. Each entry is build up as {MethodToken, Name, Attributes, ImplementationFlags, ILCode, NativeCode, SecondaryNativeCode[]: Integer)
getTypeDefParent(ModuleHandle, TypedefToken): {ModuleHandle, TypedefToken}
getTypeDefData(ModuleHandle, TypedefToken) : table - Returns a table containing all the fields in the specified typedef.  {ObjectType, ElementType, CountOffset, ElementSize, FirstElementOffset, ClassName, Fields[]{Offset, FieldType, Name} }
getMethodParameters(ModuleHandle, MethodDefToken): table - Returns a table containing all the parameters of the for method. {Name, CType}
getAddressData(address): table - Queries a specific address and returns information about it, assuming it is a valid object. It contains the following data: {StartAddress, ObjectType, ElementType, CountOffset, ElementSize, FirstElementOffset, ClassName, Fields[]{Offset, FieldType, Name} }

enumAllObjects(): table - Queries ALL defined objects. {StartAddress, Size, TypeID{token1,token2}, ClassName}   WARNING: This will take a LOOOOOONG time and if done from the main thread will make it look like CE is frozen
enumAllObjectsOfType(ModuleHandle, TypedefToken): {} - Returns a list of addresses that have this type




Diagram class(Inheritance: CustomControl->WinControl->Control->LclComponent->Component->Object):
The diagram class lets you represent data using blocks and lines.

createDiagram(owner)

properties
  LineThickness: integer - Default thickness of lines in pixels
  LineColor: integer - Sets the default color of lines
  PlotPointColor: integer - Sets the default color for points
  BlockBackground: integer - Color of the diagramBlocks
  BackgroundColor: integer - Color of the diagram background
  ArrowStyles: string - can be one or more of the following between [ and ] : 
                          asOrigin : There will be an arrow at the point of origin
                          asDestination : There will be an arrow at the destination
                          asPoints: There will be an arrow at plot point locations
                          asCenterBetweenPoints: There will be an arrow between two points
                          asCenter: There will be an arrow in the center of the line

  BlockCount: integer - Returns the number of blocks in the diagram (readonly)
  Block[index]: DiagramBlock - Returns the block at the specific index
  LinkCount: integer - Returns the number of linkes in the diagram (readonly)
  Link[index]: DiagramLink - Returns the link at the specific index
  DrawPlotPoints: boolean - If set to true linkpoints will be shown
  AllowUserToCreatePlotPoints: boolean - If true(default) will allow the user to create plotpoints by clicking on lines
  AllowUserToMovePlotPoints: boolean - If true(default) will allow the user to move plotpoints by dragging them
  AllowUserToResizeBlocks: boolean - If true(default) will allow the user to resize blocks
  AllowUserToMoveBlocks: boolean - If true(default) will allow the user to move blocks around by draging the caption
  AllowUserToChangeAttachPoints: boolean - If true(default) will allow the user to move move the point where a line connects to the block by dragging it
  ScrollX: integer - The horizontal scroll
  ScrollY: integer - The vertical scroll
  Zoom: float - The zoom level to use 




methods
  createBlock(): DiagramBlock - Creates a new uninitialized block
  addConnection(Source: DiagramBlock, Destination: DiagramBlock): DiagramLink - Creates a link between the two blocks
  addConnection(Source: BlockSideDescriptorTable, Destination: BlockSideDescriptorTable) - Creates a link using the BlockSideDescritorTable table definition
      BlockSideDescriptorTable=
      {
         Block: DiagramBlock - The block to attach to
         Side: integer - One of the blockside typedefs: dbsTop=0, dbsLeft=1, dbsRight=2, dbsBottom=3, dbsTopLeft=4, dbsTopRight=5, dbsBottomLeft=6, dbsBottomRight=7
         Position: integer - Position on the provided side based on the center. Only for Sides 0 to 3
      } 

  saveAsImage(filenamepng): saves the current display as an PNG image
  saveToFile(filename): Saves the state of the diagram to a file
  loadFromFile(filename): loads the state of the diagram from a file
  saveToStream(stream): Saves the state of the diagram to a stream
  loadFromStream(stream): loads the state of the diagram from a stream
  getObjectAt({x,y}): Returns the object at this position. nil if nothing
  


DiagramBlock class:
The diagramBlock is a block with a header and body which can contain text (ansi escape codes supported) 

properties
  Owner: Diagram - The diagram that this block is in
  X: integer - x-position of the block
  Y: integer - y-position of the block
  Width: integer - Width of the block
  Height: integer - Height of the block
  Caption: string - Header of the block (ansi escape codes supported)
  Strings: Strings - Strings object containing the lines of the block (ansi escape codes supported)
  BackgroundColor: integer - When set overrides the default color for the block to the given one
  TextColor: Integer - The starting/default textcolor
  Name: string - The name of the block
  AutoSize: boolean - If true the width and height of the box will adjust to the given Caption and Strings
  AutoSide: boolean - If true the connection side of a link will be picked for you instead of providing the side yourself
  AutoSideDistance: integer - If autoside is true and there are multiple lines on the same side, this determines the distance between
  ShowHeader: boolean - If true show ther header. (default true)
  DragBody: boolean - If true allows dragging of the body. Useful when there is no header (default false)
  Tag: integer - Use for whatever you like
  OnDoubleClickHeader: function(DiagramBlock) - Function to call when the block's header is doubleclicked
  OnDoubleClickBody: function(DiagramBlock) - Function to call when the block's body is doubleclick
  OnRenderHeader: function(sender,rect,beforeownerdraw): boolean - Function to call when the header is being rendered. This is called twice, before and after the normal painting code. In case of before and the function returns nil or false, the original text will not be drawn
  OnRenderBody: function(sender,rect,beforeownerdraw): boolean - ^ but then for body
  OnDragStart: funtion(DiagramBlock) - Called when a block starts getting dragged
  OnDrag: function(DiagramBlock) - Called when a block is dragged around
  OnDragEnd: function(DiagramBlock) - Called when a dragged block is released

methods
  getLinks(): table - Returns a table two elements: 'asSource' and 'asDestination'. each of those will have a table with DiagramLinks linking with the box
  overlapsWith(block): boolean - Returns true if the two blocks overlap
  intersectsWithLine({x,y},{x,y}): boolean,intersectpoint - Returns true and the point of intersection or false if no itersection


DiagramLink class:
Links between blocks

properties
  OriginBlock: DialogBlock - The source of the link 
  DestinationBlock: DialogBlock - The destination of the link
  OriginDescriptor: BlockSideDescriptorTable
  DestinationDescriptor: BlockSideDescriptorTable   
  PointCount: integer - The number of points in the table
  Points[index]: table{x,y} - Return a table with x,y coordinates for the point at the given index (index starts at 0)
  LineColor: integer - Color of the line , when set overrides the default
  Linethickness: integer - thickness of the line, when set overrides the default
  ArrowStyles: string - See diagram ArrowStyles
  Name: string - Name of the link
  Tag: integer - Use for whatever youy like
  OnDblClick: function(sender) - Function to call when the link is doubleclicked

methods
  hasLinkToBlock(DiagramBlock): boolean - Returns true/false depending on if this link has a connection to the provided block
  reset() - Sets all custom colors sizes back to default
  updateSide(BlockSideDescriptorTable): Updates the side of the block described by the BlockSideDescriptorTable   
  getPointIndexAt(x,y): integer - Returns the pointindex at the given x, y coordinate
  addPoint(x,y,index OPTIONAL): creates a point. If no index is given if inside the line at that line index, else at the end of the list.  If a index is given at that specific index. 
  removeAllPoints(): Removes all points


RemoteExecutor class
The remoteExecute class creates an executor thread inside the target process waiting for commands to execute specific functions
An executor can only run one piece of code at a time, but you can have more than one executor

createExecuteMethodStub(callmethod, address, classregisternr, {type=typenr},typenr,{type=5, size=y, isOutputOnly=true/false, isInputOnly=true/false }, ....) - Creates an ExecuteCodeExStub object which the executor can execute
createExecuteCodeExStub(callmethod, address, {type=typenr},typenr,{type=5, size=y, isOutputOnly=true/false, isInputOnly=true/false }, ....) - Creates an ExecuteCodeExStub object which the executor can execute
createRemoteExecutor() - creates a new remote executor

properties

methods
  executeStub(ExecuteCodeExStub,{parameters},timeout,waittilldone) 

CECustomButton class(Inheritance: CustomControl->WinControl->Control->Component->Object)
A more customizable button instead of the windows theme'd button, and lets you repaint it from scratch as well

createCECustomButton(owner)

properties
  ShowPrefix: boolean - Process first single '&' per line as an underscore and draw '&&' as '&'  
  BorderColor: Color  - The color of the button border
  BorderSize: integer - The thickness of the border
  ButtonColor: Color - The color of the button face
  ButtonHighlightedColor: Color  - The color of the buttonface when highlighted(hovered over with the mouse)
  ButtonDownColor: Color - The color of the buttonface when the mouse is pressed down on it
  DrawFocusRect: boolean   - If true will draw a focus roundrect showing it has focus
  DrawBorder: boolean - default=true.  Will draw a border around the button
  FocusedSize: integer - The with of the focus roundrect
  FocusElipseColor: Color - The color of the focus roundrect
  GrowFont: boolean read - When true the font will get resized till the caption fits the button
  RoundingX: integer 
  RoundingY: integer 
  CustomDrawn: boolean - Do your own drawing in the OnPaint property of the button
  FramesPerSecond: integer - If animation is used this will determine how often per second the OnPaint gets called
  ButtonAnimationSpeed: integer - If not customdrawn, this determnines how long the animations for enter/leave take
                                                                                                                      

methods
  startAnimatorTimer() - Starts the animator timer which will trigger an OnPaint with the speed of the current framesPerSecond property
  stopAnimatorTimer() - Stops the animator timer


------- XML ------- 
DOMNode class(Inheritance:)
properties
methods
  writeToFile(filename)
  writeToStream(stream)


DOMDocument class(Inheritance: DOMNode_TopLevel->DOMNode_WithChildren->DOMNode)
properties
methods


XMLDocument class(Inheritance: DOMDocument->DOMNode_TopLevel->DOMNode_WithChildren->DOMNode)
createXMLDocument() - Creates an empty XML document
createXMLDocumentFromFile(filename) - reads the given filename and return an XMLDocument with the parsed contents of the file
