createXMLDocumentFromStream(stream) - reads the given stream and returns an XMLDocument with the parsed contents of the stream

properties
methods

VirtualTreeColumn class(Inheritance: CollectionItem->Persistent->Object):
properties
  Index: integer - The position of this column in the header
  Text: string - the text the column shows
  Visible: shortcut for coVisible in Options
  Options: set(string):  a comma seperated list of the folowing options:
             coAllowClick           - Column can be clicked (must be enabled too).
             coDraggable            - Column can be dragged.
             coEnabled              - Column is enabled.
             coParentBidiMode       - Column uses the parent's bidi mode.
             coParentColor          - Column uses the parent's background color.
             coResizable            - Column can be resized.
             coShowDropMark         - Column shows the drop mark if it is currently the drop target.
             coVisible              - Column is shown.
             coAutoSpring           - Column takes part in the auto spring feature of the header (must be resizable too).
             coFixed                - Column is fixed and can not be selected or scrolled etc.
             coSmartResize          - Column is resized to its largest entry which is in view (instead of its largest visible entry).
             coAllowFocus           - Column can be focused.
             coDisableAnimatedResize- Column resizing is not animated.
             coWrapCaption          - Caption could be wrapped across several header lines to fit columns width.
             coUseCaptionAlignment  - Column's caption has its own aligment.
             coEditable             - Column can be edited                      
    
methods

VirtualTreeColunmns class:
properties
methods
  add(text OPTIONAL) : Created ands returns a new VirtualTreeColumn object

Header class:
properties
  AutoSizeIndex: integer - When Options contains hoAutoResize this determines which column will be resized on resize of the control
  AutoResize: boolean - shortcut to access the hoAutoResize flag in Options
  Columns: VirtualTreeColunmns  
  Options: set(string) - Options is a comma seperated string which can be one of the following:
              hoAutoResize            - Adjust a column so that the header never exceeds the client width of the owner control.
              hoColumnResize          - Resizing columns with the mouse is allowed.
              hoDblClickResize        - Allows a column to resize itself to its largest entry.
              hoDrag                  - Dragging columns is allowed.
              hoHotTrack              - Header captions are highlighted when mouse is over a particular column.
              hoOwnerDraw             - Header items with the owner draw style can be drawn by the application via event.
              hoRestrictDrag          - Header can only be dragged horizontally.
              hoShowHint              - Show application defined header hint.
              hoShowImages            - Show header images.
              hoShowSortGlyphs        - Allow visible sort glyphs.
              hoVisible               - Header is visible.
              hoAutoSpring            - Distribute size changes of the header to all columns, which are sizable and have the// coAutoSpring option enabled.
              hoFullRepaintOnResize   - Fully invalidate the header (instead of subsequent columns only) when a column is resized.
              hoDisableAnimatedResize - Disable animated resize for all columns.
              hoHeightResize          - Allow resizing header height via mouse.
              hoHeightDblClickResize  - Allow the header to resize itself to its default height.
              hoHeaderClickAutoSort   - Clicks on the header will make the clicked column the SortColumn or toggle sort direction if it already was the sort column             

  
methods


StringTreeOptions class:
properties
    AnimationOptions: comma seperated string containing one or more of:
           toAnimatedToggle           - Expanding and collapsing a node is animated (quick window scroll).
           toAdvancedAnimatedToggle   - Do some advanced animation effects when toggling a node.        

    AutoOptions: comma seperated string containing one or more of: 
           toAutoDropExpand           - Expand node if it is the drop target for more than a certain time.
           toAutoExpand               - Nodes are expanded (collapsed) when getting (losing) the focus.
           toAutoScroll               - Scroll if mouse is near the border while dragging or selecting.
           toAutoScrollOnExpand       - Scroll as many child nodes in view as possible after expanding a node.
           toAutoSort                 - Sort tree when Header.SortColumn or Header.SortDirection change or sort node if child nodes are added.
           toAutoSpanColumns          - Large entries continue into next column(s) if there's no text in them (no clipping).
           toAutoTristateTracking     - Checkstates are automatically propagated for tri state check boxes.
           toAutoHideButtons          - Node buttons are hidden when there are child nodes, but all are invisible.
           toAutoDeleteMovedNodes     - Delete nodes which where moved in a drag operation (if not directed otherwise).
           toDisableAutoscrollOnFocus - Disable scrolling a node or column into view if it gets focused.
           toAutoChangeScale          - Change default node height automatically if the system's font scale is set to big fonts.
           toAutoFreeOnCollapse       - Frees any child node after a node has been collapsed (HasChildren flag stays there).
           toDisableAutoscrollOnEdit  - Do not center a node horizontally when it is edited.
           toAutoBidiColumnOrdering   - When set then columns (if any exist) will be reordered from lowest index to highest index and vice versa when the tree's bidi mode is changed.          

    MiscOptions: comma seperated string containing one or more of:
           toAcceptOLEDrop            - Register tree as OLE accepting drop target
           toCheckSupport             - Show checkboxes/radio buttons.
           toEditable                 - Node captions can be edited.
           toFullRepaintOnResize      - Fully invalidate the tree when its window is resized (CS_HREDRAW/CS_VREDRAW).
           toGridExtensions           - Use some special enhancements to simulate and support grid behavior.
           toInitOnSave               - Initialize nodes when saving a tree to a stream.
           toReportMode               - Tree behaves like TListView in report mode.
           toToggleOnDblClick         - Toggle node expansion state when it is double clicked.
           toWheelPanning             - Support for mouse panning (wheel mice only). This option and toMiddleClickSelect are mutal exclusive, where panning has precedence.
           toReadOnly                 - The tree does not allow to be modified in any way. No action is executed and node editing is not possible.
           toVariableNodeHeight       - When set then GetNodeHeight will trigger OnMeasureItem to allow variable node heights.
           toFullRowDrag              - Start node dragging by clicking anywhere in it instead only on the caption or image. Must be used together with toDisableDrawSelection.
           toNodeHeightResize         - Allows changing a node's height via mouse.
           toNodeHeightDblClickResize - Allows to reset a node's height to FDefaultNodeHeight via a double click.
           toEditOnClick              - Editing mode can be entered with a single click
           toEditOnDblClick           - Editing mode can be entered with a double click
           toReverseFullExpandHotKey  - Used to define Ctrl+'+' instead of Ctrl+Shift+'+' for full expand (and similar for collapsing)  

    PaintOptions: comma seperated string containing one or more of:
           toHideFocusRect            - Avoid drawing the dotted rectangle around the currently focused node.
           toHideSelection            - Selected nodes are drawn as unselected nodes if the tree is unfocused.
           toHotTrack                 - Track which node is under the mouse cursor.
           toPopupMode                - Paint tree as would it always have the focus (useful for tree combo boxes etc.)
           toShowBackground           - Use the background image if there's one.
           toShowButtons              - Display collapse/expand buttons left to a node.
           toShowDropmark             - Show the dropmark during drag'n drop operations.
           toShowHorzGridLines        - Display horizontal lines to simulate a grid.
           toShowRoot                 - Show lines also at top level (does not show the hidden/internal root node).
           toShowTreeLines            - Display tree lines to show hierarchy of nodes.
           toShowVertGridLines        - Display vertical lines (depending on columns) to simulate a grid.
           toThemeAware               - Draw UI elements (header, tree buttons etc.) according to the current theme if enabled (Windows XP+ only, application must be themed).
           toUseBlendedImages         - Enable alpha blending for ghosted nodes or those which are being cut/copied.
           toGhostedIfUnfocused       - Ghosted images are still shown as ghosted if unfocused (otherwise the become non-ghosted images).
           toFullVertGridLines        - Display vertical lines over the full client area, not only the space occupied by nodes. This option only has an effect if toShowVertGridLines is enabled too.
           toAlwaysHideSelection      - Do not draw node selection, regardless of focused state.
           toUseBlendedSelection      - Enable alpha blending for node selections.
           toStaticBackground         - Show simple static background instead of a tiled one.
           toChildrenAbove            - Display child nodes above their parent.
           toFixedIndent              - Draw the tree with a fixed indent.
           toUseExplorerTheme         - Use the explorer theme if run under Windows Vista (or above).
           toHideTreeLinesIfThemed    - Do not show tree lines if theming is used.
           toShowFilteredNodes        - Draw nodes even if they are filtered out.              

    SelectionOptions: comma seperated string containing one or more of:
           toDisableDrawSelection     - Prevent user from selecting with the selection rectangle in multiselect mode.
           toExtendedFocus            - Entries other than in the main column can be selected, edited etc.
           toFullRowSelect            - Hit test as well as selection highlight are not constrained to the text of a node.
           toLevelSelectConstraint    - Constrain selection to the same level as the selection anchor.
           toMiddleClickSelect        - Allow selection, dragging etc. with the middle mouse button. This and toWheelPanning are mutual exclusive.
           toMultiSelect              - Allow more than one node to be selected.
           toRightClickSelect         - Allow selection, dragging etc. with the right mouse button.
           toSiblingSelectConstraint  - Constrain selection to nodes with same parent.
           toCenterScrollIntoView     - Center nodes vertically in the client area when scrolling into view.
           toSimpleDrawSelection      - Simplifies draw selection, so a node's caption does not need to intersect with the selection rectangle.
           toAlwaysSelectNode         - If this flag is set to true, the tree view tries to always have a node selected. This behavior is closer to the Windows TreeView and useful in Windows Explorer style applications.
           toRestoreSelection         - Set to true if upon refill the previously selected nodes should be selected again. The nodes will be identified by its caption only.     

    StringOptions: comma seperated string containing one or more of:
           toSaveCaptions             - If set then the caption is automatically saved with the tree node, regardless of what is saved in the user data.
           toShowStaticText           - Show static text in a caption which can be differently formatted than the caption but cannot be edited.
           toAutoAcceptEditChange     - Automatically accept changes during edit if the user finishes editing other then VK_RETURN or ESC. If not set then changes are cancelled.    

methods



VirtualStringTree class:
createVirtualStringTree(owner)
properties
  NodeDataSize: integer - The number of bytes to assign for data storage in a node (default is set to hold enough for a pointer)
  OnExpanding: function(sender, node): boolean - called when a node gets expended. Return true to allow
  OnGetText: function(sender, nodeindex, columnindex, node, texttype) : string - called when the text to draw is requested. return the string you wish the field to have
  OnPaintText: function(sender, canvas, node, column, texttype) - called when the text is about to be painted. Use this to change the canvas font colors or do some background painting
  OnDrawText: function(sender, canvas, node, column, celltext, cellrect): defaultdraw - called when text is being painted. return true if you wish the normal painting to happen besides your own, false if you wish to do it all yourself
  OnFreeNode: function(sender, node) - Called when a node gets deleted
  OnInitNode: function(sender, parentnode, node, initialStates) : initialStates - Called when a node gets created. Return the initialStates set (string) to set it's state. initialStates can be a comma seperated string containing one or more of:     ivsDisabled, ivsExpanded, ivsHasChildren, ivsMultiline, ivsSelected,ivsFiltered, ivsReInit 
  TreeOptions: StringTreeOptions 
  FullRowSelect: boolean - Shortcut to TreeOptions->SelectionOptions->toFullRowSelect
  FocusedNode: node - gets/sets the focused node
  FocusedColumn: integer - gets/sets the focused column index

  NodeParent[node]: node - gets/sets the node parent
  NodeHeight[node]: height of the node - gets/sets the height of the node
  HasChildren[node]: boolean - gets/sets the state that the node has children
  Selected[node]: boolean - gets/sets the selected state of the node
  Expanded[node]: boolean - gets/sets if the node is expanded (calls onExpanding when set to true)

methods
  saveToFile(filepath)
  loadFromFile(filepath)


  clear() - deletes all nodes
  beginUpdate()
  endUpdate()
  addChild(parent): node - Adds a child to the tree. Node is an ambiguous object that can only be accessed by the VirtualTreeString object
  addToSelection(node)
  removeFromSelection(node)

  getRootNode(): node - returns the rootnode

  absoluteIndex(node): integer - returns the absolute index of the given node
  nodeSelected(node): boolean - returns true if the node is selected
  nodeChecked(node): boolean - returns true if the node is checked
  enumSelectedNodes(): table - returns an indexed table of selected nodes
  enumCheckedNodes() : table - returns an indexed table of checked nodes
  enumChildren(node) : table - returns an indexed table of childnodes

  deleteNode(node)  - Deletes the given node
  deleteSelectedNodes() - Deletes all selected nodes
  
  getNodeData(node) : bytetable- returns the data of the node as a bytetable
  setNodeData(node, bytetable) - sets the data of the node using a bytetable
  getNodeDataAsInteger(node):integer - returns the node data interpreted as a single integer
  setNodeDataAsInteger(node, integer) - sets the node data as an integer
  getNodeDataPointer(node): integer - Returns the pointer to the node data. You can use the Read/Write*Local functions to access it instead of a bytetable. (Handy when nodedatasize is very big)

  getNodeParent(node): node - returns a parent node, or nil
  getFirstChild(node): node - returns the first child of a node
  getNextSibling(node): node - gets the next sibling


----CEServer----
connectToCEServer(hostname,port) - Connects to the given host and port. On success, most commands subsequent will be handled by the server. Like processlist, memory reading, etc...
isConnectedToCEServer(): boolean - returns true if currently connected to a ceserver
getCEServerPath(): string - returns the path where ceserver is located on the target



ce lua extensions:
string table:
split(character) -> table of strings separated by character  
endsWith('string') : boolean - Returns true if the string ends with the given string
startsWith('string') : boolean - Returns true if the string starts with the given string