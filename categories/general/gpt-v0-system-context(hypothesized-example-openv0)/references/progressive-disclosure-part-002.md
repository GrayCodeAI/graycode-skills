    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\table.mdx",
    "docs": {
      "import": {
        "source": "table.mdx",
        "code": "import {\n  Table,\n  TableBody,\n  TableCaption,\n  TableCell,\n  TableHead,\n  TableHeader,\n  TableRow,\n} from \"@/components/ui/table\""
      },
      "use": [
        {
          "source": "table.mdx",
          "code": "<Table>\n  <TableCaption>A list of your recent invoices.</TableCaption>\n  <TableHeader>\n    <TableRow>\n      <TableHead className=\"w-[100px]\">Invoice</TableHead>\n      <TableHead>Status</TableHead>\n      <TableHead>Method</TableHead>\n      <TableHead className=\"text-right\">Amount</TableHead>\n    </TableRow>\n  </TableHeader>\n  <TableBody>\n    <TableRow>\n      <TableCell className=\"font-medium\">INV001</TableCell>\n      <TableCell>Paid</TableCell>\n      <TableCell>Credit Card</TableCell>\n      <TableCell className=\"text-right\">$250.00</TableCell>\n    </TableRow>\n  </TableBody>\n</Table>"
        }
      ],
      "examples": [
        {
          "source": "table-demo.tsx",
          "code": "import {\r\n  Table,\r\n  TableBody,\r\n  TableCaption,\r\n  TableCell,\r\n  TableHead,\r\n  TableHeader,\r\n  TableRow,\r\n} from \"@/components/ui/table\"\r\n\r\nconst invoices = [\r\n  {\r\n    invoice: \"INV001\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$250.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n  {\r\n    invoice: \"INV002\",\r\n    paymentStatus: \"Pending\",\r\n    totalAmount: \"$150.00\",\r\n    paymentMethod: \"PayPal\",\r\n  },\r\n  {\r\n    invoice: \"INV003\",\r\n    paymentStatus: \"Unpaid\",\r\n    totalAmount: \"$350.00\",\r\n    paymentMethod: \"Bank Transfer\",\r\n  },\r\n  {\r\n    invoice: \"INV004\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$450.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n  {\r\n    invoice: \"INV005\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$550.00\",\r\n    paymentMethod: \"PayPal\",\r\n  },\r\n  {\r\n    invoice: \"INV006\",\r\n    paymentStatus: \"Pending\",\r\n    totalAmount: \"$200.00\",\r\n    paymentMethod: \"Bank Transfer\",\r\n  },\r\n  {\r\n    invoice: \"INV007\",\r\n    paymentStatus: \"Unpaid\",\r\n    totalAmount: \"$300.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n]\r\n\r\nexport default function TableDemo() {\r\n  return (\r\n    <Table>\r\n      <TableCaption>A list of your recent invoices.</TableCaption>\r\n      <TableHeader>\r\n        <TableRow>\r\n          <TableHead className=\"w-[100px]\">Invoice</TableHead>\r\n          <TableHead>Status</TableHead>\r\n          <TableHead>Method</TableHead>\r\n          <TableHead className=\"text-right\">Amount</TableHead>\r\n        </TableRow>\r\n      </TableHeader>\r\n      <TableBody>\r\n        {invoices.map((invoice) => (\r\n          <TableRow key={invoice.invoice}>\r\n            <TableCell className=\"font-medium\">{invoice.invoice}</TableCell>\r\n            <TableCell>{invoice.paymentStatus}</TableCell>\r\n            <TableCell>{invoice.paymentMethod}</TableCell>\r\n            <TableCell className=\"text-right\">{invoice.totalAmount}</TableCell>\r\n          </TableRow>\r\n        ))}\r\n      </TableBody>\r\n    </Table>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Tabs",
    "description": "A set of layered sections of content—known as tab panels—that are displayed one at a time.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\tabs.mdx",
    "docs": {
      "import": {
        "source": "tabs.mdx",
        "code": "import { Tabs, TabsContent, TabsList, TabsTrigger } from \"@/components/ui/tabs\""
      },
      "use": [
        {
          "source": "tabs.mdx",
          "code": "<Tabs defaultValue=\"account\" className=\"w-[400px]\">\n  <TabsList>\n    <TabsTrigger value=\"account\">Account</TabsTrigger>\n    <TabsTrigger value=\"password\">Password</TabsTrigger>\n  </TabsList>\n  <TabsContent value=\"account\">Make changes to your account here.</TabsContent>\n  <TabsContent value=\"password\">Change your password here.</TabsContent>\n</Tabs>"
        }
      ],
      "examples": [
        {
          "source": "tabs-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Card,\r\n  CardContent,\r\n  CardDescription,\r\n  CardFooter,\r\n  CardHeader,\r\n  CardTitle,\r\n} from \"@/components/ui/card\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\nimport {\r\n  Tabs,\r\n  TabsContent,\r\n  TabsList,\r\n  TabsTrigger,\r\n} from \"@/components/ui/tabs\"\r\n\r\nexport default function TabsDemo() {\r\n  return (\r\n    <Tabs defaultValue=\"account\" className=\"w-[400px]\">\r\n      <TabsList className=\"grid w-full grid-cols-2\">\r\n        <TabsTrigger value=\"account\">Account</TabsTrigger>\r\n        <TabsTrigger value=\"password\">Password</TabsTrigger>\r\n      </TabsList>\r\n      <TabsContent value=\"account\">\r\n        <Card>\r\n          <CardHeader>\r\n            <CardTitle>Account</CardTitle>\r\n            <CardDescription>\r\n              Make changes to your account here. Click save when you're done.\r\n            </CardDescription>\r\n          </CardHeader>\r\n          <CardContent className=\"space-y-2\">\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"name\">Name</Label>\r\n              <Input id=\"name\" defaultValue=\"Pedro Duarte\" />\r\n            </div>\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"username\">Username</Label>\r\n              <Input id=\"username\" defaultValue=\"@peduarte\" />\r\n            </div>\r\n          </CardContent>\r\n          <CardFooter>\r\n            <Button>Save changes</Button>\r\n          </CardFooter>\r\n        </Card>\r\n      </TabsContent>\r\n      <TabsContent value=\"password\">\r\n        <Card>\r\n          <CardHeader>\r\n            <CardTitle>Password</CardTitle>\r\n            <CardDescription>\r\n              Change your password here. After saving, you'll be logged out.\r\n            </CardDescription>\r\n          </CardHeader>\r\n          <CardContent className=\"space-y-2\">\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"current\">Current password</Label>\r\n              <Input id=\"current\" type=\"password\" />\r\n            </div>\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"new\">New password</Label>\r\n              <Input id=\"new\" type=\"password\" />\r\n            </div>\r\n          </CardContent>\r\n          <CardFooter>\r\n            <Button>Save password</Button>\r\n          </CardFooter>\r\n        </Card>\r\n      </TabsContent>\r\n    </Tabs>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Textarea",
    "description": "Displays a form textarea or a component that looks like a textarea.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\textarea.mdx",
    "docs": {
      "import": {
        "source": "textarea.mdx",
        "code": "import { Textarea } from \"@/components/ui/textarea\""
      },
      "use": [{ "source": "textarea.mdx", "code": "<Textarea />" }],
      "examples": [
        {
          "source": "textarea-demo.tsx",
          "code": "import { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaDemo() {\r\n  return <Textarea placeholder=\"Type your message here.\" />\r\n}"
        },
        {
          "source": "textarea-disabled.tsx",
          "code": "import { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaDisabled() {\r\n  return <Textarea placeholder=\"Type your message here.\" disabled />\r\n}"
        },
        {
          "source": "textarea-with-button.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithButton() {\r\n  return (\r\n    <div className=\"grid w-full gap-2\">\r\n      <Textarea placeholder=\"Type your message here.\" />\r\n      <Button>Send message</Button>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "textarea-with-label.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithLabel() {\r\n  return (\r\n    <div className=\"grid w-full gap-1.5\">\r\n      <Label htmlFor=\"message\">Your message</Label>\r\n      <Textarea placeholder=\"Type your message here.\" id=\"message\" />\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "textarea-with-text.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithText() {\r\n  return (\r\n    <div className=\"grid w-full gap-1.5\">\r\n      <Label htmlFor=\"message-2\">Your Message</Label>\r\n      <Textarea placeholder=\"Type your message here.\" id=\"message-2\" />\r\n      <p className=\"text-sm text-muted-foreground\">\r\n        Your message will be copied to the support team.\r\n      </p>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Toast",
    "description": "A succinct message that is displayed temporarily.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\toast.mdx",
    "docs": {
      "import": {
        "source": "toast.mdx",
        "code": "import { useToast } from \"@/components/ui/use-toast\""
      },
      "use": [],
      "examples": [
        {
          "source": "toast-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastDemo() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Scheduled: Catch up \",\r\n          description: \"Friday, February 10, 2023 at 5:57 PM\",\r\n          action: (\r\n            <ToastAction altText=\"Goto schedule to undo\">Undo</ToastAction>\r\n          ),\r\n        })\r\n      }}\r\n    >\r\n      Add to calendar\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-destructive.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastDestructive() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          variant: \"destructive\",\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n          action: <ToastAction altText=\"Try again\">Try again</ToastAction>,\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-simple.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastSimple() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          description: \"Your message has been sent.\",\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-with-action.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastWithAction() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n          action: <ToastAction altText=\"Try again\">Try again</ToastAction>,\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-with-title.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastWithTitle() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Toggle",
    "description": "A two-state button that can be either on or off.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\toggle.mdx",
    "docs": {
      "import": {
        "source": "toggle.mdx",
        "code": "import { Toggle } from \"@/components/ui/toggle\""
      },
      "use": [{ "source": "toggle.mdx", "code": "<Toggle>Toggle</Toggle>" }],
      "examples": [
        {
          "source": "toggle-demo.tsx",
          "code": "import { Bold } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleDemo() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\">\r\n      <Bold className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-disabled.tsx",
          "code": "import { Underline } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleDisabled() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\" disabled>\r\n      <Underline className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-lg.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleLg() {\r\n  return (\r\n    <Toggle size=\"lg\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-outline.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleOutline() {\r\n  return (\r\n    <Toggle variant=\"outline\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-sm.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleSm() {\r\n  return (\r\n    <Toggle size=\"sm\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-with-text.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleWithText() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\">\r\n      <Italic className=\"mr-2 h-4 w-4\" />\r\n      Italic\r\n    </Toggle>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Tooltip",
    "description": "A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\tooltip.mdx",
    "docs": {
      "import": {
        "source": "tooltip.mdx",
        "code": "import {\n  Tooltip,\n  TooltipContent,\n  TooltipProvider,\n  TooltipTrigger,\n} from \"@/components/ui/tooltip\""
      },
      "use": [
        {
          "source": "tooltip.mdx",
          "code": "<TooltipProvider>\n  <Tooltip>\n    <TooltipTrigger>Hover</TooltipTrigger>\n    <TooltipContent>\n      <p>Add to library</p>\n    </TooltipContent>\n  </Tooltip>\n</TooltipProvider>"
        }
      ],
      "examples": [
        {
          "source": "tooltip-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Tooltip,\r\n  TooltipContent,\r\n  TooltipProvider,\r\n  TooltipTrigger,\r\n} from \"@/components/ui/tooltip\"\r\n\r\nexport default function TooltipDemo() {\r\n  return (\r\n    <TooltipProvider>\r\n      <Tooltip>\r\n        <TooltipTrigger asChild>\r\n          <Button variant=\"outline\">Hover</Button>\r\n        </TooltipTrigger>\r\n        <TooltipContent>\r\n          <p>Add to library</p>\r\n        </TooltipContent>\r\n      </Tooltip>\r\n    </TooltipProvider>\r\n  )\r\n}"
        }
      ]
    }
  }
]
