---
name: Component request
about: Suggest an idea for this project
title: "[COMPONENT]"
labels: ''
assignees: zainhoda

---

## Description (required) 

## Proposed HTML (optional)
Any template format is ok as long as it's clear where the parameters should go. For more advanced components which require transformations before inserting into the HTML, just describe what you think it should do.
```html
<a class="\(classes)" href="\(url)">\(text)</a>
```

## Spec JSON (optional)
```json
{
  "category" : "Basic HTML",
  "arguments" : [
    {
      "name" : "text",
      "type" : "String",
      "description" : "Text to be rendered"
    },
    {
      "name" : "url",
      "type" : "String",
      "description" : "URL to link to"
    },
    {
      "defaultValue" : "",
      "name" : "classes",
      "type" : "Optional String",
      "description" : "Classes to be applied to the link"
    }
  ],
  "elementType" : "plainlink",
  "attachableTo" : [
    "page",
    "navbar",
    "card",
    "container"
  ],
  "exampleCode" : [
    {
      "arguments" : [
        {
          "argumentName" : "text",
          "argumentValue" : "Here's a link"
        },
        {
          "argumentName" : "url",
          "argumentValue" : "https:\/\/www.pycob.com"
        }
      ]
    }
  ],
  "description" : "Renders a link without any styling",
  "name" : "Unstyled Link"
}
```
